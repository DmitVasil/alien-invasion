import pygame

class Button():

    def __init__(self, ai_game, msg):
        """Initializes button parameters"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #assigment of size and properties of buttons
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #creation of RECT object for button and alingment it nio center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #message of button create only one time
        self._prep_message(msg)

    def _prep_message(self, msg):
        """transform message in rectangle and center it"""
        self.msg_image = self.font.render(msg, True, self.text_color, 
                                    self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """display empty button and message output"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
