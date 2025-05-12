class GameStats:
    """Track the statistics of the game"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize the statistics which are update through the game"""
        self.ships_left = self.settings.ship_limit
