import pygame 
import os

from pygame.sprite import Sprite
from settings import images_dir, load_image

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings


        # 子弹图像路径
        bullet_dir = os.path.join(images_dir, "bullets")
        # 加载子弹图像并转换为Surface对象
        bullets = [f for f in os.listdir(bullet_dir) if int(os.path.splitext(f)[0][-1]) < 9]
        bullets.sort()
        self.images = []
        for bullet in bullets:
            self.images.append(load_image(bullet, None, 0.25, bullet_dir))
        
        # 加载子弹图像并获取其外接矩形
        self.rects_index = 0
        self.rect = self.images[self.rects_index].get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor


        # 用于控制子弹图像切换的计数器
        self.frame_counter = 0
        # 用于控制子弹图像切换的频率
        self.frame_rate = 1  # 每10帧切换一次图像

        # 保存初始子弹缩放
        self.current_scale =  ai_settings.bullet_scale
        # 保存缩放后的子弹图像列表
        # 预先生成缩放版本, 确保动画帧与缩放版本一一对应
        self.scale_images = [
            # 列表推导式 
            pygame.transform.scale(img, (int(img.get_width() * self.current_scale), int(img.get_height() * self.current_scale)))
            for img in self.images  # 预生成所有缩放图像
        ]

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

        # 控制子弹图像切换
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            # 循环切换图像索引
            self.rects_index = (self.rects_index + 1) % len(self.scale_images)  

            # 直接使用预生成的缩放图像
            self.rect = self.scale_images[self.rects_index].get_rect(center = self.rect.center)


           
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.scale_images[self.rects_index], self.rect)
