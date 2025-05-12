import sys
import pygame
from  settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from gameStats import GameStats
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        # Start the game in an inactive status
        self.game_active = False
        pygame.init()
        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1200,800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # Make the play button
        self.play_button = Button(self, "Start Game")
        self.level_1_button = Button(self, "Level 1",y_offset=60)
        self.level_2_button = Button(self,"Level 2", y_offset =120)
        self.level_3_button = Button(self,"Level 3", y_offset= 180)

        #create an instance to store the game stats
        self.status = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._check_fleet_edges()
                self._update_aliens()
            self._update_screen_()
            self.clock.tick(60)

    def _update_bullets(self):
        """Update the position of bullets on the screen"""
        self.bullets.update()
        #Remove the bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
            #print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """Update the position of all aliens on the screen and add new row if space available."""
        self.aliens.update()
        if self._can_add_new_row():
            self._create_fleet_row()
        # check if there is any collision between alien and the ship
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("Ship Hit!!!!")
        self._check_aliens_bottom()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos, key_clicked=None):
        """Start new game when the player presses start game button or selects a level"""
        level_map = {
            self.play_button: 1.0,
            self.level_1_button: 1.1,
            self.level_2_button: 1.3,
            self.level_3_button: 1.5,
        }
        # Handle mouse click
        for button, speed in level_map.items():
            if button.rect.collidepoint(mouse_pos) and not self.game_active:
                self._start_game(speed)
                return
        # Handle keyboard shortcut
        if key_clicked and not self.game_active:
            self._start_game(1.0)

    def _start_game(self, speed):
        """Centralized logic to start the game with a given speed."""
        self.status.reset_stats()
        self.settings.initialize_dynamic_settings(speed)
        self.game_active = True
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            # move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos,key_clicked=True)

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
        #if len(self.bullets) < self.settings.bullets_allowed:
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

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1


    def _update_screen_(self):
        """Update images to screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        if not self.game_active:
            self.play_button.draw_button()
            self.level_1_button.draw_button()
            self.level_2_button.draw_button()
            self.level_3_button.draw_button()
        pygame.display.flip()

    def _can_add_new_row(self):
        """Return True if there's space at the top to add a new row."""
        if not self.aliens:
            return True  # No aliens, so yes
        top_y = min(alien.rect.top for alien in self.aliens.sprites())
        alien = Alien(self)
        return top_y > 2 * alien.rect.height

    def _create_fleet_row(self):
        """Create a single new row of aliens above the current topmost row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x = alien_width
        if self.aliens:
            top_y = min(alien.rect.top for alien in self.aliens.sprites())
            current_y = top_y - 2 * alien_height  # Place 2*height above the highest alien
        else:
            current_y = 2 * alien_height  # Start higher if there are no aliens

        while current_x < (self.settings.screen_width - 2 * alien_width):
            self._create_alien(current_x, current_y)
            current_x += 2 * alien_width

    def _check_bullet_alien_collisions(self):
        """check if bullets have hit any aliens and if
           hits then remove the alien and the bullet"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # if all aliens destroyed then clear the bullets and create a new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _ship_hit(self):
        """Respond to the ship getting hit by the aliens and decrement on ship"""
        if self.status.ships_left >0:
            self.status.ships_left-=1
            #Get rid of remaining aliens and the bullets
            self.aliens.empty()
            self.bullets.empty()
            #create a new fleet
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if any alien reaches the bottom and if it removes
        the alien"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.aliens.remove(alien)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()




