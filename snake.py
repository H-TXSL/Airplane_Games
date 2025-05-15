import os
from settings import images_dir, load_image
from pygame.sprite import Sprite
import random

def file_sort(filename):
    return int(filename[6:-4])

class Snake(Sprite):
    def __init__(self, ai_settings, screen):
        super(Snake, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        # 蛇
        snake_dir = os.path.join("images", "snake")
        snakes = [f for f in os.listdir(snake_dir)]
        snakes.sort(key=file_sort)
        self.snake_images = []
        for snake in snakes:
            self.snake_images.append(load_image(snake, None, 1, snake_dir))
        self.snake_rects_index = 0

        print(len(self.snake_images))
        # Surface对象
        self.snake_image = self.snake_images[self.snake_rects_index]
        # 外接矩形
        self.snake_rect = self.snake_image.get_rect()
        self.snake_rect.centerx = random.randint(0, self.screen_rect.width - self.snake_rect.width)
        self.snake_rect.top = self.ai_settings.screen_height
        self.rect = self.snake_rect

        self.y = float(self.snake_rect.top)
        # 切换帧计时器
        self.snake_frame_counter = 0
        self.snake_frame_rate = 50
        # 动画flag
        self.snake_flag = False

    def update(self):
        self.y -= self.ai_settings.snake_speed_factor
        self.snake_rect.top = self.y
        self.rect = self.snake_rect

        self.snake_frame_counter += 1
        if self.snake_frame_counter>= self.snake_frame_rate:
            self.snake_frame_counter = 0
            self.snake_rects_index = (self.snake_rects_index + 1) % len(self.snake_images)
            self.snake_image = self.snake_images[self.snake_rects_index]
            self.snake_rect = self.snake_image.get_rect(center=self.snake_rect.center)
    
    def snake_blit(self):
        self.screen.blit(self.snake_image, self.snake_rect)