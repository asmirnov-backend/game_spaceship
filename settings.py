from os import path
import pygame


# Заданная сложность типо
score_for_next_lvl = [250, 300, 500]
enemy_damage = 25
lvl2_mob2 = 4
lvl3_mob2 = 3
lvl3_mob3 = 4

WIDTH = 1280
HEIGHT = 720
FPS = 60

standart_volume = 0.15  # Громкость

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  #pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Game by Andrew")
clock = pygame.time.Clock()

# Улучшения коробля космического
POWERUP_TIME = 5000
energy_for_shoot = 2
player_speed = 7

all_sprites = pygame.sprite.Group()
