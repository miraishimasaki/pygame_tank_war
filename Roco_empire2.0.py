"""使用for 循环遍历列表（或Pygame编组）时，Python要求该列表的
长度在整个循环中保持不变。因为不能从for 循环遍历的列表或编
组中删除元素，所以必须遍历编组的副本。我们使用方法copy()"""
#思考p键重启技能
from music import Music
from alien import Alien
from bullet import Bullet
from ship import Ship
from setting import Settings
import sys
from time import sleep
from game_stas import GameStats
import pygame
from button import Button
from ScoreBoard import Score_Board

class AlienInvasion:      #主初始化中的调用顺序很关键，因为解释器从上往下读取。
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.stats = GameStats(self)
        self.sb = Score_Board(self)
        self.music = Music()  #初始化音乐实例
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.ship = Ship(self)

        self.alien_hit_sound = self.settings.alien_hit_sound
        self.losser_sound = pygame.mixer.Sound('music/preview.mp3')
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self._creat_fleet()
        self.play_button = Button(self,"PLAY")


        pygame.display.set_caption("Roco Empire")


    def run_game(self):

        while True:                   #辅助方法放在RUN_GAME里面直接调用，使用不用通过实例调用。
            self._check_events()

            if self.stats.game_active:
                self.ship.update()          #通过飞船的实例调用
                self._update_bullets()
                                    #若此处添加self._creat_fleets()方法，兔仙人将一直在屏幕上。(不会移动)
                self._update_aliens()

            self._update_screen()

    def _start_game(self):
        self.music.play_music()
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_lives()
        self.stats.game_active = True
        self.aliens.empty()
        self.bullets.empty()
        self._creat_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)  # 传入的布尔值表示是否隐藏鼠标光标

    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #pygame.mouse.get_pos() ，它返回一个元组，其中包含玩家单击时鼠标的x坐标和y坐标
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            #使用了rect 的方法collidepoint() 检查鼠标单击位置是否在Play按钮的rect 内
            self._start_game()
    def _check_keydown_events(self,event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_UP:
            self.ship.moving_up = True

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down  = True

        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self.fire_bullets()

        elif event.key == pygame.K_p:
            self._start_game()
    def _check_keyup_events(self,event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    def _update_screen(self):
        #if self.stats.game_active:
         #self.screen.blit(self.bg,(0,0))  #绘制背景
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets:
            bullet.DrawBullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        self._check_done()

        if not self.stats.game_active:

            #pygame.mixer.music.load('music/bgm(castle).wav')
            #pygame.mixer.music.play(-1)
            #self.screen.blit(self.settings.bg_image,(0,0))
            self.play_button.draw_button()

        pygame.display.flip()
    def _update_bullets(self):
        self.bullets.update()    #通过编组的实例调用，对编组里面的每一个sprite都调用bullet.update()。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)  # 在循环中副本中编组元素个数保持不变，原编组删除对应元素
        print(len(self.bullets))
        self._check_collisions()


    def fire_bullets(self):
        if len(self.bullets) < self.settings.bullet_allowed:
           new_bullet = Bullet(self)
           self.bullets.add( new_bullet )


    def _creat_fleet(self):
        alien = Alien(self)

        alien_width = alien.rect.width
        available_x = self.settings.screen_width - 2*(alien_width)
        number_aliens_x = available_x//(2*alien_width)


        for row_number in range(3):

            for number in range(number_aliens_x):
                self._creat_a_aliens(number,row_number)

    def _creat_a_aliens(self,number,row_number):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size #属性size 。该属性是一个元组，包含rect 对象的宽度和高度。
        alien.x = alien_width + 2 * alien_width * number
        alien.rect.x = alien.x
        alien.y = alien_height +2 * alien_height*row_number
        alien.rect.y = alien.y

        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_alien_bottom()

#函数spritecollideany() 接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组。

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_direction()
                break

    def _change_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.settings.drop_speed
        self.settings.speed_direction *= -1    #一个撞墙，全部改变方向。

    def _check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        '''每当有子弹和外星人的rect 重叠时，groupcollide() 就在它返回的字典中添加一个键值对。两个实参True 让Pygame删除发生碰撞的子弹和外
        星人。'''
        if collisions:
            self.alien_hit_sound.set_volume(0.10)
            self.alien_hit_sound.play()
            self.stats.score += self.settings.alien_points
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb._check_high_score()
#在_check_bullet_alien_collisions()中，与外星人碰撞的子弹都是字典collisions中的一个键，而与每颗子弹相关的值都是一个列表，其中包含该子弹击中的外星人。
        if not self.aliens:
            self.settings.clear_sound.set_volume(0.75)
            self.settings.clear_sound.play()
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self._creat_fleet()


    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_lives()
            self.aliens.empty()
            self.bullets.empty()
            self._creat_fleet()
            self.ship.center_ship()


            self.losser_sound.play()
            self.losser_sound.set_volume(0.25)
            print("Ship hittt!!!!!!")
            sleep(0.1)

        else:

            self.music._stop()
            self.settings.alien_bottom_sound.set_volume(0.25)
            self.settings.alien_bottom_sound.play()
            sleep(3)
            self.settings.fail_sound.set_volume(0.5)
            self.settings.fail_sound.play()
        # self.sb.show_message()#为啥没用？就因为它放在update_aliens()下面

            self.stats.game_active = False
            pygame.mouse.set_visible(True)#在游戏结束后重新显示光标

    def _check_alien_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom > self.screen_rect.bottom:
                self.aliens.empty()
                self.bullets.empty()
                self._creat_fleet()
                self.ship.center_ship()

                self.settings.alien_bottom_sound.set_volume(0.25)
                self.settings.alien_bottom_sound.play()
                print("Ship hittt!!!!!!")
                sleep(0.1)
                break
    def _check_done(self):
        #self.stats.ships_left -= 1 #如果放上这行代码，一开始就会显示message
        if not self.stats.game_active and self.stats.ships_left <= 1:
            self.stats.ships_left -= 1
            self.sb.prep_lives() #让最后一架飞船消失后可以看到生命条归零
            self.sb.show_message()


if __name__ == '__main__':
    ai = AlienInvasion()
     #放在主循环前，无画面
    ai.run_game()
     #放在主循环后，无音乐