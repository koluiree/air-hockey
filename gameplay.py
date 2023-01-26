import os

from pygame.locals import *
import pygame
import main_menu

FPS = 50
size = WIDTH, HEIGHT = 600, 800
STEP = 10
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
puck_vel = 0
player1_point = 0
player2_point = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Border(pygame.sprite.Sprite):
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
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Goal2(pygame.sprite.Sprite):  # ворота верхнего игрока
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(goal2_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(goal2_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Goal1(pygame.sprite.Sprite):  # ворота нижнего игрока
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(goal1_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(goal1_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Puck(pygame.sprite.Sprite):  # класс шайбы
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.radius = radius
        self.radius = radius
        self.image = pygame.transform.scale(load_image('puck.png', colorkey=-1), (70, 70))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.difficulty = main_menu.diff
        self.vx = 4
        self.vy = 4


    def update(self):
        global player2_point, player1_point
        if main_menu.diff == 'Easy':
            self.vx = 2 if self.vx > 0 else -2
            self.vy = 2 if self.vy > 0 else -2
        elif main_menu.diff == 'Medium':
            self.vx = 3 if self.vx > 0 else -3
            self.vy = 3 if self.vy > 0 else -3
        elif main_menu.diff == 'Hardcore':
            self.vx = 4 if self.vx > 0 else -4
            self.vy = 4 if self.vy > 0 else -4
        self.rect = self.rect.move(self.vx, self.vy)
        print(main_menu.diff, self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

        if pygame.sprite.spritecollideany(self, pad1_group):
            if abs(self.rect.centerx - pad1.rect.centerx) >= 68:
                self.vx = -self.vx
            else:
                self.rect.centerx += 2 if self.vx < 0 else -2
            if abs(self.rect.centery - pad1.rect.centery) >= 68:
                self.vy = -self.vy
            else:
                self.rect.centery += 2 if self.vy < 0 else -2

        if pygame.sprite.spritecollideany(self, pad2_group):
            if abs(self.rect.centerx - pad2.rect.centerx) >= 68:
                self.vx = -self.vx
            else:
                self.rect.centerx += 2 if self.vx < 0 else -2
            if abs(self.rect.centery - pad2.rect.centery) >= 68:
                self.vy = -self.vy
            else:
                self.rect.centery += 2 if self.vy < 0 else -2

        if pygame.sprite.spritecollideany(self, goal2_group):
            player1_point += 1  # очко нижнему игроку
            self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
            print(player1_point)
        if pygame.sprite.spritecollideany(self, goal1_group):
            player2_point += 1  # очко верхнему игроку
            self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
            print(player2_point)


class Pad1(pygame.sprite.Sprite):  # нижний игрок
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(pad1_group)
        self.radius = radius
        self.image = pygame.transform.scale(load_image('pad.png', colorkey=-1), (70, 70))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.paddle1_vel = 0
        self.event_key = None

    def keydown(self, event):
        if event.key == K_UP:
            self.paddle1_vel = -4
        elif event.key == K_DOWN:
            self.paddle1_vel = 4
        elif event.key == K_LEFT:
            self.paddle1_vel = -4
        elif event.key == K_RIGHT:
            self.paddle1_vel = 4
        self.event_key = event.key
        self.update()

    def keyup(self, event):
        if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
            self.paddle1_vel = 0

    def update(self):
        if self.event_key == K_UP and self.rect.y >= HEIGHT / 2:
            self.rect.y += self.paddle1_vel
        elif self.event_key == K_LEFT and self.rect.x >= 25:
            self.rect.x += self.paddle1_vel
        elif self.event_key == K_DOWN and self.rect.y + 74 <= 780:
            self.rect.y += self.paddle1_vel
        elif self.event_key == K_RIGHT and self.rect.x + 74 <= 580:
            self.rect.x += self.paddle1_vel


class Pad2(pygame.sprite.Sprite):  # верхний игрок
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(pad2_group)
        self.radius = radius
        self.image = pygame.transform.scale(load_image('pad.png', colorkey=-1), (70, 70))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.paddle2_vel = 0
        self.event_key = None

    def keydown(self, event):
        if event.key == K_w:
            self.paddle2_vel = -4
        elif event.key == K_s:
            self.paddle2_vel = 4
        elif event.key == K_a:
            self.paddle2_vel = -4
        elif event.key == K_d:
            self.paddle2_vel = 4

        self.event_key = event.key
        self.update()

    def keyup(self, event):
        if event.key in (K_w, K_s, K_a, K_d):
            self.paddle2_vel = 0

    def update(self):
        if self.event_key == K_w and self.rect.y >= 20:
            self.rect.y += self.paddle2_vel
        elif self.event_key == K_a and self.rect.x >= 25:
            self.rect.x += self.paddle2_vel
        elif self.event_key == K_s and self.rect.y + 74 <= HEIGHT / 2:
            self.rect.y += self.paddle2_vel
        elif self.event_key == K_d and self.rect.x + 74 <= 580:
            self.rect.x += self.paddle2_vel


def paused():
    font = pygame.font.SysFont('comicsansms', 100)
    pause_text = font.render('Пауза', 2, 'black')
    text_rect = pause_text.get_rect()
    text_rect.center = (WIDTH / 2, HEIGHT / 2)

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                if event.key == pygame.K_SPACE:
                    screen.fill((0, 0, 0))
                    pause = False
        screen.blit(pause_text, text_rect)
        pygame.display.flip()


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

pad1_group = pygame.sprite.Group()
pad2_group = pygame.sprite.Group()

goal2_group = pygame.sprite.Group()  # группа для ворот верхнего игрока
goal1_group = pygame.sprite.Group()  # группа для ворот нижнего игрока

Border(25, 19, 195, 20)  # верхняя, слева
Border(405, 19, WIDTH - 25, 20)  # верхняя, справа
Border(25, HEIGHT - 20, 195, HEIGHT - 25)  # нижняя, слева
Border(405, HEIGHT - 20, WIDTH - 25, HEIGHT - 20)  # нижняя, справа
Border(25, 20, 25, HEIGHT - 20)  # левая
Border(WIDTH - 25, 20, WIDTH - 25, HEIGHT - 20)  # правая

Goal2(195, 5, 405, 5)
Goal1(195, HEIGHT - 5, 405, HEIGHT - 5)

puck = Puck(37, WIDTH / 2 - 35, HEIGHT / 2 - 35)

pad2 = Pad2(37, WIDTH / 2 - 40, HEIGHT / 2 - 200)
pad1 = Pad1(37, WIDTH / 2 - 35, HEIGHT / 2 + 150)


def game():
    global player1_point, player2_point
    fon = pygame.transform.scale(load_image('field.png', colorkey=-1), (WIDTH, HEIGHT))
    win = False

    font = pygame.font.Font(None, 55)
    win_first_text = font.render("Победил нижний игрок", 2, 'black')
    win_second_text = font.render("Победил верхний игрок", 2, 'black')

    text_rect = win_first_text.get_rect()
    text_rect.center = WIDTH / 2, HEIGHT / 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player1_point = 0
                player2_point = 0
                main_menu.start_screen()

            if event.type == KEYDOWN:
                if event.key in (K_w, K_s, K_a, K_d):
                    pad2.keydown(event)
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    pad1.keydown(event)
                if event.key == pygame.K_ESCAPE:
                    paused()

            elif event.type == KEYUP:
                if event.key in (K_w, K_s, K_a, K_d):
                    pad2.keyup(event)
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    pad1.keyup(event)

            if win and event.type == MOUSEBUTTONUP:
                win = False
                player1_point = 0
                player2_point = 0
                main_menu.start_screen()

        if player1_point == 7:
            win = True
            screen.blit(win_first_text, text_rect)
            pygame.display.flip()
        elif player2_point == 7:
            win = True
            screen.blit(win_second_text, text_rect)
            pygame.display.flip()
        else:
            counter_first = font.render(str(player2_point), 1, 'black')
            counter_second = font.render(str(player1_point), 1, 'black')

            screen.blit(fon, (0, 0))
            screen.blit(counter_first, (50, 30))
            screen.blit(counter_second, (WIDTH - 70, HEIGHT - 60))

            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
        pygame.display.set_caption(f'Игра. Счёт: {player2_point}:{player1_point}')
        clock.tick(120)
