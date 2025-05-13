# pause.py,
import pygame
import sys
from menu import main_menu

def pause_menu(screen, playtime):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Police personnalisée
    title_font = pygame.font.Font("assets/fonts/Medievalfonts.ttf", 70)
    button_font = pygame.font.SysFont("arial", 32)
    playtime_font = pygame.font.SysFont("arial", 28)

    # Couleur de fond unie
    background_color = (30, 30, 30)

    # Boutons
    resume_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50)
    menu_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50)
    quit_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50)

    while True:
        screen.fill(background_color)

        # Titre
        title = title_font.render("Pause", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Affichage du Playtime
        time_text = playtime_font.render(f"Playtime : {playtime}s", True, (240, 240, 240))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 180))

        # Boutons stylisés
        draw_styled_button(screen, resume_btn, "Reprendre", (255, 215, 0), (0, 0, 0), button_font)
        draw_styled_button(screen, menu_btn, "Menu principal", (139, 69, 19), (255, 255, 255), button_font)
        draw_styled_button(screen, quit_btn, "Quitter", (139, 0, 0), (255, 255, 255), button_font)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.collidepoint(event.pos):
                    return
                elif menu_btn.collidepoint(event.pos):
                    main_menu(screen)
                    return
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def draw_styled_button(screen, rect, text, color, text_color, font):
    pygame.draw.rect(screen, color, rect, border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=5)  # bordure noire
    text_surf = font.render(text, True, text_color)
    screen.blit(text_surf, (rect.centerx - text_surf.get_width() // 2, rect.centery - text_surf.get_height() // 2))
