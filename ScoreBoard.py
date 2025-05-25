'''在画之前都要调用prep函数'''

white = (250, 250, 250)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
import pygame.font
import pygame.image
from pygame.sprite import Sprite
from pygame.sprite import Group

class Score_Board:
    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = self.ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = self.ai_game.settings
        self.stats = self.ai_game.stats
        self.text_color = red
        self.font = pygame.font.SysFont("arial",32)
        #实例化一个字体对象，第一个参数表示字体，第二个参数表示大小
        self.prep_score()
        self.prep_high_score()
        self.prep_level()#如果没有调用prep函数直接show_score，报错
        self.prep_message()
        self.prep_lives()
    def prep_score(self):
        #score_str = str(self.stats.score)
        round_score = round(self.stats.score,-1)#将传入数据精确到小数点后几位，-1表示精确到10位
        score_str = "{:,}".format(round_score)
        _score_str = "Score:"+score_str
        self.score_image = self.font.render(_score_str,True,self.text_color,self.settings.bg_color)
        #render创建图像
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        round_high_score = round(self.stats.high_score,-1)
        high_score_str = "{:,}".format(round_high_score)
        _high_score_str = "Highest:" + high_score_str
        self.high_score_image = self.font.render(_high_score_str,True,self.text_color,self.settings.bg_color)
        self._high_score_rect = self.high_score_image.get_rect()
        self._high_score_rect.center = self.screen_rect.center
        self._high_score_rect.top = 20

    def prep_level(self):
        level_str = str(self.stats.level)
        _level_str = "Level:"+level_str
        self.level_image = self.font.render(_level_str,True,self.text_color,self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        level_width,level_height = self.level_rect.size
        self.level_rect.right = self.screen_rect.right
        self.level_rect.y = self.settings.screen_height - level_height

    def prep_message(self):
        message = "You are done!!!!"
        self.message_image = self.font.render(message,True,self.text_color,self.settings.bg_color)
        self.message_rect = self.message_image.get_rect()
        m_width,m_height = self.message_rect.size
        self.message_rect.midbottom = self.screen_rect.midbottom
        self.message_rect.y = self.settings.screen_height - 5 * m_height
    def _check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self._high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.lives.draw(self.screen)
    def show_message(self):
        self.screen.blit(self.message_image,self.message_rect)



    def prep_lives(self):
        self.lives = Group()
        for live_number in range(self.stats.ships_left):
            live = Live(self.ai_game)
            live.rect.x = 10+live_number*live.rect.width #不小心变成加号，三个爱心重叠在一起。
            live.rect.y = 10
            self.lives.add(live)






class Live(Sprite):
    def __init__(self,ai_game):
        super().__init__()

        self.image = pygame.image.load('image/螢幕擷取畫面 2023-11-19 105312.png')
        self.rect = self.image.get_rect()