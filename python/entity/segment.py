#Importer global_var qui est dans un dossier parent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import global_var as var
import math

import pygame
import numpy as np
import pymunk

class Segment():
    def __init__(self, debut:tuple[int, int], fin:tuple[int, int], space, epaisseur:int=4, elasticity:float=0.8, friction:float=0.8):
        self.body = space.static_body
        self.shape = pymunk.Segment(self.body, debut, fin, epaisseur)  # De (0,0) à (640,0), épaisseur 4
        self.shape.elasticity = 1
        self.shape.friction = 0.4
        
    def add_in_space(self, space):
        space.add(self.shape)
        
    def draw(self, screen):
        x, y = self.body.position
        angle = -math.degrees(self.body.angle)  # rotation pymunk → pygame
        
        # Rotation du sprite
        rotated = pygame.transform.rotate(self.sprite, angle)
        rect = rotated.get_rect(center=(int(x), int(y)))
        screen.blit(rotated, rect)