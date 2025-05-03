# 模块pygame包含开发游戏所需的功能
import pygame

# 从模块中导入特定的对象
from settings import Settings
from ship import Ship
# 导入整个模块
# 模块game_functions指定了别名gf
import game_functions as gf
from pygame.sprite import Group
 
def run_game():  
    # 初始化背景设置
    pygame.init()
    ai_settings = Settings()
    # 指定了游戏窗口的尺寸
    # display.set_mode()返回的surface表示整个游戏窗口
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 游戏窗口名称
    pygame.display.set_caption("Alien Invasion")

    # 创建飞船
    ship = Ship(ai_settings, screen)
    # 创建存储子弹的编组
    bullets = Group()

    # 主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)
        # 更新飞船位置
        ship.update()
        # 更新子弹
        gf.update_bullets(bullets)
        # 更新屏幕上的图像
        gf.update_screen(ai_settings, screen, ship, bullets)

run_game()