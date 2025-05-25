import pygame.font
white = (250, 250, 250)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

class Button:
    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width,self.height =200,50
        self.text_color = white
        self.button_color = green
        self.font = pygame.font.SysFont("arial",32)
        #指定使用什么字体来渲染文本,实参None 让Pygame使用默认字体，而48 指定了文本的字号。
        self.rect = pygame.Rect(0,0,self.width,self.height)#创建表示按键的rect对象
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        #调用font.render() 将存储在msg 中的文本转换为图像,Bool实参决定是否开启反锯齿功能，如果没有指定背景色，自动渲染成透明
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)#接受两个参数，一个是颜色，一个是位置
        self.screen.blit(self.msg_image,self.msg_rect)#一个参数是图像，一个参数是位置

