# pieces
import pygame
import random
from level import is_pixel_solid, semi_platforms

# Dimensions de la pièce
COIN_SIZE = 32
MAX_COINS = 5

# Génération procédurale de l'image de la pièce
def generate_coin_image(size=COIN_SIZE):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    radius = size // 2 - 2
    # Couleurs
    GOLD = (212, 175, 55)
    DARK = (160, 130, 40)
    LIGHT = (255, 220, 100)
    # Corps principal
    pygame.draw.circle(surf, GOLD, (center, center), radius)
    # Bordure sombre
    pygame.draw.circle(surf, DARK, (center, center), radius, 2)
    # Reflet
    pygame.draw.circle(surf, LIGHT, (center - radius//3, center - radius//3), radius//4)
    return surf

# Image générée une seule fois
coin_image = generate_coin_image()

# Liste des pièces actives
coins = []


def spawn_coins(count=MAX_COINS):
    """Fait apparaître 'count' pièces aléatoirement sur le sol ou les plateformes."""
    coins.clear()
    surf = pygame.display.get_surface()
    w, h = surf.get_size()
    attempts = 0

    while len(coins) < count and attempts < count * 10:
        attempts += 1
        x = random.randint(0, w - COIN_SIZE)
        # chercher le premier y où poser la pièce
        for yy in range(h):
            # test sol
            if is_pixel_solid(x + COIN_SIZE//2, yy):
                y = yy - COIN_SIZE
                break
            # test plateforme semi-solide
            for plat in semi_platforms:
                if plat.collidepoint(x + COIN_SIZE//2, yy):
                    y = plat.top - COIN_SIZE
                    break
            else:
                continue
            break
        else:
            continue  # pas de sol ni plateforme trouvé
        # ajouter la pièce
        coins.append(pygame.Rect(x, y, COIN_SIZE, COIN_SIZE))


def update_coins(player_rect, collect_callback):
    """Gère la collection et le respawn par vagues de pièces."""
    # collecte si collision
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            collect_callback()
    # si toutes ramassées, spawn une nouvelle vague
    if not coins:
        spawn_coins()


def draw_coins(screen):
    """Dessine toutes les pièces à l'écran."""
    for coin in coins:
        screen.blit(coin_image, coin.topleft)
