import pygame
import settings
font_name = pygame.font.match_font('arial')


def draw_text_button(text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, settings.BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    settings.screen.blit(text_surface, text_rect)


def draw_text(text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, settings.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    settings.screen.blit(text_surface, text_rect)


def draw_hp_bar(x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = settings.WIDTH / 6
    BAR_HEIGHT = settings.HEIGHT / 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(settings.screen, settings.GREEN, fill_rect)
    pygame.draw.rect(settings.screen, settings.WHITE, outline_rect, 4)


def draw_power_to_shoot(x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = settings.WIDTH / 6
    BAR_HEIGHT = settings.HEIGHT / 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(settings.screen, (188, 0, 20), fill_rect)
    pygame.draw.rect(settings.screen, settings.WHITE, outline_rect, 4)


def draw_lives(x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        settings.screen.blit(img, img_rect)
