import sys
import pygame
from  settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1200,800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen_()
            self.clock.tick(60)

    def _update_bullets(self):
        """Update the position of bullets on the screen"""
        self.bullets.update()

    def _update_aliens(self):
        """Update the position of all aliens on the screen"""
        self.aliens.update()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            # move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self,event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create fleet of aliens"""
        #Make an alien
        #Draw an alien, alien width form each other
        row_offset=0
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y <(self.settings.screen_height - 3*alien_width):
            while current_x <(self.settings.screen_width - (2+row_offset)*alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            current_x = alien_width*(2+row_offset)
            row_offset+=1
            current_y += 2*alien_height

    def _create_alien(self, current_x,current_y):
        """create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)


    def _update_screen_(self):
        """Update images to screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()




