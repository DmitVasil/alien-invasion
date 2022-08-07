import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """one alien class"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #load alien image and assign attribute rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #every new alien appears in left top corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #save precise horizontal position of alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """return True if alien is near of screen edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move alien to the right"""
        self.x += (self.settings.alien_speed * 
                        self.settings.fleet_direction)
        self.rect.x = self.x
