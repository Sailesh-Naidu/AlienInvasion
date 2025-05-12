import pygame.font


class Button:
    """Class to build button for the game"""
    def __init__(self, ai_game, msg, y_offset = 0):
        #iinitialize button attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set attributes for the button
        self.width, self.height = 200,50
        self.button_color = (0,135,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y +=y_offset

        # the button message needs to be prepped once.
        self._prep_msg(msg)

    def _prep_msg(self, message):
        """Render the text as an image and center text on the button"""
        self.msg_image = self.font.render(message,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button on the screen with a message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)