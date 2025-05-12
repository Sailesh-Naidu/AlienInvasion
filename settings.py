class Settings:
    """A close to store all the settings."""

    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.ship_limit = 2
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        #self.bullets_allowed = 10
        #Alien settings
        self.fleet_drop_speed = 10
        #How quickly the game speeds up
        self.speedScale_up = 1.1
        #How quickly the point value increases
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self, level_speed =1 , level_bonus = 1):
        self.ship_speed = 1.5*level_speed
        self.bullet_speed = 2.5*level_speed
        self.alien_speed = 1.0*level_speed
        # fleet_direction of 1 represent right and -1 represents left
        self.fleet_direction = 1
        self.alien_score = int(50 * level_bonus)

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedScale_up
        self.bullet_speed *= self.speedScale_up
        self.alien_speed *= self.speedScale_up
        self.alien_score = int(self.alien_score * self.score_scale)
        print(self.alien_score)