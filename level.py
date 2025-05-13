# level.py : Rampes, plateformes, collisions
import pygame
from settings import WIDTH, HEIGHT
from assets import collision_mask

# les escaliers :
ramps = [
    {'rect': pygame.Rect(440, 430, 120, 45), 'y_start': 520, 'y_end': 432}, # escalier du bas
    {'rect': pygame.Rect(500, 270, 150, 45), 'y_start': 269, 'y_end': 430}, # escalier du bas
    {'rect': pygame.Rect(713, 81, 100, 45), 'y_start': 149, 'y_end': 80} # escalier du bas
]

semi_platforms = [pygame.Rect(663, 215, 10, 1)]

def get_y_on_ramp(ramp, x):
    """Retourne la hauteur (y) attendue en fonction de la position X sur la rampe"""
    t = (x - ramp['rect'].left) / ramp['rect'].width # On prend la position X et on la normalise entre 0 et 1 par rapport à la largeur de la rampe
    t = max(0, min(t, 1)) # verifie que t est entre 0 et 1
    return ramp['y_start'] + t * (ramp['y_end'] - ramp['y_start'])

def is_pixel_solid(x, y):
    """ detecte les colisions, si on est en dehors du jeu"""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        return collision_mask.get_at((x, y)) == 1  #return True si c'est solide, False sinon
    return False