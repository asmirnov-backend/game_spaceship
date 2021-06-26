import pygame
import check_collide
import effects
import lvls
import music
import player_kod
import settings
import draw_auxilary
import draw_screens


# Создаем игру и окно
pygame.init()

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

        # Проверки столкновений
        check_collide.check_all_collides(player, shield)

        # Спавним мобов и улучшения с рандомной задержкой
        lvls.spawn_mobs_with_delay(current_lvl)


        # Если игрок набрал достаточно очков, переместить на след уровень
        if lvls.score >= settings.score_for_next_lvl[current_lvl - 1]:
            current_lvl += 1
            game_over = True
        # Если HP меньше нуля, то вычитаем одну жизнь
        if player.hp <= 0:
            death_explosion = effects.Explosion(player.rect.center, 'player')
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
