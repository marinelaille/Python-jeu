# player.py,
import pygame
import time
from settings import WIDTH, GRAVITY, JUMP_FORCE, PLAYER_SPEED, ANIM_SPEED
from assets import walk_images, idle_image, background
from level import is_pixel_solid, ramps, semi_platforms, get_y_on_ramp
from menu import main_menu

# Rectangle représentant le joueur
player = pygame.Rect(100, 100, 40, 72)
player_vel_y = 0
player_direction = "right"
player_anim_index = 0
player_anim_timer = 0
on_ground = False
is_moving = False

# --- Vie du joueur ---
health = 5
dead = False

# Barre de vie (6 niveaux de vie de 0 à 5)
health_images = [
    pygame.image.load("assets/player/health_bar/HB0.png").convert_alpha(),
    pygame.image.load("assets/player/health_bar/HB20.png").convert_alpha(),
    pygame.image.load("assets/player/health_bar/HB40.png").convert_alpha(),
    pygame.image.load("assets/player/health_bar/HB60.png").convert_alpha(),
    pygame.image.load("assets/player/health_bar/HB80.png").convert_alpha(),
    pygame.image.load("assets/player/health_bar/HB100.png").convert_alpha(),
]

# Animation de mort (6 images)
death_frames = [
    pygame.image.load(f"assets/player/dead/Dead_{i}.png").convert_alpha() for i in range(1, 7)
]

# Déplacement horizontal et saut
def move(keys):
    global player, player_direction, is_moving, player_vel_y
    is_moving = False
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        player.x -= PLAYER_SPEED
        player_direction = "left"
        is_moving = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += PLAYER_SPEED
        player_direction = "right"
        is_moving = True
    if (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_UP]) and on_ground:
        player_vel_y = JUMP_FORCE

    # Téléportation de l’autre côté si on sort de l’écran
    if player.right < 0:
        player.left = WIDTH
    elif player.left > WIDTH:
        player.right = 0

    update_animation()

# Met à jour l’animation de marche
def update_animation():
    global player_anim_index, player_anim_timer
    if is_moving:
        player_anim_timer += 1
        if player_anim_timer >= ANIM_SPEED:
            player_anim_timer = 0
            player_anim_index = (player_anim_index + 1) % len(walk_images)
    else:
        player_anim_index = 0
        player_anim_timer = 0

# Applique la gravité et gère les collisions verticales
def apply_gravity():
    global player_vel_y, on_ground
    on_ground = False
    player_vel_y += GRAVITY
    move_y = int(player_vel_y)
    direction = -1 if move_y < 0 else 1

    for _ in range(abs(move_y)):
        player.y += direction
        # Collision avec les pixels solides
        for dx in range(5, player.width - 5, 5):
            foot_x = player.left + dx
            foot_y = player.bottom if direction > 0 else player.top
            if is_pixel_solid(foot_x, foot_y):
                player.y -= direction
                player_vel_y = 0
                if direction > 0:
                    on_ground = True
                break
        # Rampe
        for ramp in ramps:
            if ramp['rect'].colliderect(player):
                ramp_y = get_y_on_ramp(ramp, player.centerx)
                if player.bottom >= ramp_y - 2 and player.bottom <= ramp_y + 15:
                    player.bottom = ramp_y
                    player_vel_y = 0
                    on_ground = True
        # Plateforme semi-solide
        for plat in semi_platforms:
            if player.colliderect(plat):
                from_top = player_vel_y > 0 and player.bottom - player_vel_y <= plat.top
                if from_top:
                    player.bottom = plat.top
                    player_vel_y = 0
                    on_ground = True

# Affiche le joueur à l’écran
def draw(screen):
    image = walk_images[player_anim_index] if is_moving else idle_image
    if player_direction == "left":
        image = pygame.transform.flip(image, True, False)
    offset = player.height - image.get_height()
    screen.blit(image, (player.x, player.y + offset))

# Affiche la barre de vie
def draw_health_bar(screen):
    life_img = health_images[health] if 0 <= health <= 5 else health_images[0]
    screen.blit(life_img, (20, 20))

# Retourne le rectangle du joueur (utile pour les collisions)
def get_player_rect():
    return player

# Réduit la vie du joueur et déclenche la mort si nécessaire
def take_damage():
    global health, dead
    if health > 0:
        health -= 1
    if health <= 0 and not dead:
        dead = True

# Vérifie si le joueur est en vie
def is_alive():
    return not dead

# Joue l’animation de mort (affichée image par image)
def play_death_animation(screen, playtime):
    for img in death_frames:
        screen.blit(background, (0, 0))
        screen.blit(img, (player.x, player.y))
        pygame.display.flip()
        pygame.time.delay(150)
    screen.blit(background, (0, 0))
    screen.blit(death_frames[-1], (player.x, player.y))
    pygame.display.flip()

# Réinitialise l’état du joueur (position, vie, animation…)
def reset_player():
    global player, player_vel_y, player_direction, player_anim_index
    global player_anim_timer, on_ground, is_moving, health, dead

    player = pygame.Rect(100, 100, 40, 72)
    player_vel_y = 0
    player_direction = "right"
    player_anim_index = 0
    player_anim_timer = 0
    on_ground = False
    is_moving = False
    health = 5
    dead = False
