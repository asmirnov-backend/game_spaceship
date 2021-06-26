import pygame
import draw_auxilary
import settings
from os import path

background = pygame.image.load(path.join(settings.img_dir, "sky3.jpg")).convert()
background_rect = background.get_rect()
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
        settings.screen.blit(self.image_button, self.rect)
        draw_auxilary.draw_text_button(text, 27, self.rect.centerx, self.rect.top + 2)


def show_go_screen():
    settings.screen.blit(background_main_menu, background_main_menu.get_rect())
    button1 = Button("Старт", settings.WIDTH / 2, settings.HEIGHT / 2)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if button1.rect.collidepoint(x, y):
                    waiting = False



def show_lvl1end_screen():
    settings.screen.blit(background, background_rect)
    draw_auxilary.draw_text("Первый уровень пройден!!!!", 36, settings.WIDTH / 2, settings.HEIGHT / 4)
    draw_auxilary.draw_text("Умничка!!!", 22, settings.WIDTH / 2, settings.HEIGHT / 2)
    draw_auxilary.draw_text("Нажми на абсолютно любую клавишу", 18, settings.WIDTH / 2, settings.HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    time_end = pygame.time.get_ticks()
    while waiting:
        settings.clock.tick(settings.FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
            if event.type == pygame.KEYUP and pygame.time.get_ticks() - time_end > 1500:
                waiting = False


def show_lvl2end_screen():
    settings.screen.blit(background, background_rect)
    draw_auxilary.draw_text("Второй уровень пройден!!!!", 36, settings.WIDTH / 2, settings.HEIGHT / 4)
    draw_auxilary.draw_text("Умничка!!!", 22, settings.WIDTH / 2, settings.HEIGHT / 2)
    draw_auxilary.draw_text("Нажми на абсолютно любую клавишу", 18, settings.WIDTH / 2, settings.HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    time_end = pygame.time.get_ticks()
    while waiting:
        settings.clock.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP and pygame.time.get_ticks() - time_end > 1500:
                waiting = False


def show_win_screen():
    settings.screen.blit(background_menu, background_menu.get_rect())
    draw_auxilary.draw_text("Ты прошёл игру!!!!", 64, settings.WIDTH / 2, settings.HEIGHT / 4)
    draw_auxilary.draw_text("Поздравляем!!!", 22, settings.WIDTH / 2, settings.HEIGHT / 2)
    draw_auxilary.draw_text("Нажми на абсолютно любую клавишу", 18, settings.WIDTH / 2, settings.HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    time_end = pygame.time.get_ticks()
    while waiting:
        settings.clock.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP and pygame.time.get_ticks() - time_end > 1500:
                waiting = False