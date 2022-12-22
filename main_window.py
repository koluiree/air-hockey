import os
import sys

import pygame

FPS = 50
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
coords = {'start_game': (), 'settings': (), 'skins': (), 'rules': (), 'quit': ()}
Flag = 0


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


class StartScreen:
    def __init__(self, pos=(0, 0)):
        self.mouse_pos = pos

    def start_screen(self):
        intro_text = ["Начать игру",
                      "Настройки",
                      "Скины и прочее",
                      'Правила',
                      "Выход"]

        fon = pygame.transform.scale(load_image('sastavka_more.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 100
        for line, setting in zip(intro_text, coords):
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = WIDTH / 2 - 80
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            coords[setting] = intro_rect
        print(coords)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)

    def choice(self):
        if self.mouse_pos == coords['start_game']:
            print(4)
        elif self.mouse_pos == coords['settings']:
            print(3)
        elif self.mouse_pos == coords['skins']:
            print(2)
        elif self.mouse_pos == coords['quit']:
            print(1)


def switch_window(self):
    if Flag == 1:
        pass
        # okno igri
    elif Flag == 2:
        pass
        # okno menu skinov
    elif Flag == 3:
        pass
        # okno menu nastroek(rasmer okna tam ili eshe cho, svuk meibi(peoshe musiku postavit)
    elif Flag == 4:
        pass
        # okno dla pravil igri.....
    elif Flag == '':
        pass
        # and tak dalee


if __name__ == '__main__':
    pygame.init()
    running = True
    main_menu = StartScreen()
    while running:
        main_menu.start_screen()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu = StartScreen(event.pos)
