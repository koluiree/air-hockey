import os
import sys
import pygame
import gameplay

FPS = 100
size = WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode(size)
coords = {'start_game': (), 'settings': (), 'skins': (), 'rules': (), 'quit': (), 'difficulty': ()}
difffficult_to_c = {'Easy': (), 'Medium': (), "Hardcore": ()}
clock = pygame.time.Clock()
diff = 'hardcore'


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


def difficulty():
    intro_text = ["Легко  :)",
                  "Средне :/",
                  "ТЯЯЖКО >;(",
                  ]

    fon = pygame.transform.scale(load_image('menu.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line, difficultyy in zip(intro_text, difffficult_to_c):
        string_rendered = font.render(line, 1, 'white')
        text_rect = string_rendered.get_rect()
        text_coord += 35
        text_rect.top = text_coord
        text_rect.x = WIDTH / 2 - 80
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)
        difffficult_to_c[difficultyy] = text_rect
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                choice_of_difficulty(event.pos)
                start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def choice_of_difficulty(mouse_pos):
    global diff
    if difffficult_to_c['Easy'].collidepoint(mouse_pos[0], mouse_pos[1]):
        diff = 'Easy'
    if difffficult_to_c['Medium'].collidepoint(mouse_pos[0], mouse_pos[1]):
        diff = 'Medium'
    if difffficult_to_c['Hardcore'].collidepoint(mouse_pos[0], mouse_pos[1]):
        diff = 'Hardcore'


def choice(mouse_pos):
    if coords['start_game'].collidepoint(mouse_pos[0], mouse_pos[1]):
        gameplay.game()
    elif coords['settings'].collidepoint(mouse_pos[0], mouse_pos[1]):
        difficulty(mouse_pos)
    elif coords['skins'].collidepoint(mouse_pos[0], mouse_pos[1]):
        pass
    elif coords['rules'].collidepoint(mouse_pos[0], mouse_pos[1]):
        rules(mouse_pos)
    elif coords['quit'].collidepoint(mouse_pos[0], mouse_pos[1]):
        terminate()


def rules():
    rules = ("W, A, S, D - движение первого игрока",
             "Стрелки на клавиатуре - движение второго игрока",
             "Забейте шайбу в ворота противника, чтобы заработать очко",
             "Игра продолжается до 7 голов")

    fon = pygame.transform.scale(load_image('menu.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 29)
    text_coord = 100
    for line in rules:
        string_rendered = font.render(line, 1, 'yellow4')
        text_rect = string_rendered.get_rect()
        text_coord += 70
        text_rect.top = text_coord
        text_rect.x = WIDTH / 2 - 300
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen()
        pygame.display.flip()
        clock.tick(FPS)


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
