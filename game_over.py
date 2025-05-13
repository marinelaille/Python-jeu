# game_over.py,
import pygame
import sys
import highscore
from menu import main_menu

def draw_styled_button(screen, rect, text, color, text_color, font):
    pygame.draw.rect(screen, color, rect, border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=5)
    text_surf = font.render(text, True, text_color)
    screen.blit(
        text_surf,
        (rect.centerx - text_surf.get_width() // 2,
         rect.centery - text_surf.get_height() // 2)
    )

def game_over_screen(screen, playtime, score):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Polices
    title_font  = pygame.font.Font("assets/fonts/Medievalfonts.ttf", 70)
    button_font = pygame.font.SysFont("arial", 32)
    info_font   = pygame.font.SysFont("arial", 28)

    # Couleur de fond
    background_color = (20, 20, 20)

    # Boutons
    menu_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2,      200, 50)
    quit_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50)

    # Mettre à jour et récupérer les 5 meilleurs scores (pièces)
    best_scores = highscore.update_scores(score)

    # Marge gauche pour la liste
    LEFT_MARGIN = 50

    while True:
        screen.fill(background_color)

        # Titre centré
        title = title_font.render("Game Over", True, (255, 0, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        # Playtime centré
        t_surf = info_font.render(f"Playtime : {playtime}s", True, (230, 230, 230))
        screen.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 180))

        # Score actuel centré
        s_surf = info_font.render(f"Score : {score}", True, (255, 215, 0))
        screen.blit(s_surf, (WIDTH//2 - s_surf.get_width()//2, 220))

        # Titre de la liste aligné à gauche
        rec_title = info_font.render("Top 5 Meilleurs scores", True, (212, 175, 55))
        screen.blit(rec_title, (LEFT_MARGIN, 260))

        # Liste des scores, alignée à gauche
        for i, s in enumerate(best_scores):
            line = info_font.render(f"{i+1}. {s} pièces", True, (230, 230, 230))
            screen.blit(line, (LEFT_MARGIN, 300 + i*30))

        # Boutons (gardés centrés)
        draw_styled_button(screen, menu_btn, "Menu principal",
                           (139, 69, 19), (255,255,255), button_font)
        draw_styled_button(screen, quit_btn, "Quitter",
                           (139, 0, 0), (255,255,255), button_font)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.collidepoint(event.pos):
                    main_menu(screen)
                    return
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
