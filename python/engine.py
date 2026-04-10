
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
    
    mur_gauche = seg.Segment((0, 0), (0, 480), space, elasticity=1, friction=0.4)
    mur_gauche.add_in_space(space)
    
    seg1 = seg.Segment((600, 200), (640, 200), space, elasticity=1, friction=0.4)
    seg1.add_in_space(space)

    #Balle
    
    
    texture_ball = pygame.Surface((10,10))
    ball1 = ball.Ball(100, 100, 10, texture_ball, elasticity=0.7)
    
    ball1.add_in_space(space)
    
    ball2 = ball.Ball(200, 80, 10, texture_ball, elasticity=0.7)
    
    ball2.add_in_space(space)
    
    ball3 = ball.Ball(300, 100, 10, texture_ball, elasticity=0.7)
    
    ball3.add_in_space(space)
    
    join = pymunk.PinJoint(ball1.body, ball2.body, (0,0), (0,0))

    join2 = pymunk.PinJoint(ball2.body, ball3.body, (0,0), (0,0))

    muscle_lenght = 150
    
    muscle = pymunk.DampedSpring(ball1.body, ball3.body, (0,0), (0,0), muscle_lenght, 200, 10)
    
    space.add(join, join2, muscle)

    muscle_up = True
    
    
    b_arm1 = pymunk.Body(1, 10)
    b_arm1.position = 400, 100
    arm1_shape = pymunk.Segment(b_arm1, (0,0), (100,0),4)
    
    b_arm2 = pymunk.Body(1, 10)
    b_arm2.position = 500, 100
    arm2_shape = pymunk.Segment(b_arm2, (0, 0), (100,0),4)
    
    muscle_lenght2 = 200
    muscle_up2 = True
    muscle2 = pymunk.DampedSpring(b_arm1, b_arm2, (80,0), (60,0), muscle_lenght, 200, 10)
    
    rotation_arm = pymunk.PivotJoint(b_arm1, b_arm2, (100, 0), (0, 0))
    
    space.add(b_arm1, arm1_shape, b_arm2, arm2_shape, rotation_arm, muscle2)
    
    

    # loop
    loop = True


    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Superposition du fond ciel
        screen.fill("gray")    # Efface l'écran
        
        
        if muscle_up:
            muscle_lenght +=1
        else:
            muscle_lenght -=1
            
        if muscle_lenght <= 50: 
            muscle_up = True
        elif muscle_lenght >= 150:
            muscle_up = False
            
        if muscle_up2:
            muscle_lenght2 +=1
        else:
            muscle_lenght2 -=1
            
        if muscle_lenght2 <= 25: 
            muscle_up2 = True
        elif muscle_lenght2 >= 200:
            muscle_up2 = False

        muscle2.rest_length = muscle_lenght2

        muscle.rest_length = muscle_lenght
        
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
