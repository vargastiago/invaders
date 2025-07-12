import sys
import pygame
import random
from entities import Ship, Bullet, Invader, InvaderBullet
from ui import show_start_screen, show_game_over_screen

FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
INVADER_SHOOT_EVENT = pygame.USEREVENT + 1


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Invaders')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.invader_bullets = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()

        self.invaders_direction = 1
        self.invaders_speed = 10
        self.score = 0
        self.game_active = True

        pygame.time.set_timer(INVADER_SHOOT_EVENT, 800)

        self.create_invaders()

    def run(self):
        show_start_screen(self)
        while True:
            self.check_events()
            if self.game_active:
                self.update_game()
            else:
                show_game_over_screen(self)
                self.reset_game()

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self.ship.shoot()
                elif event.key == pygame.K_q:
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
            elif event.type == INVADER_SHOOT_EVENT:
                self.invader_shoot()

    def update_game(self):
        self.ship.update()
        self.update_bullets()
        self.update_invader_bullets()
        self.update_invaders()

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def update_invader_bullets(self):
        self.invader_bullets.update()
        for bullet in self.invader_bullets.copy():
            if bullet.rect.top >= SCREEN_HEIGHT:
                self.invader_bullets.remove(bullet)
            elif bullet.rect.colliderect(self.ship.rect):
                self.game_active = False

    def update_invaders(self):
        self.check_invaders_edge()
        self.invaders.update()

        collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, True, True)
        if collisions:
            self.explosion_sound.play()
            for hit_list in collisions.values():
                self.score += len(hit_list) * 10

        if not self.invaders:
            self.bullets.empty()
            self.invaders_speed += 3
            self.create_invaders()

        if pygame.sprite.spritecollideany(self.ship, self.invaders):
            self.game_active = False

        for invader in self.invaders.sprites():
            if invader.rect.bottom >= SCREEN_HEIGHT:
                self.game_active = False

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.ship.draw()
        self.invaders.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw()
        for bullet in self.invader_bullets:
            bullet.draw()
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def create_invaders(self):
        invader = Invader(self)
        invader_width, invader_height = invader.rect.size
        x, y = invader_width, invader_height
        while y < (SCREEN_HEIGHT - 5 * invader_height):
            while x < (SCREEN_WIDTH - 2 * invader_width):
                invader = Invader(self)
                invader.rect.x = x
                invader.rect.y = y
                self.invaders.add(invader)
                x += 2 * invader_width
            x = invader_width
            y += 2 * invader_height

    def check_invaders_edge(self):
        for invader in self.invaders.sprites():
            if (
                invader.rect.right > self.screen.get_rect().right
                or invader.rect.left <= 0
            ):
                for invader in self.invaders.sprites():
                    invader.rect.y += self.invaders_speed
                self.invaders_direction *= -1
                break

    def invader_shoot(self):
        if self.invaders:
            shooter = random.choice(self.invaders.sprites())
            self.invader_bullets.add(InvaderBullet(self, shooter.rect))

    def reset_game(self):
        self.ship = Ship(self)
        self.bullets.empty()
        self.invaders.empty()
        self.invader_bullets.empty()
        self.invaders_direction = 1
        self.invaders_speed = 10
        self.score = 0
        self.game_active = True
        self.create_invaders()
