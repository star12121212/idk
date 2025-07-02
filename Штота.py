from pygame import *
from random import randint
import sys
import os
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
init()
mixer.init()
window = display.set_mode((700, 500))
clock = time.Clock()
background = transform.scale(image.load(os.path.join(base_path, "images", "fon.jpg")), (700, 500))
image_player = transform.scale(image.load(os.path.join(base_path, "images", "rocket.png")), (65, 96))
image_enemy = transform.scale(image.load(os.path.join(base_path, "images", "ufo.png")), (70, 70))
image_bullet = transform.scale(image.load(os.path.join(base_path, "images", "bomb.png")), (50, 42))

# Настройки скорости
initial_speed_player1 = 10
initial_speed_player2 = 10
speed_player1 = initial_speed_player1
speed_player2 = initial_speed_player2
min_speed_player = 2  # Минимальная скорость игрока
speed_decrease_step = 1  # Шаг уменьшения скорости

last_difficulty_increase = time.get_ticks()
difficulty_interval = 5000  
time_spawn = 60  
min_time_spawn = 10  
enemy_speed = 2 
max_enemy_speed = 8  
start_time = time.get_ticks()
survival_time = 0

mixer.music.load(os.path.join(base_path, "images", 'space.ogg'))
mixer.music.set_volume(0.2) # 50% громкости
fire_sound = mixer.Sound(os.path.join(base_path, "images", 'fire.ogg'))
fire_sound.set_volume(0.3) # 30% громкости
RED = (255, 0, 0)
enemy_list = []
bullet_list = []
last_soot_time = 0
cooldown_time = 300
score = 0
miss_score = 0
score_font = font.Font(None, 36)
orig_image = image_player
current_angle = 0


class Area():
    def __init__(self, x, y, width, height, image=None):
        self.rect = Rect(x, y, width, height) 
        self.image = image
    
    def fill(self):
        if self.image:
            window.blit(self.image, self.rect.topleft)
        else:
            draw.rect(window, RED, self.rect)

class Player(Area): 
    # метод рисует картинку поверх прямоугольника
    def fill(self):
        if self.image: # если картинка задана, отображаем картинку
            rotated_image = transform.rotate(image_player, current_angle)
            rotated_rect = rotated_image.get_rect(center=player.rect.center)
            window.blit(rotated_image, rotated_rect.topleft)
        else: # если картинка НЕ задана, просто рисуем серый прямоугольник
            draw.rect(window, RED, self.rect)

class Enemy(Area):
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)
        self.speed = enemy_speed
    
    def move(self):
        self.rect.y += self.speed

class Bullet(Area):
    def shoot(self):
        self.rect.y -= 10
player = Player(318, 380, 65, 96, image_player)
gameover_font = font.Font(None, 65)
game_over = False
orig_image = image_player
current_angle = 0

def show_game_over():
    window.blit(background, (0, 0))
    score_surf = gameover_font.render("Ты проиграл... ", True, (255, 255, 255))
    window.blit(score_surf, (200, 200))
    time_surf = score_font.render(f"Ты выживал: {survival_time:.1f} сек", True, (255, 255, 255))
    window.blit(time_surf, (200, 280))

def game_reset():
    global score, miss_score, enemy_list, bullet_list, player, game_over, speed_player1, speed_player2, last_difficulty_increase, start_time, survival_time, time_spawn, enemy_speed, move_left, move_right, move_up, move_down
    score = 0
    miss_score = 0
    enemy_list = []
    bullet_list = []
    player = Player(318, 380, 65, 96, image_player)
    game_over = False
    speed_player1 = initial_speed_player1
    speed_player2 = initial_speed_player2
    last_difficulty_increase = time.get_ticks()
    start_time = time.get_ticks()
    survival_time = 0
    time_spawn = 60
    enemy_speed = 2
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    
move_left = False
move_right = False
move_up = False
move_down = False

mixer.music.play(-1)
run = True

while run:
    current_time = time.get_ticks()
    
    if not game_over:
        survival_time = (current_time - start_time) / 1000
    
    if (current_time - last_difficulty_increase) >= difficulty_interval and not game_over:
        

        
        if speed_player1 > min_speed_player:
            speed_player1 = max(speed_player1 - speed_decrease_step, min_speed_player)
        if speed_player2 > min_speed_player:
            speed_player2 = max(speed_player2 - speed_decrease_step, min_speed_player)
        
        last_difficulty_increase = current_time
    
    if game_over:
        show_game_over()
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_r:
                    game_reset()
        display.update()
        clock.tick(60)
        continue
    
    window.blit(background, (0, 0))
    score_surf = score_font.render(f"Счет: {score}", True, (255, 255, 255))
    window.blit(score_surf, (10, 10))
    window.blit(score_font.render(f"Пропущено: {miss_score}", True, (255, 255, 255)), (10, 40))
    window.blit(score_font.render(f"Время: {survival_time:.1f} сек", True, (255, 255, 255)), (500, 10))
    window.blit(score_font.render(f"Скорость: {speed_player1:.1f}", True, (255, 255, 255)), (500, 40))
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_LEFT:
                move_left = True
            if e.key == K_RIGHT:
                move_right = True
            if e.key == K_UP:
                move_up = True
            if e.key == K_DOWN:
                move_down = True
            if e.key == K_SPACE and current_time - last_soot_time > cooldown_time:
                bullet_list.append(Bullet(player.rect.centerx - 10, player.rect.top, 21, 42, image_bullet))
                fire_sound.play()
                last_soot_time = current_time
        if e.type == KEYUP:
            if e.key == K_LEFT:
                move_left = False
            if e.key == K_RIGHT:
                move_right = False
            if e.key == K_UP:
                move_up = False
            if e.key == K_DOWN:
                move_down = False
    
    if move_left:
        player.rect.x -= speed_player1
        current_angle = min(current_angle + 2,  60)
    if move_right:
        player.rect.x += speed_player1
        current_angle = max(current_angle - 2, -60)
    if move_up:
        player.rect.y -= speed_player2
        current_angle = min(current_angle + 2,  180)
    if move_down:
        player.rect.y += speed_player2
        current_angle = max(current_angle - 2, -180)
    else: 
        current_angle *= 0.99
    player.rect.x = max(0, min(700 - player.rect.width, player.rect.x))
    player.rect.y = max(0, min(500 - player.rect.height, player.rect.y))
    
    if randint(1, time_spawn) == 1:
        enemy_list.append(Enemy(randint(20, 620), -50, 70, 70, image_enemy))
    
    for e in enemy_list[:]:
        e.fill()
        e.move()
        if player.rect.colliderect(e.rect):
            game_over = True
        if e.rect.top > 500:
            miss_score += 1
            enemy_list.remove(e)
    
    for b in bullet_list[:]:
        b.fill()
        b.shoot()
        if b.rect.bottom < 0:
            bullet_list.remove(b)
            continue
        for e in enemy_list[:]:
            if b.rect.colliderect(e.rect):
                score += 1
                enemy_list.remove(e)
                bullet_list.remove(b)
                break
    
    player.fill()
    display.update()
    clock.tick(60)
