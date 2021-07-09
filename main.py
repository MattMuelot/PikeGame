import pygame
import random

pygame.init()
pygame.font.init()
game_font = pygame.font.SysFont('timesnewroman', 35)
level_complete_font = pygame.font.SysFont('timesnewroman', 70)
clock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load('Assets/bground.png').convert_alpha()
startbg = pygame.image.load('Assets/startbg.png').convert_alpha()
level2bg = pygame.image.load('Assets/level2bg.png').convert_alpha()
pygame.mixer.init(size=-16, channels=2)
pygame.mixer.set_num_channels(16)
pike_sound = pygame.mixer.Sound('Assets/pike.ogg')
lose_sound = pygame.mixer.Sound('Assets/ugh.ogg')


class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load('Assets/pike.png').convert_alpha()
        self.x = x
        self.y = y
        self.vel = 10
        self.score = 0
        self.lives = 3
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


def main_menu():
    pygame.mixer.music.load('Assets/startnoise.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        clock.tick(60)
        screen.blit(startbg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    result = level_one()
                    if result is False:
                        running = False
                    elif result:
                        result = level_two()
                        if result is False:
                            running = False
        pygame.display.update()


def level_two():
    p = Player(200, 200)
    enemies = [Enemy() for _ in range(30)]
    beans = [Bean() for _ in range(20)]
    running = True
    while running:
        clock.tick(60)
        score_label = game_font.render(f'Score: {p.score}', True, (0, 0, 0))
        lives_label = game_font.render(f'Lives: {p.lives}', True, (0, 0, 0))
        screen.blit(level2bg, (0, 0))
        screen.blit(score_label, (10, 10))
        screen.blit(lives_label, (660, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        p.draw_player(screen)
        p.move_player()
        p.update_rect()
        for b in beans[:]:
            b.vel = 5
            b.draw_enemy(screen)
            b.move_enemy()
            b.update_rect()
            result = b.off_screen()
            if result:
                beans.remove(b)
            if p.rect.colliderect(b.rect):
                beans.remove(b)
                pike_sound.play()
                p.score += 1
            if len(beans) <= 0:
                beans = [Bean() for _ in range(20)]
        for e in enemies[:]:
            e.vel = 5
            e.draw_enemy(screen)
            e.move_enemy()
            e.update_rect()
            result = e.off_screen()
            if result:
                enemies.remove(e)
            if p.rect.colliderect(e.rect):
                p.lives -= 1
                lose_sound.play()
                enemies.remove(e)
                if p.lives <= 0:
                    pygame.time.delay(3000)
                    running = False
        if p.score >= 50:
            pygame.time.delay(3000)
            return True
        else:
            pass
            if len(enemies) <= 0:
                enemies = [Enemy() for _ in range(30)]
        pygame.display.update()


def level_one():
    p = Player(200, 200)
    enemies = [Enemy() for _ in range(20)]
    beans = [Bean() for _ in range(20)]
    pygame.mixer.music.load('Assets/gametheme.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        clock.tick(60)
        score_label = game_font.render(f'Score: {p.score}', True, (0, 0, 0))
        lives_label = game_font.render(f'Lives: {p.lives}', True, (0, 0, 0))
        screen.blit(bg, (0, 0))
        screen.blit(score_label, (10, 10))
        screen.blit(lives_label, (660, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
                pike_sound.play()
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
                p.lives -= 1
                lose_sound.play()
                enemies.remove(e)
                if p.lives <= 0:
                    pygame.time.delay(3000)
                    running = False
        if p.score >= 25:
            level_label = level_complete_font.render('Level One Complete', True, (0, 0, 0))
            screen.blit(level_label, (125, 350))
            screen.blit(score_label, (10, 10))
            pygame.display.update()
            pygame.time.delay(3000)
            return True
        else:
            pass
            if len(enemies) <= 0:
                enemies = [Enemy() for _ in range(20)]
        pygame.display.update()


main_menu()
