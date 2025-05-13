# throwing.py,
import pygame
import math
from lancer import Projectile, GRAVITY
from player import get_player_rect
from monstres import monstres

# Constantes de visée façon Angry Birds
MAX_FORCE = 15
FORCE_FACTOR = 0.2
PARABOLA_STEPS = 30
PARABOLA_DT = 0.1

# Etat global
projectile = None
is_aiming = False
start_pos = (0, 0)


def calculate_velocity(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 0.0, 0.0
    speed = min(dist * FORCE_FACTOR, MAX_FORCE)
    angle = math.atan2(dy, dx)
    return math.cos(angle) * speed, math.sin(angle) * speed


def draw_parabolic_path(screen, start, velocity):
    x0, y0 = start
    vx, vy = velocity
    for i in range(PARABOLA_STEPS):
        t = i * PARABOLA_DT
        x = int(x0 + vx * t)
        y = int(y0 + vy * t + 0.5 * GRAVITY * (t ** 2))
        pygame.draw.circle(screen, (150, 150, 100), (x, y), 3)


def handle_events(event):
    global projectile, is_aiming, start_pos
    # pas de nouveau tir si épée déjà en vol ou au sol
    if projectile is not None:
        return

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        is_aiming = True
        # départ de la visée au centre du joueur
        start_pos = get_player_rect().center

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_aiming:
        end_pos = pygame.mouse.get_pos()
        vx, vy = calculate_velocity(start_pos, end_pos)
        projectile = Projectile(start_pos, (vx, vy), pygame.display.get_surface().get_size())
        is_aiming = False


def update_and_draw(screen):
    """Met à jour, dessine le projectile et gère ses collisions."""
    global projectile, is_aiming

    # Affichage de la parabole si on vise
    if is_aiming:
        mouse = pygame.mouse.get_pos()
        vx, vy = calculate_velocity(start_pos, mouse)
        draw_parabolic_path(screen, start_pos, (vx, vy))

    # Mise à jour et dessin du projectile
    if projectile:
        projectile.update()
        projectile.draw(screen)

        # → NOUVEAU : collision projectile / monstres
        for monstre in monstres[:]:  # on itère sur une copie pour pouvoir modifier la liste
            if projectile.rect.colliderect(monstre.rect):
                monstre.take_hit()
                # supprime l'épée pour éviter multi-hits
                projectile = None
                break

        # Si l'épée est posée au sol et qu’on marche dessus, on la ramasse
        if projectile and projectile.landed:
            pr = get_player_rect()
            if projectile.rect.colliderect(pr):
                projectile = None
                is_aiming = False
