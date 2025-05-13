import pygame
import random
from settings import WIDTH, HEIGHT, GRAVITY, PLAYER_SPEED
from assets import monstre_walk_right, monstre_walk_left
from level import ramps, get_y_on_ramp
from player import is_pixel_solid, take_damage

#hh

# Liste des monstres actifs
monstres = []
spawn_timer = 0

# Fait apparaître un nouveau monstre avec une vitesse augmentée
def spawn_stronger_monstre():
    side = random.choice(['left', 'right'])
    x = -40 if side == 'left' else WIDTH + 40
    base_speed = 2
    increment = 0.15
    max_speed = PLAYER_SPEED - 0.5
    speed = min(base_speed + len(monstres) * increment, max_speed)
    monstres.append(Monstre(x, speed))

class Monstre:
    def __init__(self, x, speed=2):
        self.rect = pygame.Rect(x, 100, 40, 72)
        self.vel_y = 0
        self.anim_index = 0
        self.anim_timer = 0
        self.direction = "left"
        self.on_ground = False
        self.hp = 1
        self.speed = speed
        self.attack_cooldown = 60
        self.attack_timer = 0

    def take_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            monstres.remove(self)
            spawn_stronger_monstre()

    def update(self, player_rect):
        # Déplacement horizontal vers le joueur
        if self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed
            self.direction = "right"
        else:
            self.rect.x -= self.speed
            self.direction = "left"

        # Sauter ou tomber selon la position du joueur
        if player_rect.centery < self.rect.centery - 50 and self.on_ground:
            self.vel_y = -8
            self.on_ground = False
        elif player_rect.centery > self.rect.centery + 50 and self.on_ground:
            self.vel_y = 5
            self.on_ground = False

        # Gravité et collisions verticales
        self.vel_y += GRAVITY
        move_y = int(self.vel_y)
        direction = 1 if move_y > 0 else -1

        for _ in range(abs(move_y)):
            self.rect.y += direction
            collided = False
            for dx in range(5, self.rect.width - 5, 5):
                x = self.rect.left + dx
                y = self.rect.bottom if direction > 0 else self.rect.top
                if is_pixel_solid(x, y):
                    self.rect.y -= direction
                    self.vel_y = 0
                    if direction > 0:
                        self.on_ground = True
                    collided = True
                    break
            if collided:
                break

        # Ajustement sur les rampes
        for ramp in ramps:
            if ramp['rect'].colliderect(self.rect):
                ramp_y = get_y_on_ramp(ramp, self.rect.centerx)
                if self.rect.bottom >= ramp_y - 2 and self.rect.bottom <= ramp_y + 15:
                    self.rect.bottom = ramp_y
                    self.vel_y = 0
                    self.on_ground = True

        # Attaque du joueur
        self.attack_timer += 1
        if self.rect.colliderect(player_rect) and self.attack_timer >= self.attack_cooldown:
            take_damage()
            self.attack_timer = 0

        # Animation
        self.anim_timer += 1
        if self.anim_timer >= 6:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(monstre_walk_right)

    def draw(self, screen):
        # Affichage du sprite courant selon la direction
        img_list = monstre_walk_right if self.direction == "right" else monstre_walk_left
        current_image = img_list[self.anim_index]
        offset_y = self.rect.height - current_image.get_height()
        screen.blit(current_image, (self.rect.x, self.rect.y + offset_y))

# Met à jour tous les monstres et en fait apparaître un nouveau régulièrement
def update_monstres(player_rect):
    global spawn_timer
    spawn_timer += 1

    if spawn_timer >= 180:
        spawn_timer = 0
        side = random.choice(['left', 'right'])
        x = -40 if side == 'left' else WIDTH + 40
        base_speed = 2
        increment = 0.15
        max_speed = PLAYER_SPEED - 0.5
        speed = min(base_speed + len(monstres) * increment, max_speed)
        monstres.append(Monstre(x, speed))

    for monstre in monstres:
        monstre.update(player_rect)

# Dessine tous les monstres
def draw_monstres(screen):
    for monstre in monstres:
        monstre.draw(screen)

# Réinitialise la liste des monstres
def reset_monstres():
    global monstres, spawn_timer
    monstres = []
    spawn_timer = 0
