import random
import pygame

import explosion
import lvls
import mobs
import music
import player_kod
import powerup_kod
import settings


def check_all_collides(player, shield):
    # проверьте, не попала ли пуля в моб1
    hits = pygame.sprite.groupcollide(mobs.mobs1_group, player_kod.bullets_group, True, player.bullet_delete)
    for hit in hits:
        lvls.score += 50
        random.choice(music.expl_sounds).play()
        expl = explosion.Explosion(hit.rect.center, 'lg')
        settings.all_sprites.add(expl)
        if random.random() > 0.9:
            powerup_kod.new_pow(hit.rect.center)
        mobs.new_mob_meteor()

    # проверьте, не попал ли пуля от моб2 или моб 3 в игрока
    hits = pygame.sprite.spritecollide(player, mobs.bullets_enemy_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= settings.enemy_damage
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)

    # проверьте, не попала ли пуля в моб2
    hits = pygame.sprite.groupcollide(mobs.mobs2_group, player_kod.bullets_group, True, player.bullet_delete)
    for hit in hits:
        lvls.score += 100
        random.choice(music.expl_sounds).play()
        expl = explosion.Explosion(hit.rect.center, 'lg')
        settings.all_sprites.add(expl)
        if random.random() > 0.8:
            powerup_kod.new_pow(hit.rect.center)
        mobs.new_mob_ship1()

    # проверьте, не попала ли пуля в моб3
    hits = pygame.sprite.groupcollide(mobs.mobs3_group, player_kod.bullets_group, True, player.bullet_delete)
    for hit in hits:
        lvls.score += 200
        random.choice(music.expl_sounds).play()
        expl = explosion.Explosion(hit.rect.center, 'lg')
        settings.all_sprites.add(expl)
        if random.random() > 0.7:
            powerup_kod.new_pow(hit.rect.center)
        mobs.new_mob_ship2()

    #  Проверка, не врезался ли моб1 в шит
    hits = pygame.sprite.spritecollide(shield, mobs.mobs1_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)
        shield.hp -= 1
        mobs.new_mob_meteor()

    #  Проверка, не врезался ли моб2 в шит
    hits = pygame.sprite.spritecollide(shield, mobs.mobs2_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)
        shield.hp -= 3
        mobs.new_mob_ship1()

    #  Проверка, не врезался ли моб3 в шит
    hits = pygame.sprite.spritecollide(shield, mobs.mobs3_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)
        shield.hp -= 3
        mobs.new_mob_ship2()

    #  Проверка, не врезалась ли пуля от моб2 или моб3 в шит
    hits = pygame.sprite.spritecollide(shield, mobs.bullets_enemy_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        shield.hp -= 1

    #  Проверка, не врезался ли моб1 игрока
    hits = pygame.sprite.spritecollide(player, mobs.mobs1_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= hit.radius * 2
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)
        mobs.new_mob_meteor()

    #  Проверка, не врезался ли моб2 игрока
    hits = pygame.sprite.spritecollide(player, mobs.mobs2_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= 50
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)
        mobs.new_mob_ship1()

    #  Проверка, не врезался ли моб3 игрока
    hits = pygame.sprite.spritecollide(player, mobs.mobs3_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.hp -= 50
        expl = explosion.Explosion(hit.rect.center, 'sm')
        settings.all_sprites.add(expl)
        mobs.new_mob_ship2()

    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerup_kod.powerup_group, True)
    for hit in hits:
        if hit.type == 'hp':
            player.hp += random.randrange(10, 30)
            if player.hp >= 100:
                player.hp = 100
        elif hit.type == 'gun':
            player.powerup()
        elif hit.type == 'power_for_shoot':
            player.power_to_shoot += random.randrange(10, 30)
            if player.power_to_shoot >= 100:
                player.power_to_shoot = 100
        elif hit.type == 'powerup_shield':
            shield.nohide = True
        elif hit.type == 'bullet_upgrade':
            player.bullet_upgrade_for_player()
        elif hit.type == 'money':
            lvls.money += 100
