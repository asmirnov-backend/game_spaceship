import random
import pygame
from os import path
import settings


meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_tiny2.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
mob2_list = ["enemyBlack1.png", "enemyBlack2.png", "enemyBlack3.png", "enemyBlack4.png", "enemyBlack5.png"]
mob3_list = ["enemyBlue1.png", "enemyBlue2.png", "enemyBlue3.png", "enemyBlue4.png", "enemyBlue5.png"]
mob2_images = []
mob3_images = []
bullet_enemy_img = pygame.image.load(path.join(settings.img_dir, "laserBlue03.png")).convert()
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(settings.img_dir, img)).convert())
for img in mob2_list:
    mob2_images.append(pygame.transform.scale(pygame.image.load(path.join(settings.img_dir, img)).convert(), (50, 40)))
for img in mob3_list:
    mob3_images.append(pygame.transform.scale(pygame.image.load(path.join(settings.img_dir, img)).convert(), (50, 40)))


mobs1_group = pygame.sprite.Group()
mobs2_group = pygame.sprite.Group()
mobs3_group = pygame.sprite.Group()
bullets_enemy_group = pygame.sprite.Group()


def newmob1():
    m = Mob1()
    settings.all_sprites.add(m)
    mobs1_group.add(m)


def newmob2():
    m = Mob2()
    settings.all_sprites.add(m)
    mobs2_group.add(m)


def newmob3():
    m = Mob3()
    settings.all_sprites.add(m)
    mobs3_group.add(m)


class Mob1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(settings.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > settings.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > settings.WIDTH + 20:
            self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)


class Mob2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mob2_images)
        self.image_orig.set_colorkey(settings.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 1.5
        self.last_update = pygame.time.get_ticks()
        self.last_shot = 500
        self.shoot_delay = 1000

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > settings.HEIGHT + 10:
            self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

    def shoot(self):
        bullet = Bullet_enemy(self.rect.centerx, self.rect.bottom + 23)
        settings.all_sprites.add(bullet)
        bullets_enemy_group.add(bullet)


class Mob3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mob3_images)
        self.image_orig.set_colorkey(settings.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 1.5
        self.speedx = random.choice((1.5, -1.5))
        self.last_update = pygame.time.get_ticks()
        self.last_shot = 500
        self.shoot_delay = 1000

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > settings.HEIGHT + 20:
            self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedx = random.choice((1.5, -1.5))
        if self.rect.left < -20 or self.rect.right > settings.WIDTH + 20:
            self.speedx = - self.speedx

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

    def shoot(self):
        bullet = Bullet_enemy(self.rect.centerx, self.rect.bottom + 23)
        settings.all_sprites.add(bullet)
        bullets_enemy_group.add(bullet)


class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_enemy_img
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 7

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за нижнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


