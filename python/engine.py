
import pygame
from entity import ball
from entity import segment as seg
import pymunk
import pymunk.pygame_util
import random
import os

# Before you can do much with pygame, you will need to initialize it
pygame.init()
# Init de clock
clock = pygame.time.Clock()

CIEL = 0, 200, 255  # parenthèses inutiles, l'interpréteur reconnaît un tuple

debug = True

def main():

    screen = pygame.display.set_mode((640, 480))
    
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    #Creation de l'espace avec pymunk
    space = pymunk.Space()
    space.gravity = 0, 900
    
    #Sol

    sol = seg.Segment((0, 480), (640, 480), space, elasticity=1, friction=0.4)
    sol.add_in_space(space)
    
    
    mur_droite = seg.Segment((640, 0), (640, 480), space, elasticity=1, friction=0.4)
    mur_droite.add_in_space(space)
    
    collid = seg.Segment((0, 200), (200, 250), space, elasticity=1, friction=0.4)
    collid.add_in_space(space)
    
    collid2 = seg.Segment((0, 400), (200, 480), space, elasticity=1, friction=0.4)
    collid2.add_in_space(space)
    
    #Balle
    
    
    texture_ball = pygame.Surface((10,10))
    ball1 = ball.Ball(100, 100, 10, texture_ball, elasticity=0.7)
    
    ball1.add_in_space(space)

    

    
    

    # loop
    loop = True


    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Superposition du fond ciel
        screen.fill("gray")    # Efface l'écran
        

        
        space.step(0.01)  

        
        if not debug:
            ball1.draw(screen)
        else:
            space.debug_draw(draw_options)

        
        screen.blit(screen, (0,0))
        
        # Rafraîchissement de l'écran
        pygame.display.flip()

        dt = clock.tick(60) / 1000  # secondes


if __name__ == '__main__':
    main()
