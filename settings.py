# settings.py : constantes globales,
import pygame

WIDTH, HEIGHT = 1080, 607 # taille de la fenêtre
FPS = 60 # image / seconde

#Constantes physiques
GRAVITY = 0.8
JUMP_FORCE = -12
PLAYER_SPEED = 5
ANIM_SPEED = 6

#Fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efrei 2024 2025")
clock = pygame.time.Clock()
