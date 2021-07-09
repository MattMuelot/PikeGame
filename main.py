import pygame
import random

pygame.init()
clock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))


class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load('Assets/pike.png').convert_alpha()
        self.x = x
        self.y = y
        self.vel = 10
        self.score = 0
        self.rect = pygame.Rect(self.x + 20, self.y, 60, 100)

    def draw_player(self, s):
        s.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(s, (0, 255, 0), self.rect, 2)

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x - self.vel > -20:
            self.x -= self.vel
            self.update_rect()
        if keys[pygame.K_d] and self.x + self.vel < width - 80:
            self.x += self.vel
            self.update_rect()
        if keys[pygame.K_w] and self.y - self.vel > 0:
            self.y -= self.vel
            self.update_rect()
        if keys[pygame.K_s] and self.y + self.vel < height - 100:
            self.y += self.vel
            self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.x + 20, self.y, 60, 100)


class Enemy:
    def __init__(self):
        self.img = pygame.image.load('Assets/andrea.png').convert_alpha()
        self.x = random.randint(0, 700)
        self.y = random.randint(-3500, -500)
        self.vel = 2
        self.rect = pygame.Rect(self.x + 20, self.y, 60, 100)

    def draw_enemy(self, s):
        s.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(s, (0, 255, 0), self.rect, 2)

    def move_enemy(self):
        self.y += self.vel

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, 33, 100)

    def off_screen(self):
        if self.y > height:
            return True


class Bean:
    def __init__(self):
        self.img_load = pygame.image.load('Assets/bean.png').convert_alpha()
        self.img_scaled = pygame.transform.scale(self.img_load, (100, 100))
        self.x = random.randint(0, 700)
        self.y = random.randint(-3500, -500)
        self.vel = 2
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def draw_enemy(self, s):
        s.blit(self.img_scaled, (self.x, self.y))
        # pygame.draw.rect(s, (0, 255, 0), self.rect, 2)

    def move_enemy(self):
        self.y += self.vel

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y + 20, 100, 60)

    def off_screen(self):
        if self.y > height:
            return True


p = Player(200, 200)
enemies = [Enemy() for _ in range(20)]
beans = [Bean() for _ in range(20)]
running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    p.draw_player(screen)
    p.move_player()
    p.update_rect()
    for b in beans[:]:
        b.draw_enemy(screen)
        b.move_enemy()
        b.update_rect()
        result = b.off_screen()
        if result:
            beans.remove(b)
        if p.rect.colliderect(b.rect):
            beans.remove(b)
            p.score += 1
        if len(beans) <= 0:
            beans = [Bean() for _ in range(20)]
    for e in enemies[:]:
        e.draw_enemy(screen)
        e.move_enemy()
        e.update_rect()
        result = e.off_screen()
        if result:
            enemies.remove(e)
        if p.rect.colliderect(e.rect):
            running = False
        if len(enemies) <= 0:
            enemies = [Enemy() for _ in range(20)]
    pygame.display.update()
