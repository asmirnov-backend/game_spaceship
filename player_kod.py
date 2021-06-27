import os
import random
from os import path
import pygame
import settings
import music


# Загрузка игровой графики
player_img = pygame.image.load(path.join(settings.img_dir + '/player', random.choice(os.listdir(settings.img_dir + '/player')))).convert()
shield_img = pygame.image.load(path.join(settings.img_dir, "shield1.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(settings.BLACK)
bullet_img = pygame.image.load(path.join(settings.img_dir, "laserRed16.png")).convert()
bullet_upgrade_img = pygame.image.load(path.join(settings.img_dir, "laserGreen10.png")).convert()
bullets_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = settings.WIDTH / 2
        self.rect.bottom = settings.HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.hp = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.bullet_upgrade = 0
        self.bullet_delete = True
        self.bullet_upgrade_time = pygame.time.get_ticks()
        self.power_to_shoot = 100
        self.bullet_img = bullet_img

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > settings.POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.bullet_upgrade >= 1 and pygame.time.get_ticks() - self.bullet_upgrade_time > settings.POWERUP_TIME:
            self.bullet_upgrade -= 1
            self.bullet_upgrade_time = pygame.time.get_ticks()

        if self.bullet_upgrade >= 1:
            self.bullet_delete = False
        else:
            self.bullet_delete = True

            # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2500:
            self.hidden = False
            self.rect.centerx = settings.WIDTH / 2
            self.rect.bottom = settings.HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -settings.player_speed
        if keystate[pygame.K_d]:
            self.speedx = settings.player_speed
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > settings.WIDTH:
            self.rect.right = settings.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.speedy = 0
        if keystate[pygame.K_w]:
            self.speedy = -settings.player_speed
        if keystate[pygame.K_s]:
            self.speedy = settings.player_speed
        self.rect.y += self.speedy
        if self.rect.bottom > settings.HEIGHT and not self.hidden:
            self.rect.bottom = settings.HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def bullet_upgrade_for_player(self):
        self.bullet_upgrade += 1
        self.bullet_img = bullet_upgrade_img
        self.bullet_upgrade_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and self.power_to_shoot > 0:
            self.last_shot = now
            self.power_to_shoot -= settings.energy_for_shoot

            if self.bullet_upgrade == 0:
                self.bullet_img = bullet_img

            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_img)
                settings.all_sprites.add(bullet)
                bullets_group.add(bullet)
                music.shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, self.bullet_img)
                bullet2 = Bullet(self.rect.right, self.rect.centery, self.bullet_img)
                settings.all_sprites.add(bullet1)
                settings.all_sprites.add(bullet2)
                bullets_group.add(bullet1)
                bullets_group.add(bullet2)
                music.shoot_sound.play()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (settings.WIDTH * 2, settings.HEIGHT * 3)


class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shield_img, (70, 50))
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 32
        self.hp = 3
        self.nohide = False
        self.player = player
        self.rect.centerx = settings.WIDTH * 2
        self.rect.bottom = settings.HEIGHT
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        if self.nohide:
            self.rect.centerx = self.player.rect.centerx
            self.rect.bottom = self.player.rect.top + 30
        if self.hp <= 0:
            self.rect.centerx = settings.WIDTH * 20
            self.rect.bottom = settings.HEIGHT
            self.nohide = False
            self.hp = 3


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_imge):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_imge
        self.bullet_delete = True
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


def new_player():
    player = Player()
    settings.all_sprites.add(player)
    return player


def new_shield(player):
    shield = Shield(player)
    settings.all_sprites.add(shield)
    return shield


