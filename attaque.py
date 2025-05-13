# ataque du joueur
import pygame
from player import player, is_moving, player_direction
from assets import run_attack_images, idle_attack_images
from monstres import monstres

# État de l'attaque
duration = 6  # frames entre chaque image
attack_index = 0
attack_timer = 0
attacking = False
cooldown = 60  # 60 frames = 1 seconde à 60 FPS
cooldown_timer = 0
attack_direction = "right"  # direction enregistrée lors de l'attaque

# Gestion de l'attaque
def handle_attack(keys):
    global attacking, attack_timer, attack_index, cooldown_timer, attack_direction

    if cooldown_timer > 0:
        cooldown_timer -= 1


    if pygame.mouse.get_pressed()[2] and not attacking and cooldown_timer == 0:
        attacking = True
        attack_index = 0
        attack_timer = 0
        cooldown_timer = cooldown  # démarrer le cooldown
        attack_direction = player_direction  # enregistrer la direction au début

    if attacking:
        attack_timer += 1
        if attack_timer >= duration:
            attack_timer = 0
            attack_index += 1

        total_frames = len(run_attack_images) if is_moving else len(idle_attack_images)
        if attack_index >= total_frames:
            attacking = False
            attack_index = 0

        # Générer la hitbox d'attaque
        hitbox = pygame.Rect(player.x, player.y, player.width + 20, player.height)
        if attack_direction == "left":
            hitbox.x -= 20

        # Tuer un seul monstre dans la hitbox
        for monstre in monstres:
            if hitbox.colliderect(monstre.rect):
                monstre.take_hit()
                break

# Affichage
def draw_attack(screen):
    if not attacking:
        return

    if is_moving:
        image = run_attack_images[attack_index % len(run_attack_images)]
    else:
        image = idle_attack_images[attack_index % len(idle_attack_images)]

    if attack_direction == "left":
        image = pygame.transform.flip(image, True, False)

    offset_y = player.height - image.get_height()
    screen.blit(image, (player.x, player.y + offset_y))

def is_attacking():
    return attacking
