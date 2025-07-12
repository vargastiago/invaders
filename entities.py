import pygame
from pygame.sprite import Sprite

MAX_BULLETS = 3


class Ship:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = game.screen.get_rect().midbottom
        self.moving_right = False
        self.moving_left = False
        self.speed = 5

    def update(self):
        if self.moving_right and self.rect.right < self.game.screen.get_rect().right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def shoot(self):
        if len(self.game.bullets) < MAX_BULLETS:
            self.game.bullets.add(Bullet(self.game))
            self.game.shoot_sound.play()


class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.color = (255, 15, 15)
        self.speed = 5
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midtop = game.ship.rect.midtop

    def update(self):
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)


class Invader(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.speed = 2.0
        self.image = pygame.image.load('images/invader.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def update(self):
        self.rect.x += self.speed * self.game.invaders_direction


class InvaderBullet(Sprite):
    def __init__(self, game, invader_rect):
        super().__init__()
        self.game = game
        self.color = (0, 255, 0)
        self.speed = 4
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midtop = invader_rect.midbottom

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)
