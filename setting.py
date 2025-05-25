
from pygame import image
from pygame import transform
from pygame import mixer
white = (250, 250, 250)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
speed = 30
fps = 30
tip_width = 1200
tip_height =800
full_width = 1440
full_height = 900


class Settings:
    def __init__(self):
        self.screen_width = tip_width
        self.screen_height = tip_height
        self.bg_color = (white)
        self.ship_speed = 3
        self.bullet_speed = 1
        self.bullet_allowed = 5
        self.alien_speed = 0.3
        self.fps = fps
        self.drop_speed = 30
        self.speed_direction = 1
        self.ship_limit = 3
        self.alien_hit_sound = mixer.Sound('music/5c88e50f1759533914.mp3')
        self.alien_bottom_sound = mixer.Sound('music/5c891516ceb6539239.mp3')
        self.clear_sound = mixer.Sound('music/newbee.wav')
        self.fail_sound = mixer.Sound('music/failure_scream.mp3')
        # self.bg = image.load('image/螢幕擷取畫面 2023-11-11 221053.png')

        # self.bg_image = transform.scale(self.bg,(self.screen_width,self.screen_height))
        self.speedup_scale = 1.1
        self.alien_points = 50
        self.point_scale = 1.5



    def initialize_dynamic_settings(self):
        self.bullet_speed = 1
        self.alien_speed = 0.3
        self.speed_direction = 1
        self.ship_speed = 3

    def increase_speed(self):
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.ship_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.point_scale)