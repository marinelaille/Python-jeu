# lancer.py lance l'objet
import pygame
import math
from level import ramps, semi_platforms, get_y_on_ramp, is_pixel_solid

GRAVITY = 0.35

class Projectile:
    def __init__(self, pos, velocity, screen_size):
        # Position initiale
        self.pos = [float(pos[0]), float(pos[1])]
        # Vitesse initiale
        self.vx, self.vy = velocity
        # Rayon du projectile
        self.radius = 10
        self.landed = False
        self.returning = False
        self.ignore_gravity = False  # Ignore la gravité si True
        self.rect = pygame.Rect(pos[0]-self.radius, pos[1]-self.radius,
                                self.radius*2, self.radius*2)
        self.bounce_damping = 0.8  # Réduction de vitesse après rebond
        self.screen_w, self.screen_h = screen_size  # Dimensions de l'écran

    def update(self):
        # Si le projectile est au sol et ne revient pas, on arrête les mises à jour
        if self.landed and not self.returning:
            return

        if not self.ignore_gravity:
            self.vy += GRAVITY
        # Mise à jour de la position
        self.pos[0] += self.vx
        self.pos[1] += self.vy
        # Mise à jour du rectangle de collision
        self.rect.topleft = (self.pos[0]-self.radius,
                             self.pos[1]-self.radius)
        # Si le projectile est en vol libre , on vérifie collisions et rebonds
        if not self.returning:
            self.handle_wall_bounce()
            self.check_collisions()

    def handle_wall_bounce(self):
        # Gestion des rebonds sur les bords de l'écran
        x, y = self.pos
        if x - self.radius < 0 or x + self.radius > self.screen_w:
            self.vx *= -self.bounce_damping  # inversion + atténuation
        if y - self.radius < 0 or y + self.radius > self.screen_h:
            self.vy *= -self.bounce_damping
            if abs(self.vy) < 1:  # Si la vitesse verticale est faible après rebond, on considère le projectile au sol
                self.landed = True

    def check_collisions(self):
        x, y = int(self.pos[0]), int(self.pos[1])
        if is_pixel_solid(x, y):  # collision avec un mur ou sol solide
            self.landed = True
            return
        # Collision avec une rampe
        for ramp in ramps:
            if ramp['rect'].collidepoint(x, y):
                ey = get_y_on_ramp(ramp, x)
                if y >= ey:
                    self.pos[1] = ey
                    self.rect.top = ey - self.radius
                    self.landed = True
                    return
        # Collision avec une plateforme semi-solide
        for plat in semi_platforms:
            if plat.collidepoint(x, y + self.radius):
                self.pos[1] = plat.top
                self.rect.top = plat.top - self.radius
                self.landed = True
                return

    def draw(self, screen):
        # Calcule l'angle
        angle = math.atan2(self.vy, self.vx)
        length = self.radius * 5  # longueur de l'épée
        width = self.radius // 3  # largeur de l'épée
        # Surface transparente sur laquelle dessiner l'épée
        surf = pygame.Surface((length + width*2, length + width*2), pygame.SRCALPHA)
        cx = cy = (length + width*2) // 2  # centre de la surface

        # Lame
        blade_rect = pygame.Rect(0, 0, width, length)
        blade_rect.center = (cx, cy - length//4)
        pygame.draw.rect(surf, (220, 220, 220), blade_rect)

        # Fuller (rainure au centre de la lame)
        fuller = pygame.Rect(0, 0, width//3, length)
        fuller.center = blade_rect.center
        pygame.draw.rect(surf, (180, 180, 180), fuller)

        # Garde (croix de protection)
        guard = pygame.Rect(0, 0, width*4, width//2)
        guard.center = (cx, cy + width//2)
        pygame.draw.rect(surf, (150, 75, 0), guard)

        # Manche
        handle = pygame.Rect(0, 0, int(width//1.5), length//3)
        handle.center = (cx, cy + length//4)
        pygame.draw.rect(surf, (100, 50, 20), handle)

        # Pommeau (bout du manche)
        pygame.draw.circle(surf, (160,160,160), (cx, handle.bottom + width), width)

        # Rotation de l'épée selon sa direction de vol
        rot = pygame.transform.rotate(surf, -math.degrees(angle))
        rect = rot.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(rot, rect)  # affichage de l'épée à l'écran
