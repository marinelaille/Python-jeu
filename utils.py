# main.py
import pygame, sys
from settings import screen, clock, FPS
from assets import background
from player import move, apply_gravity, draw

pygame.init()

# Boucle principale du jeu
while True:
    clock.tick(FPS)  # Limite la boucle à X images par seconde

    # Gestion des événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Contrôles du joueur
    keys = pygame.key.get_pressed()
    move(keys)
    apply_gravity()

    # Rendu de l’arrière-plan et du joueur
    screen.blit(background, (0, 0))
    draw(screen)
    pygame.display.flip()  # Mise à jour de l'affichage
