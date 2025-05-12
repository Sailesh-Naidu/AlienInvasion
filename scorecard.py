import pygame.font

class Scorecard:
    """A class to display the scoring information"""

    def __init__(self, ai_game):
        """Initialize scorecard attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.status = ai_game.status

        #Font settings for scorecard information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        # prepare the initial score image
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """Turn the scorecard into a rendered image"""
        rounded_score = round(self.status.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,self.text_color,self.settings.bg_color)
        #Display the score on the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top =20

    def prep_high_score(self):
        """Turn the high score into rendered image"""
        high_score = round(self.status.high_score, -1)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check if the new score is high score"""
        if self.status.score > self.status.high_score:
            self.status.high_score = self.status.score
            self.prep_high_score()

    def show_score(self):
        """Display the score on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)


