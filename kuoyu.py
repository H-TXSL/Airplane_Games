import os
from settings import images_dir, load_image

def file_sort(filename):
    return int(filename[6:-4])

class Kuoyu():

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 蛞蝓
        kuoyu_dir = os.path.join("images", "kuoyu")
        kuoyus = [f for f in os.listdir(kuoyu_dir)]
        kuoyus.sort(key=file_sort)
        self.kuoyu_images = []
        for kuoyu in kuoyus:
            self.kuoyu_images.append(load_image(kuoyu, None, 2, kuoyu_dir))
        self.kuoyu_rects_index = 0
        # Surface对象
        self.kuoyu_image = self.kuoyu_images[self.kuoyu_rects_index]
        # 外接矩形
        self.kuoyu_rect = self.kuoyu_image.get_rect()
        self.kuoyu_rect.centerx = self.screen_rect.centerx
        self.kuoyu_rect.centery = self.screen_rect.centery
        # 切换帧计时器
        self.kuoyu_frame_counter = 0
        self.kuoyu_frame_rate = 20
        # 动画flag
        self.kuoyu_flag = False

    def kuoyu_update(self):
        self.kuoyu_frame_counter += 1
        if self.kuoyu_frame_counter>= self.kuoyu_frame_rate:
            self.kuoyu_frame_counter = 0
            self.kuoyu_rects_index = (self.kuoyu_rects_index + 1) % len(self.kuoyu_images)
            self.kuoyu_image = self.kuoyu_images[self.kuoyu_rects_index]
            self.kuoyu_rect = self.kuoyu_image.get_rect(center=self.kuoyu_rect.center)
        
    def kuoyu_blit(self, screen):
        """绘制蛞蝓"""
        self.kuoyu_update()
        screen.blit(self.kuoyu_image, self.kuoyu_rect)

        if self.kuoyu_rects_index >= (len(self.kuoyu_images) - 1):
            self.kuoyu_flag = False
        