import imp
import sys
import pygame

from hashlib import new
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion():
    """Class is responsible for managenet resourses and game beheivor"""

    def __init__(self):
        """Initializing game and creating game resourses"""
        pygame.init()
        self.FPS = 60
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("AlienInvasion")
        self.clock = pygame.time.Clock()

        #creation of instance for game statistic's storage
        #and result bar
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.star = Star(self)

        self._create_fleet()

        #creation of button Play
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Starting main game cycle"""
        while True:
            self.clock.tick(self.FPS)
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Tracking events of keyboard and mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start new game if button Play is pressed"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset game parameters
            self.settings.initialize_dynamic_settings()
            #reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_high_score()

            #erase existing bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            #creation new fleet and placement ship in the center
            self._create_fleet()
            self.ship.center_ship()

            #hide mouse pointer
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """reacts to press buttons"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.write_record()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """reacts to release buttons"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _ship_hit(self):
        """treat collision alien - ship"""

        if self.stats.ship_left > 0:
            #reduse ship_left and update score panel
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            #erase existing bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            #creation of new fleet and placemeten of ship in the center
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """checking of alien's achievment to bottom edge of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _fire_bullet(self):
        """create new bullet and including it in group bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update bullet position and erase bullets reaching top edge of screen"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Treatment of collisions bullets and aliens"""
        #If alien hitted - erase bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #erase existing bullets and creation of new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """update positions of all aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        #checking collisions "alien - ship"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #checking of alien's achievment to bottom edge of screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        """creation of alien's fleet"""
        #creation alien and estimation of alien number in row
        #gap between aliens is equal of alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """specify number of alien rows in screen"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #creation of alien fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """creation of alien and placement him in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """react to alien's reaching the screen egde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop alien fleet down and chenge moving direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Display is updated every cycle and show the last drawn display"""
        self.screen.fill(self.settings.bg_color)
        #self.star.blitme()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #output of score
        self.sb.show_score()

        #button Play display if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    #Creation class instance
    ai = AlienInvasion()
    ai.run_game()
