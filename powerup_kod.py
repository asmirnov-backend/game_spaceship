import random
from os import path
import pygame
import settings


powerup_images = {}
powerup_images['hp'] = pygame.image.load(path.join(settings.img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(settings.img_dir, 'bolt_gold.png')).convert()
powerup_images['power_for_shoot'] = pygame.image.load(path.join(settings.img_dir, 'bolt_bronze.png')).convert()
powerup_images['powerup_shield'] = pygame.image.load(path.join(settings.img_dir, 'powerupBlue_shield.png')).convert()
powerup_images["bullet_upgrade"] = pygame.image.load(path.join(settings.img_dir, 'bolt_green.png')).convert()
powerup_images["money"] = pygame.image.load(path.join(settings.img_dir, 'money1.png')).convert()


powerup_group = pygame.sprite.Group()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'gun', "power_for_shoot", "powerup_shield", "bullet_upgrade", 'money'])
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
