import pygame
import draw_auxilary
import lvls
import settings
from os import path

background = pygame.image.load(path.join(settings.img_dir, "sky3.jpg")).convert()
background_rect = background.get_rect()
background_shop_large = pygame.image.load(path.join(settings.img_dir, "shop_back.jpg")).convert()
background_shop = pygame.transform.scale(background_shop_large, (settings.WIDTH, settings.HEIGHT))
background_shop_rect = background_shop.get_rect()
background_menu = pygame.image.load(path.join(settings.img_dir, "sky2.jpg")).convert()
background_main_menu = pygame.image.load(path.join(settings.img_dir, "sky3t.jpg")).convert()
background_win = pygame.image.load(path.join(settings.img_dir, "purple.png")).convert()
background_rect_win = background_win.get_rect()
button_img = pygame.image.load(path.join(settings.img_dir, "buttonGreen.png")).convert()


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_button = button_img  # Загружаем изображение исходной кнопки
        #self.image_button = pygame.transform.scale(player_img, (50, 38)) # Изменяем размер
        self.rect = self.image_button.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.colour = (64, 128, 255)
        self.is_drawn = False
        self.pos_for_draw_vadelenie = (self.rect.left, self.rect.top, self.rect.width, self.rect.height)
        settings.screen.blit(self.image_button, self.rect)
        draw_auxilary.draw_text_button(text, 27, self.rect.centerx, self.rect.top + 2)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if self.rect.collidepoint(x, y):
                    pygame.draw.rect(settings.screen, self.colour, self.pos_for_draw_vadelenie, 3)
                    pygame.display.update()
                    self.is_drawn = True
                elif self.is_drawn:
                    pygame.draw.rect(settings.screen, settings.WHITE, self.pos_for_draw_vadelenie, 3)
                    pygame.display.update()
                    self.is_drawn = False


def show_go_screen():
    pygame.mouse.set_visible(True)
    settings.screen.blit(background_main_menu, background_main_menu.get_rect())
    button_exit = Button("Выход", settings.WIDTH / 2, settings.HEIGHT / 2 + 50)
    button_start = Button("Старт", settings.WIDTH / 2, settings.HEIGHT / 2)
    draw_auxilary.draw_text("Игруха от Андрюхи!", 64, settings.WIDTH / 2, settings.HEIGHT / 4)
    draw_auxilary.draw_text("WASD для управления, пробел для стрельбы", 22, settings.WIDTH / 2, settings.HEIGHT * 0.7)
    draw_auxilary.draw_text("F2 - для отключения звука", 22, settings.WIDTH / 2, settings.HEIGHT * 0.7 + 25)
    draw_auxilary.draw_text("F1 - для включения звука", 22, settings.WIDTH / 2, settings.HEIGHT * 0.7 + 50)
    draw_auxilary.draw_text("ESC - для выключения игры", 22, settings.WIDTH / 2, settings.HEIGHT * 0.7 + 75)
    draw_auxilary.draw_text("P - для паузы", 22, settings.WIDTH / 2, settings.HEIGHT * 0.7 + 100)
    draw_auxilary.draw_text("Весёлой игры!", 18, settings.WIDTH / 2, settings.HEIGHT * 0.93)
    pygame.display.flip()
    waiting = True

    while waiting:
        settings.clock.tick(settings.FPS)
        events = pygame.event.get()
        button_start.update(events)  # Обновление
        button_exit.update(events)
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    waiting = False
                elif button_exit.rect.collidepoint(x, y):
                    pygame.quit()


def show_lvl_end_screen():
    pygame.mouse.set_visible(True)
    settings.screen.blit(background, background_rect)
    button_continue = Button("Продолжить", settings.WIDTH / 2, settings.HEIGHT / 2)
    button_shop = Button("Магазин", settings.WIDTH / 2, settings.HEIGHT / 2 + 50)
    button_exit = Button("Выход", settings.WIDTH / 2, settings.HEIGHT / 2 + 100)
    draw_auxilary.draw_text("Уровень пройден!!!!", 36, settings.WIDTH / 2, settings.HEIGHT / 4)
    draw_auxilary.draw_text("Умничка!!!", 22, settings.WIDTH / 2, settings.HEIGHT / 2.5)
    pygame.display.flip()
    waiting = True
    time_end = pygame.time.get_ticks()
    while waiting:
        settings.clock.tick(settings.FPS)
        events = pygame.event.get()
        button_continue.update(events)  # Обновление
        button_shop.update(events)
        button_exit.update(events)
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE and pygame.time.get_ticks() - time_end > 1500:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button_continue.rect.collidepoint(x, y):
                    waiting = False
                elif button_shop.rect.collidepoint(x, y):
                    show_shop()
                elif button_exit.rect.collidepoint(x, y):
                    pygame.quit()


def show_win_screen():
    pygame.mouse.set_visible(True)
    settings.screen.blit(background_menu, background_menu.get_rect())
    button_main_menu = Button("Главное меню", settings.WIDTH / 2, settings.HEIGHT / 2 + 50)
    button_exit = Button("Выход", settings.WIDTH / 2, settings.HEIGHT / 2 + 100)
    draw_auxilary.draw_text("Ты прошёл игру!!!!", 64, settings.WIDTH / 2, settings.HEIGHT / 4)
    draw_auxilary.draw_text("Поздравляем!!!", 22, settings.WIDTH / 2, settings.HEIGHT / 1.3)
    pygame.display.flip()
    waiting = True
    while waiting:
        events = pygame.event.get()
        settings.clock.tick(settings.FPS)
        button_exit.update(events)
        button_main_menu.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button_exit.rect.collidepoint(x, y):
                    pygame.quit()
                elif button_main_menu.rect.collidepoint(x, y):
                    waiting = False


def show_shop():
    pygame.mouse.set_visible(True)
    settings.screen.blit(background_shop, background_shop_rect)
    draw_auxilary.draw_text("Score: " + str(lvls.score), 18, settings.WIDTH / 2 - 48, 20)
    draw_auxilary.draw_text("Money: " + str(lvls.money), 18, settings.WIDTH / 2 + 48, 20)
    button_continue = Button("Продолжить", settings.WIDTH / 2, settings.HEIGHT / 2)
    button_up_energy_for_shoot = Button("В 2 раза уменьшить потребление энергии за выстрел за 100", settings.WIDTH / 2, settings.HEIGHT / 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        events = pygame.event.get()
        settings.clock.tick(settings.FPS)
        button_continue.update(events)
        button_up_energy_for_shoot.update(events)
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button_continue.rect.collidepoint(x, y):
                    waiting = False
                elif button_up_energy_for_shoot.rect.collidepoint(x, y):
                    if lvls.money >= 100:
                        settings.energy_for_shoot = 1
                        lvls.money -= 100
