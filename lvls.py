import random
import pygame
import draw_screens
import mobs
import player_kod
import powerup_kod
import settings

# данные уровня
money = 0
score = 0


def update_all_groups():
    settings.all_sprites = pygame.sprite.Group()
    mobs.mobs1_group = pygame.sprite.Group()
    mobs.mobs2_group = pygame.sprite.Group()
    mobs.mobs3_group = pygame.sprite.Group()
    mobs.bullets_enemy_group = pygame.sprite.Group()
    player_kod.bullets_group = pygame.sprite.Group()


def make_lvl_1():
    update_all_groups()
    draw_screens.show_go_screen()
    pygame.mouse.set_visible(False)
    player = player_kod.new_player()
    shield = player_kod.new_shield(player)
    for i in range(15):
        mobs.new_mob_meteor()
    mobs.new_mob_ship2()
    return player, shield


def make_lvl_2():
    update_all_groups()
    draw_screens.show_lvl1end_screen()
    pygame.mouse.set_visible(False)
    player = player_kod.new_player()
    shield = player_kod.new_shield(player)
    for i in range(5):
        mobs.new_mob_meteor()
    return player, shield


def make_lvl_3():
    update_all_groups()
    draw_screens.show_lvl2end_screen()
    pygame.mouse.set_visible(False)
    player = player_kod.new_player()
    shield = player_kod.new_shield(player)
    for i in range(16):
        mobs.new_mob_meteor()
    for i in range(2):
        mobs.new_mob_ship1()
    return player, shield


# Спавним мобов и улучшения с рандомной задержкой
def spawn_mobs_with_delay(current_lvl):
    if current_lvl == 2 and len(mobs.mobs2_group) < settings.lvl2_mob2 and random.random() > 0.99:
        mobs.new_mob_ship1()
    if current_lvl == 3 and len(mobs.mobs2_group) < settings.lvl3_mob2 and random.random() > 0.99:
        mobs.new_mob_ship1()
    if current_lvl == 3 and len(mobs.mobs3_group) < settings.lvl3_mob3 and random.random() > 0.99:
        mobs.new_mob_ship2()
    if random.random() > 0.997:
        powerup_kod.new_pow((random.randint(100, settings.WIDTH - 100), -100))
