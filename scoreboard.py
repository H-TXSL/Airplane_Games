import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时的字体信息
        self.text_color = (30, 30, 30)
        # 黑体字体,保证中文显示
        self.font = pygame.font.SysFont('simhei', 32)

        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()

        self.prep_ships()

    def prep_score(self):
        # 准备初始得分图像
        # 化整数倍
        rounded_score = int(round(self.stats.score, -1))
        # 将逗号作为千分位分隔符
        score_str = "分数: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "最高分数: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_ships(self):
        """显示剩余飞船数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen, 0.25)
            ship.rect.x = 10 + ship_number * ship.rect.width + (ship_number * 10)
            ship.rect.y = 10
            self.ships.add(ship)
            

    def show_score(self):
        """显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # 飞船
        self.ships.draw(self.screen)
