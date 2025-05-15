import pygame
import settings
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self, ai_settings, screen, scale = 1):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = settings.load_image("ship.png", None, scale)
        # 加载飞船图像并获取其外接矩形
        self.rect = self.image.get_rect()
        # 加载屏幕的外接矩形
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        # 飞船中心的x坐标
        self.centerX = float(self.screen_rect.centerx)
        self.rect.centerx = self.centerX
        # 飞船的截断Y轴高
        self.rect_heightY = (self.rect.height / 16 * 2)
        self.centerY = float(self.screen_rect.bottom - (self.rect.height / 2) + self.rect_heightY)
        # 飞船中心的y坐标
        self.rect.centery = self.centerY
        # 飞船初始位置
        self.center_ship_xy = (self.centerX, self.centerY)


        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置,并限制飞船在屏幕内"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 向右移动飞船
            self.centerX += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            # 向左移动飞船
            self.centerX -= self.ai_settings.ship_speed_factor  
        if self.moving_up and self.rect.top > self.screen_rect.top:
            # 向上移动飞船
            self.centerY -= self.ai_settings.ship_speed_factor
        if self.moving_down and (self.rect.bottom - self.rect_heightY) < self.screen_rect.bottom:
            # 向下移动飞船
            self.centerY += self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = int(self.centerX)  
        self.rect.centery = int(self.centerY)    

    def blitme(self):
        """在指定位置绘制飞船""" 
        self.screen.blit(self.image,self.rect) 

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.centerX = self.center_ship_xy[0]
        self.centerY = self.center_ship_xy[1]
        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY