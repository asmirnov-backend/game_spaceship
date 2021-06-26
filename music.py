import pygame
from os import path
import settings

# Загрузка мелодий игры

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(path.join(settings.snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(settings.snd_dir, snd)))


def gromkost(volume):
    shoot_sound.set_volume(volume)
    for sound in expl_sounds:
        sound.set_volume(volume)
