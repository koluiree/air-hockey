import os
import sys

import pygame

FPS = 50
size = WIDTH, HEIGHT = 600, 800
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


def start_screen():
    intro_text = ["Начать игру",
                  "Настройки",
                  "Скины и прочее",
                  "Правила",
                  "Выход"]

    fon = pygame.transform.scale(load_image('menu.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line, setting in zip(intro_text, coords):
        string_rendered = font.render(line, 1, 'white')
        text_rect = string_rendered.get_rect()
        text_coord += 35
        text_rect.top = text_coord
        text_rect.x = WIDTH / 2 - 80
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)
        coords[setting] = text_rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                choice(event.pos)
        pygame.display.flip()
        clock.tick(FPS)


def choice(mouse_pos):
    if coords['start_game'].collidepoint(mouse_pos[0], mouse_pos[1]):
        pass
    elif coords['settings'].collidepoint(mouse_pos[0], mouse_pos[1]):
        pass
    elif coords['skins'].collidepoint(mouse_pos[0], mouse_pos[1]):
        pass
    elif coords['rules'].collidepoint(mouse_pos[0], mouse_pos[1]):
        rules(mouse_pos)
    elif coords['quit'].collidepoint(mouse_pos[0], mouse_pos[1]):
        terminate()


def rules(mouse_pos):
    rules = ("W, A, S, D - движение первого игрока",
             "Стрелки на клавиатуре - движение второго игрока",
             "Забейте шайбу в ворота противника, чтобы заработать очко",
             "Игра продолжается до 7 голов")

    fon = pygame.transform.scale(load_image('menu.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 29)
    font1 = pygame.font.Font(None, 30)
    text_coord = 200
    for line in rules:
        string_rendered = font.render(line, 1, 'white')
        string_rendered1 = font1.render(line, 1, 'black')

        text_rect = string_rendered.get_rect()
        text_coord += 30
        text_rect.top = text_coord
        text_rect.x = WIDTH / 2 - 300
        text_coord += text_rect.height
        screen.blit(string_rendered1, text_rect)
        screen.blit(string_rendered, text_rect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen()
        pygame.display.flip()
        clock.tick(FPS)


"""class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)"""


if __name__ == '__main__':
    pygame.init()
    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                choice(pos)
        pygame.display.flip()
        clock.tick(FPS)
