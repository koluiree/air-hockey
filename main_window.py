import os
import sys

import pygame

FPS = 50
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
coords = {'start_game': (), 'settings': (), 'skins': (), 'rules': (), 'quit': ()}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print(f"Файл с изображением '{fullname}' не найден")
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(mouse_pos):
    intro_text = ["Начать игру",
                  "Настройки",
                  "Скины и прочее",
                  "Правила",
                  "Выход"]

    fon = pygame.transform.scale(load_image('sastavka_more.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line, setting in zip(intro_text, coords):
        string_rendered = font.render(line, 1, 'white')
        text_rect = string_rendered.get_rect()
        text_coord += 30
        text_rect.top = text_coord
        text_rect.x = WIDTH / 2 - 80
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)
        coords[setting] = text_rect


def choice(mouse_pos):
    # print(mouse_pos)
    # print(True if coords['start_game'].collidepoint(mouse_pos[0], mouse_pos[1]) else False)
    if coords['start_game'].collidepoint(mouse_pos[0], mouse_pos[1]):
        switch_window()
    elif coords['settings'].collidepoint(mouse_pos[0], mouse_pos[1]):
        switch_window()
    elif coords['skins'].collidepoint(mouse_pos[0], mouse_pos[1]):
        switch_window()
    elif coords['rules'].collidepoint(mouse_pos[0], mouse_pos[1]):
        switch_window()
    elif coords['quit'].collidepoint(mouse_pos[0], mouse_pos[1]):
        terminate()


def switch_window():
    pass


if __name__ == '__main__':
    pygame.init()
    running = True
    while running:
        start_screen(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                choice(pos)
        pygame.display.flip()
        clock.tick(FPS)
