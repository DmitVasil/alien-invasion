from turtle import update
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Control for ship"""

    def __init__(self, ai_game):
        """Initializes ship and it original position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #load image of shop and get rectangle
        self.image = pygame.image.load('images/starship.bmp')
        self.rect = self.image.get_rect()
        #every new ship appears in the middle of bottom edge of screen
        self.rect.midbottom = self.screen_rect.midbottom
        #save the real part of ship center
        self.x = float(self.rect.x)
        #moving flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """update position of ship using flag"""
        #update the attribute X, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #update attribute rect using attr self.x
        self.rect.x = self.x

    def blitme(self):
        """draw the ship in the current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """place ship in the bottom center"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

