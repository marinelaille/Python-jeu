# menu

import pygame
import sys

pygame.init()

# Couleurs médiévales
BROWN = (120, 60, 30)
GOLD = (212, 175, 55)
IVORY = (255, 255, 224)
BLACK = (0, 0, 0)


def draw_button(screen, rect, text, font, hover=False):
    #Bouton stylisé médiéval avec effet de survol
    color = GOLD if hover else BROWN
    # Ombre portée
    shadow_rect = rect.move(4, 4)
    pygame.draw.rect(screen, BLACK, shadow_rect, border_radius=6)
    # Fond du bouton
    pygame.draw.rect(screen, color, rect, border_radius=6)
    # Bordure simple
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    # Texte
    text_surface = font.render(text, True, IVORY)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_sword_cursor(screen, pos):
    #Dessine un curseur en forme d'épée à la position donnée
    x, y = pos
    # Lame
    blade_length = 30
    blade_width = 4
    pygame.draw.rect(screen, (200, 200, 200), (x, y, blade_width, blade_length))
    # Garde
    guard_w, guard_h = 16, 4
    pygame.draw.rect(screen, GOLD, (x - (guard_w - blade_width)//2, y + blade_length//2, guard_w, guard_h))
    # Poignée
    handle_length = 12
    handle_w = 6
    pygame.draw.rect(screen, BROWN, (x + blade_width//2 - handle_w//2, y + blade_length//2 + guard_h, handle_w, handle_length))
    # Pommeau
    pygame.draw.circle(screen, GOLD, (x + blade_width//2, y + blade_length//2 + guard_h + handle_length + 4), 4)

def afficher_regles(screen, background_image):
    """Affiche les règles avec effet parchemin"""
    screen.blit(background_image, (0, 0))

    W, H = screen.get_size()
    overlay = pygame.Surface((W - 100, H - 150), pygame.SRCALPHA)
    overlay.fill((245, 222, 179, 220))  # Parchemin translucide
    pygame.draw.rect(overlay, BLACK, overlay.get_rect(), 2)
    screen.blit(overlay, (50, 75))

    font = pygame.font.SysFont("freeserif", 26, bold=True)
    lines = [
        "RÈGLES DU JEU", "",
        "- Utilise les flèches pour te déplacer.",
        "- Évite ennemis et pièges.",
        "- Collectionne un max de piece pour battre le record.",
        "", "Appuie sur Entrée ou Échap pour revenir."
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (60, 30, 10))
        rect = text.get_rect(center=(W//2, 120 + i*40))
        screen.blit(text, rect)


def main_menu(screen):
    # Cacher le curseur système uniquement dans le menu
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    W, H = screen.get_size()

    title_font = pygame.font.SysFont("freeserif", 60, bold=True, italic=True)
    btn_font = pygame.font.SysFont("freeserif", 30, bold=True)

    play_rect = pygame.Rect(W//2 - 100, H//2, 200, 60)
    rules_rect = pygame.Rect(W//2 - 100, H//2 + 80, 200, 60)

    background = pygame.image.load("image_acceuil.png").convert()
    background = pygame.transform.scale(background, (W, H))

    in_rules = False

    while True:
        screen.blit(background, (0, 0))

        if not in_rules:
            # Titre avec ombre
            title = "Bienvenue, Chevalier"
            shadow = title_font.render(title, True, BLACK)
            screen.blit(shadow, (W//2 - shadow.get_width()//2 + 3, 103))
            rendered = title_font.render(title, True, GOLD)
            screen.blit(rendered, (W//2 - rendered.get_width()//2, 100))

            mpos = pygame.mouse.get_pos()
            draw_button(screen, play_rect, "Jouer", btn_font, play_rect.collidepoint(mpos))
            draw_button(screen, rules_rect, "Règles", btn_font, rules_rect.collidepoint(mpos))
        else:
            afficher_regles(screen, background)

        # Curseur épée
        draw_sword_cursor(screen, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not in_rules and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    pygame.mouse.set_visible(True)
                    return
                if rules_rect.collidepoint(event.pos):
                    in_rules = True
            elif in_rules and event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                in_rules = False


def main_game(screen):
    # Exemple de début de jeu où le curseur système est visible
    pygame.mouse.set_visible(True)
    # ... suite de ton code de jeu ...
    pass

if __name__ == "__main__":
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Aventure Médiévale")
    main_menu(screen)
    main_game(screen)