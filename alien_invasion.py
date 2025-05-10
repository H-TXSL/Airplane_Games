# 模块pygame包含开发游戏所需的功能
import pygame

# 从模块中导入特定的对象
from settings import Settings
from ship import Ship
from alien import Alien
# 导入整个模块
# 模块game_functions指定了别名gf
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
 
def run_game():  
    # 初始化背景设置
    pygame.init()   
    ai_settings = Settings()
    # 指定了游戏窗口的尺寸
    # display.set_mode()返回的surface表示整个游戏窗口
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 游戏窗口名称
    pygame.display.set_caption("Alien Invasion")
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建飞船
    ship = Ship(ai_settings, screen)
    # 创建外星人
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 创建存储子弹的编组
    bullets = Group()


    # 主循环
    while True:
        # 添加事件泵处理底层事件队列,同时保持与系统事件处理的兼容性
        pygame.event.pump()
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            # 更新飞船位置
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            # 更新外星人
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        # 更新屏幕上的图像
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)

run_game()