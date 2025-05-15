from pickle import FALSE
import pygame
import os
import random
from pygame.sprite import Sprite
from settings import images_dir, load_image

def file_sort(filename):
    return int(filename[13:-4])

class Alien(Sprite):
    """"外星人类"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # 图像路径
        alien_dir = os.path.join(images_dir, "alien")
        # 图像Surface对象
        aliens = [f for f in os.listdir(alien_dir) if os.path.splitext(f)[1] == ".png"]
        aliens.sort(key=file_sort)
        self.images = []
        for alien in aliens:
            self.images.append(load_image(alien, None, 0.5, alien_dir))
        
        self.rects_index = 0
        self.image = self.images[self.rects_index]
        self.rect = self.images[self.rects_index].get_rect()
        self.rect.centerx = self.rect.width
        self.rect.y = self.rect.height / 2

        self.x = float(self.rect.centerx)
        self.y = float(self.rect.y)

        # 控制图像切换的计数器
        self.frame_counter = 0
        # 切换频率
        self.frame_rate = 15

    def update(self):
        """移动外星人"""
        self.x += self.ai_settings.alien_speed_factor *  self.ai_settings.fleet_direction
        
        # 更新rect
        self.rect.centerx = self.x

        # 控制图像切换
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.rects_index = (self.rects_index + 1) % len(self.images)
            self.image = self.images[self.rects_index]
            self.rect = self.images[self.rects_index].get_rect(center=self.rect.center)

    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
        

    
