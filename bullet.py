import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """control for bullet of ship"""

    def __init__(self, ai_game):
        """create object of bullet in current position of ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create bullet in position (0, 0) and assign right position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #position of bullet saved in real format
        self.y = float(self.rect.y)

    def update(self):
        """moving up bullet on screen"""
        #update of bullet position in real formate
        self.y -= self.settings.bullet_speed
        #update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """print bullet in screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)