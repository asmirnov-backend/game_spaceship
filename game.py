import pygame
import random
from os import path
import lvls
import mobs
import music
import player_kod
import powerup_kod
import settings
import draw_auxilary
import draw_screens


# Создаем игру и окно
pygame.init()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(settings.img_dir, filename)).convert()
    img.set_colorkey(settings.BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(settings.img_dir, filename)).convert()
    img.set_colorkey(settings.BLACK)
    explosion_anim['player'].append(img)


music.gromkost(0)

# Цикл игры
game_over = True
running = True
paused = False
current_lvl = 1

while running:
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused

    if not paused:
        # Держим цикл на правильной скорости
        settings.clock.tick(settings.FPS)

        if game_over:
            if current_lvl == 1:
                player, shield = lvls.make_lvl_1()
                game_over = False

            elif current_lvl == 2:
                player, shield = lvls.make_lvl_2()
                game_over = False

            elif current_lvl == 3:
                player, shield = lvls.make_lvl_3()
                game_over = False

            elif current_lvl - 1 == len(settings.score_for_next_lvl):
                draw_screens.show_win_screen()
                current_lvl = 1
                lvls.score = 0
                lvls.money = 0
                game_over = True

        # Обновление
        settings.all_sprites.update()

        # проверьте, не попала ли пуля в моб1
        hits = pygame.sprite.groupcollide(mobs.mobs1_group, player_kod.bullets_group, True, player.bullet_delete)
        for hit in hits:
            lvls.score += 50
            random.choice(music.expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            settings.all_sprites.add(expl)
            if random.random() > 0.9:
                powerup_kod.new_pow(hit.rect.center)
            mobs.newmob1()

        # проверьте, не попал ли пуля от моб2 или моб 3 в игрока
        hits = pygame.sprite.spritecollide(player, mobs.bullets_enemy_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.hp -= settings.enemy_damage
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)

        # проверьте, не попала ли пуля в моб2
        hits = pygame.sprite.groupcollide(mobs.mobs2_group, player_kod.bullets_group, True, player.bullet_delete)
        for hit in hits:
            lvls.score += 100
            random.choice(music.expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            settings.all_sprites.add(expl)
            if random.random() > 0.8:
                powerup_kod.new_pow(hit.rect.center)
            mobs.newmob2()

        # проверьте, не попала ли пуля в моб3
        hits = pygame.sprite.groupcollide(mobs.mobs3_group, player_kod.bullets_group, True, player.bullet_delete)
        for hit in hits:
            lvls.score += 200
            random.choice(music.expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            settings.all_sprites.add(expl)
            if random.random() > 0.7:
                powerup_kod.new_pow(hit.rect.center)
            mobs.newmob3()

        #  Проверка, не врезался ли моб1 в шит
        hits = pygame.sprite.spritecollide(shield, mobs.mobs1_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)
            shield.hp -= 1
            mobs.newmob1()

        #  Проверка, не врезался ли моб2 в шит
        hits = pygame.sprite.spritecollide(shield, mobs.mobs2_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)
            shield.hp -= 3
            mobs.newmob2()

        #  Проверка, не врезался ли моб3 в шит
        hits = pygame.sprite.spritecollide(shield, mobs.mobs3_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)
            shield.hp -= 3
            mobs.newmob3()

        #  Проверка, не врезалась ли пуля от моб2 или моб3 в шит
        hits = pygame.sprite.spritecollide(shield, mobs.bullets_enemy_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            shield.hp -= 1

        #  Проверка, не врезался ли моб1 игрока
        hits = pygame.sprite.spritecollide(player, mobs.mobs1_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.hp -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)
            mobs.newmob1()

        #  Проверка, не врезался ли моб2 игрока
        hits = pygame.sprite.spritecollide(player, mobs.mobs2_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.hp -= 50
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)
            mobs.newmob2()

        #  Проверка, не врезался ли моб3 игрока
        hits = pygame.sprite.spritecollide(player, mobs.mobs3_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.hp -= 50
            expl = Explosion(hit.rect.center, 'sm')
            settings.all_sprites.add(expl)
            mobs.newmob3()


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

        # Спавним мобов и улучшения с рандомной задержкой
        lvls.spawn_mobs_with_delay(current_lvl)


        # Если игрок набрал достаточно очков, переместить на след уровень
        if lvls.score >= settings.score_for_next_lvl[current_lvl - 1]:
            current_lvl += 1
            game_over = True
        # Если HP меньше нуля, то вычитаем одну жизнь
        if player.hp <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            settings.all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.hp = 100
            player.power_to_shoot = 100
        # Если игрок умер 3 раза, игра окончена
        if player.lives == 0 and not death_explosion.alive():
            game_over = True
            current_lvl = 1

        # Проверка на нажатие кнопок на клавиатуре
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    music.gromkost(settings.standart_volume)
                elif event.key == pygame.K_F2:
                    music.gromkost(0)

        # Рендеринг
        settings.screen.fill(settings.BLACK)
        settings.screen.blit(draw_screens.background, draw_screens.background_rect)
        settings.all_sprites.draw(settings.screen)
        draw_auxilary.draw_text("Score: " + str(lvls.score), 18, settings.WIDTH / 2 - 48, 10)
        draw_auxilary.draw_text("Money: " + str(lvls.money), 18, settings.WIDTH / 2 + 48, 10)
        draw_auxilary.draw_hp_bar(7, 5, player.hp)
        try:
            text = "Для победы в этом уровне наберите {} очков".format(settings.score_for_next_lvl[current_lvl - 1])
        except IndexError:
            text = "Вы победили так то"
        draw_auxilary.draw_text(text, 16, settings.WIDTH * 0.75, 10)
        draw_auxilary.draw_power_to_shoot(7, settings.HEIGHT * 0.055, player.power_to_shoot)
        draw_auxilary.draw_lives(settings.WIDTH - 100, 10, player.lives, player_kod.player_mini_img)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

pygame.quit()
