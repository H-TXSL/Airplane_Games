# 模块sys来退出游戏
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
# 游戏功能

def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_q:
        # 快捷键Q 退出
        sys.exit()
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, stats, ship, bullets)
        scale_bullet(ai_settings)

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.flag = False
        # 重置游戏设置
        stats.reset_stats()
        stats.game_active = True

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人,并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 关闭游戏窗口
        # 检测到pygame.QUIT事件,调用sys.exit()来退出游戏
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and stats.flag:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        # 按键响应
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
                
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """"更新屏幕上的图像,并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(ai_settings.bg_color)
    
    # 在飞船和敌人后重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    # 对编组调用draw()时，Pygame自动绘制编组的每个元素
    aliens.draw(screen)
    # draw() 底层实现
    # for alien in aliens.sprites():
    #     screen.blit(alien.image, alien.rect)
    # 让最近绘制的屏幕可见

    # 如果游戏处于非活动状态,就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """更新外星人的位置"""
    # 检查是否有外星人位于屏幕边缘,并更新整群外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """更新子弹的位置,并删除已消失的子弹"""
    # 更新子弹的位置
    # 调用编组的update()方法,编组会自动对其中的每个精灵调用update()方法
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # 检查是否有子弹击中了敌人,如果是这样,就删除相应的子弹和敌人
    check_alien_collisions(ai_settings, screen, ship, aliens, bullets)
    

def check_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """响应外星人与子弹的碰撞"""
    # collisions()方法接受一个精灵,并返回一个字典,其中包含了与该精灵发生碰撞的所有精灵
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹,并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

bullet_fire_count = 0
def scale_bullet(ai_settings):
    """缩放子弹"""
    global bullet_fire_count 
    bullet_fire_count += 1
    if bullet_fire_count % ai_settings.bullet_count == 0:
        ai_settings.bullet_scale *= 2.0
    
    # 重置子弹缩放
    if bullet_fire_count >= ai_settings.bullet_scale_count:
        ai_settings.bullet_scale = 0.25
        bullet_fire_count = 0

def fire_bullet(ai_settings, screen, stats, ship, bullets):
    """如果还没有到达限制,就发射一颗子弹"""
    # 创建一颗子弹,并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
        new_bullet = Bullet(ai_settings, screen, ship)
        # 确保新子弹 x 坐标在飞机中心
        new_bullet.rect.centerx = ship.rect.centerx
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群""" 
    # 创建一个外星人，并计算一行可容纳多少个外星人 
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    

    for row in range(number_rows):
        # 创建外星人群
        for alien_number in range(number_aliens_x):
            # 创建外星人并加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 计算一行可容纳多少个外星人
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # 计算每个外星人的x, y坐标
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = (alien.rect.height / 2) + (alien.rect.height * row_number)
    alien.rect.y = alien.y
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (1.5 * alien_height) - ship_height)
    number_rows = int(available_space_y / alien_height)
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.y += ai_settings.fleet_drop_speed
        alien.rect.y = alien.y
    ai_settings.fleet_direction *= -1

    

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将ships_left减1
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 飞船移动状态重置
        ship.moving_right = False
        ship.moving_left = False
        ship.moving_up = False
        ship.moving_down = False

        # 创建一群新的外星人,并将飞船放到屏幕底端中央
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)
        

        # 用 Pygame 的方式实现暂停（替换 sleep）
        pause_time = pygame.time.get_ticks() + 500  # 500 毫秒 = 0.5秒
        while pygame.time.get_ticks() < pause_time:
            pygame.event.pump()  # 保持事件循环
            pygame.time.wait(1)  # 每10毫秒检查一次
    else:
        stats.game_active = False
        stats.flag = True
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
