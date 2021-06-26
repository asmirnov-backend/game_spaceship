import os
import random
from os import path
import pygame
import settings


powerup_images = {}
for img_name in os.listdir(settings.img_dir + '/PowerUps'):
    power_up_name = img_name.split('.')[0]
    powerup_images[power_up_name] = pygame.image.load(path.join(settings.img_dir + '/PowerUps', img_name)).convert_alpha()


powerup_group = pygame.sprite.Group()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(list(powerup_images))
        self.image = powerup_images[self.type]
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > settings.HEIGHT:
            self.kill()


def new_pow(plase_where_to_init):
    pow = Pow(plase_where_to_init)
    settings.all_sprites.add(pow)
    powerup_group.add(pow)
