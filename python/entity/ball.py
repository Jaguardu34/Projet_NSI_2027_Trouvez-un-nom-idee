#Importer global_var qui est dans un dossier parent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import global_var as var
import math

import pygame
import numpy as np
import pymunk

class Ball():
    def __init__(self, x, y, radius, sprite, mass=1, moment=10, elasticity=0.8, friction=0.8):
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.sprite = sprite
        
    def add_in_space(self, space):
        space.add(self.body, self.shape)
        
    def draw(self, screen):
        x, y = self.body.position
        angle = -math.degrees(self.body.angle)  # rotation pymunk → pygame
        
        # Rotation du sprite
        rotated = pygame.transform.rotate(self.sprite, angle)
        rect = rotated.get_rect(center=(int(x), int(y)))
        screen.blit(rotated, rect)