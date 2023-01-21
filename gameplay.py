import os
import random
import time

from pygame.locals import *
import pygame
import main_menu

FPS = 50
size = WIDTH, HEIGHT = 600, 800
STEP = 10
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
puck1_vel = 0
ochko_sverhu = 0
ochko_snizu = 0


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


class vorota1(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vorotas1)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(vorotas1)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class vorota2(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vorotas2)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(vorotas2)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)




class Puck(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.radius = radius
        self.add(puck_group)
        self.radius = radius
        self.image = pygame.transform.scale(load_image('puck.png', colorkey=-1), (70, 70))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(3, 5)
        self.vy = random.randint(3, 5)

    def update(self):
        global ochko_snizu, ochko_sverhu
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, pads):
            if main_menu.diff == 'Hardcore':
                self.vx = - random.randint(720, 1800) // 360
                self.vy = - 1800 // 360
            elif main_menu.diff == 'Medium':
                self.vx = - random.randint(360, 900) // 360
                self.vy = - 900 // 360
            else:
                self.vx = - random.randint(720, 1800) // 360
                self.vy = - 1800 // 360
                                                            # - random.randint(720, 1800) // 360
        if pygame.sprite.spritecollideany(self, vorotas1):
            ochko_sverhu += 1
            self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
            print(ochko_sverhu)
        if pygame.sprite.spritecollideany(self, vorotas2):
            ochko_snizu += 1
            self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
            print(ochko_snizu)




class Pad1(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(pads)
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
        if self.event_key in (K_UP, K_DOWN):
            self.rect.y += self.paddle1_vel
        elif self.event_key in (K_LEFT, K_RIGHT):
            self.rect.x += self.paddle1_vel
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.paddle1_vel = 0
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.paddle1_vel = 0
        if pygame.sprite.spritecollideany(self, vorotas1):
            self.paddle1_vel = 0
        if pygame.sprite.spritecollideany(self, vorotas2):
            self.paddle1_vel = 0
        if pygame.sprite.spritecollideany(self, puck_group) and self.event_key in (K_UP, K_DOWN):
            self.rect.y -= 3 * self.paddle1_vel
        if pygame.sprite.spritecollideany(self, puck_group) and self.event_key in (K_LEFT, K_RIGHT):
            self.rect.x -= 3 * self.paddle1_vel
        if pygame.sprite.spritecollideany(self, puck_group):
            self.rect.y -= 3 * self.paddle1_vel





class Pad2(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(pads)
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
        if self.event_key in (K_w, K_s):
            self.rect.y += self.paddle2_vel
        elif self.event_key in (K_a, K_d):
            self.rect.x += self.paddle2_vel
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.paddle2_vel = 0
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.paddle2_vel = 0
        if pygame.sprite.spritecollideany(self, puck_group) and self.event_key in (K_UP, K_DOWN):
            self.rect.y -= 2 * self.paddle2_vel
        if pygame.sprite.spritecollideany(self, puck_group) and self.event_key in (K_LEFT, K_RIGHT):
            self.rect.x -= 2 * self.paddle2_vel
        if pygame.sprite.spritecollideany(self, puck_group):
            self.rect.x -= 2 * self.paddle2_vel



all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
pads = pygame.sprite.Group()
puck_group = pygame.sprite.Group()
vorotas1 = pygame.sprite.Group()
vorotas2 = pygame.sprite.Group()
Border(25, 20, 195, 20)
Border(405, 20, WIDTH - 25, 20)
vorota1(195, 5, 405, 5)

Border(25, HEIGHT - 20, 195, HEIGHT - 25)
Border(405, HEIGHT - 20, WIDTH - 25, HEIGHT - 20)


Border(25, 25, 25, HEIGHT - 25)
Border(WIDTH - 25, 25, WIDTH - 25, HEIGHT - 25)
vorota2(195, HEIGHT - 5, 405, HEIGHT - 5)

puck = Puck(35, WIDTH / 2 - 35, HEIGHT / 2 - 35)

pad2 = Pad2(37, WIDTH / 2 - 40, HEIGHT / 2 - 200)
pad1 = Pad1(37, WIDTH / 2 - 35, HEIGHT / 2 + 150)


def game():
    global ochko_sverhu
    fon = pygame.transform.scale(load_image('field.png', colorkey=-1), (WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu.start_screen()
            if event.type == KEYDOWN:
                if event.key in (K_w, K_s, K_a, K_d):
                    pad2.keydown(event)
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    pad1.keydown(event)
            elif event.type == KEYUP:
                if event.key in (K_w, K_s, K_a, K_d):
                    pad2.keyup(event)
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    pad1.keyup(event)
        if ochko_sverhu == 1 or main_menu.diff == 'Easy':
            print(main_menu.diff)
            screen.blit(pygame.transform.scale(load_image('360_F_285022198_LtruJzc7mtN7DWRpds1EX4QNQLCa6ltH.jpg', colorkey=-1), (WIDTH, HEIGHT)),(0,0))
            pygame.display.flip()
            time.sleep(5)
            pygame.quit()
        else:
            screen.blit(fon, (0, 0))
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
        clock.tick(120)
    pygame.quit()
