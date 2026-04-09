
import pygame
from entity import ball
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
    b0 = space.static_body
    segment = pymunk.Segment(b0, (0, 480), (640, 480), 4)  # De (0,0) à (640,0), épaisseur 4
    segment.elasticity = 1
    segment.friction = 0.4
    
    
    #Balle
    
    BASE_DIR = os.path.dirname(__file__)  # dossier de engine.py
    sprite_sheet = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'astraya_textures_final.png'))


    def get_sprite(sheet, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (x, y, width, height))
        return sprite
    
    texture_ball = get_sprite(sprite_sheet, 0, 288, 16, 16)
    ball1 = ball.Ball(100, 100, 10, texture_ball)
    
    ball1.add_in_space(space)
    
    space.add(segment)
    

    
    

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
