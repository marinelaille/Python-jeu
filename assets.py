# assets.py : chargement des images
import pygame

background = pygame.image.load("background.png").convert()
collision_image = pygame.image.load("mask.png").convert()
collision_mask = pygame.mask.from_threshold(collision_image, (255, 255, 255), (1, 1, 1))

# Chargement animation
walk_images = [
    pygame.transform.scale(
        pygame.image.load(f"assets/player/walk/Walk (0_{i}).png").convert_alpha(), (84, 100)
    ) for i in range(7)
]
idle_image = pygame.image.load("assets/player/normal.png").convert_alpha()

monstre_walk_right = []
monstre_walk_left = []

#Chargement des animtaions des monstres
for i in range(8):
    img = pygame.image.load(f"assets/monstres/walk/Walk ({i}).png").convert_alpha()
    img = pygame.transform.scale(img, (84, 100))
    monstre_walk_right.append(img)
    monstre_walk_left.append(pygame.transform.flip(img, True, False))


# Chargement des animations d'attaque
run_attack_images = [
    pygame.image.load(f"assets/player/running_attack/Run+Attack (0_{i}).png").convert_alpha()
    for i in range(6)
]
idle_attack_images = [
    pygame.image.load(f"assets/player/attacks/Attack 1_{i+1}.png").convert_alpha()
    for i in range(5)
]
