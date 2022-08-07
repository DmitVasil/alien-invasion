import pygame
from random import randint

class Star():
    """create star for game space"""

    def __init__(self, ai_game):
        """Initializes star and its original position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/star2.bmp')
        self.rect = self.image.get_rect()

        self.image.set_alpha(50)

        available_space_x = self.screen_rect.width - 2 * self.rect.width
        available_space_y = self.screen_rect.height - 2 * self.rect.height

        self.star_number = available_space_x // (2 * self.rect.width)
        self.row_number = available_space_y // (2 * self.rect.height)


    def blitme(self):
        """draw the ship in the current position"""
        #creation of star grid
        rand_num = randint(-10, 10)
        for row in range(self.row_number):
            for star_num in range(self.star_number):
                self.screen.blit(self.image, ((self.rect.width + 
                                    5 * self.rect.width * star_num + rand_num), 
                                    self.rect.height + 7 * self.rect.height * row))
