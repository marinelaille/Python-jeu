# main.py,

import pygame
import sys
import time

pygame.init()


# Ensuite, importe les modules qui utilisent Pygame
from settings import screen, clock, FPS
from assets import background
from menu import main_menu
from player import (
    move, apply_gravity, draw, get_player_rect,
    draw_health_bar, play_death_animation,
    is_alive, reset_player
)
from monstres import update_monstres, draw_monstres, reset_monstres
import throwing
from attaque import handle_attack, draw_attack, is_attacking
from pause import pause_menu
from coin import spawn_coins, update_coins, draw_coins

score = 0
font_score = pygame.font.SysFont("arial", 24)

def collect_coin():
    global score
    score += 1

def draw_score(screen):
    surf = font_score.render(f"Score : {score}", True, (255, 215, 0))
    screen.blit(surf, (20, 20))
# -------------------------------------------------------------

# Fenêtre
WIDTH, HEIGHT = 1080, 607
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon Jeu")
clock = pygame.time.Clock()
FPS = 60

# 🎮 Afficher le menu
main_menu(screen)
start_time = time.time()

# ---- NOUVEAU : spawn initial des pièces ----
spawn_coins()


# === Boucle principale ===
def main():
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            throwing.handle_events(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu(screen, playtime)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        move(keys)
        apply_gravity()
        handle_attack(keys)

        screen.blit(background, (0, 0))

        if not is_alive():
            play_death_animation(screen, playtime)
            time.sleep(2)
            from game_over import game_over_screen
            game_over_screen(screen, playtime, score)
            return

        if is_attacking():
            draw_attack(screen)  # attaque avec sprite animé
        else:
            draw(screen)  # sinon le sprite normal

        player_rect = get_player_rect()
        update_monstres(player_rect)
        draw_monstres(screen)

        # mise à jour et dessin des pièces
        update_coins(player_rect, collect_coin)
        draw_coins(screen)


        throwing.update_and_draw(screen)
        draw_health_bar(screen)

        # affichage du score ----
        draw_score(screen)

        playtime = int(time.time() - start_time)  # 🔁 temps écoulé en secondes

        pygame.display.flip()


if __name__ == "__main__":
    main_menu(screen)
    main()
