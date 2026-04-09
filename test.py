
import pygame
import numpy as np

# Before you can do much with pygame, you will need to initialize it
pygame.init()
# Init de clock
clock = pygame.time.Clock()

CIEL = 0, 200, 255  # parenthèses inutiles, l'interpréteur reconnaît un tuple

pos_ball_1 = [320, 240]
pos_ball_2 = (200, 240)
v_ball1 = 0
vecteur_ball = [1000,0]
constante_gravitation = 9.81 * 1000

def main():
    global v_ball1, vx_ball1, pos_ball_1, pos_ball_2
    dt=0
    fenetre = pygame.display.set_mode((640, 480))

    # loop
    loop = True
    # Création d'une image de la taille de la fenêtre
    background = pygame.Surface(fenetre.get_size())

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Superposition du fond ciel
        background.fill(CIEL)
        vecteur_ball[1] += constante_gravitation * dt
        pos_ball_1[1] += vecteur_ball[1] * dt
        pos_ball_1[0] += vecteur_ball[0] * dt
        print(pos_ball_1)
        print(v_ball1)
        pygame.draw.circle(background, "red", pos_ball_1, 10)
        
        pygame.draw.circle(background, "yellow", pos_ball_2, 10)
        fenetre.blit(background, (0, 0))

        if pos_ball_1[1] >= 400:
            vecteur_ball[1] = -vecteur_ball[1] * 0.90
            vecteur_ball[0] = vecteur_ball[0] * 0.90
            
        if pos_ball_1[0] >= 640:

            vecteur_ball[0] = -vecteur_ball[0] * 0.90
        
        if pos_ball_1[0] <= 0:

            vecteur_ball[0] = -vecteur_ball[0] * 0.90
    
        
        
        # Rafraîchissement de l'écran
        pygame.display.flip()
        # By calling Clock.tick(10) once per frame, the program will never run
        # at more than 10 frames per second
        clock.tick(10)
        dt = clock.tick(120) / 1000  # secondes

if __name__ == '__main__':
    main()
