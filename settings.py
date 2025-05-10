import os
import pygame

class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置""" 
        # 屏幕设置
        self.screen_info = pygame.display.Info()
        self.screen_width = 1200
        self.screen_height = 600
        # self.screen_width = self.screen_info.current_w
        # self.screen_height = self.screen_info.current_h
        self.bg_color = (0, 0, 0)
        
        # 飞船速度设置
        self.ship_speed_factor = 1.5
        # 飞船数限制
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed_factor = 3.0
        # 子弹放大的限制数
        self.bullet_count = 10
        # 设置初始子弹缩放大小
        self.bullet_scale = 0.25
        # 设置重置子弹缩放的次数
        self.bullet_scale_count = 50
        # 限制子弹数量
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed_factor = 0.5
        # fleet_drop_speed表示外星人撞到屏幕边缘时向下移动的速度
        self.fleet_drop_speed = 15
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        
    
# 图像路径设置
# 保证在不同的操作系统中都能正确地访问图像文件
# 获取当前脚本的绝对路径
main_dir = os.path.split(os.path.abspath(__file__))[0]
# 构建图像路径
images_dir = os.path.join(main_dir, "images") 

# 加载图像的函数 参数：图像名称，颜色键，缩放比例
def load_image(name, colorkey=None, scale=1.0, images_dir=images_dir):
    # 加载图像并转换为Surface对象
    fullname = os.path.join(images_dir, name)
    image = pygame.image.load(fullname)
    # 设置缩放比例
    if scale != 1:
        size = image.get_size()
        new_size = (int(size[0] * scale), int(size[1] * scale))
        image = pygame.transform.scale(image, new_size)
    # 转换图像的颜色格式为Pygame支持的格式，以提高性能 
    image = image.convert_alpha()
    # 设置颜色键
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image
