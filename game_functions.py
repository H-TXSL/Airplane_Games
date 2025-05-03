# 模块sys来退出游戏
import sys
import pygame
from bullet import Bullet
# 游戏功能

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
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


def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 关闭游戏窗口
        # 检测到pygame.QUIT事件,调用sys.exit()来退出游戏
        if event.type == pygame.QUIT:
            sys.exit()
        # 按键响应
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
                
def update_screen(ai_settings, screen, ship, bullets):
    """"更新屏幕上的图像,并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(ai_settings.bg_color)
    
    # 在飞船和敌人后重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    """更新子弹的位置,并删除已消失的子弹"""
    # 更新子弹的位置
    # 调用编组的update()方法,编组会自动对其中的每个精灵调用update()方法
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

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

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制,就发射一颗子弹"""
    # 创建一颗子弹,并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        # 确保新子弹 x 坐标在飞机中心
        new_bullet.rect.centerx = ship.rect.centerx
        bullets.add(new_bullet)