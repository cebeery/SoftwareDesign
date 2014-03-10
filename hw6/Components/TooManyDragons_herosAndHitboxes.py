# -*- coding: utf-8 -*-
"""
Received on  Sunday, March 09, 2014 8:40 PM

@author: ldavis
"""

import pygame
from pygame.locals import *
import random
import math
import time

position = 0

class TooManyDragonsModel:
    """ Encodes the game state of Too Many Dragons"""
    def __init__(self):
        self.alive = 1
        self.hero = Hero()
        self.hitbox = Hitbox()
   
    def update(self):
        self.hero.update()
        self.hitbox.update()
   
class Hero:
    """Encodes the state of the player character in Too Many Dragons"""
    def __init__(self):
        self.icon = pygame.image.load('hero0.png').convert()
       
    def update(self):
        global position
        self.icon = pygame.image.load('hero'+str(position)+'.png').convert()
       
class Hitbox:
    """Encodes the state of the invisible fireball-blocking hitbox in Too Many Dragons"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 30
        self.height = 30
        self.color = (0,0,0)
       
    def update(self):
        global position
        if position == 0:
            self.x = 610
            self.y = 450
        elif position == 1:
            self.x = 335
            self.y = 305
        elif position == 2:
            self.x = 275
            self.y = 305
        elif position == 3:
            self.x = 335
            self.y = 335
        elif position == 4:
            self.x = 275
            self.y = 335           
        elif position == 5:
            self.x = 305
            self.y = 305
   
class PyGameTooManyDragonsView:
    """ renders the TooManyDragonsModel to a pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
   
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        self.screen.blit(model.hero.icon,(320,320))
        pygame.draw.rect(self.screen, pygame.Color(255,255,255), pygame.Rect(self.model.hitbox.x, self.model.hitbox.y, 30, 30))
        pygame.display.update()

class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input """
    def __init__(self, model):
        self.model = model
   
    def handle_pygame_event(self, event):       
        global position       
        if event.type != KEYDOWN:
            position = 0
        elif event.key == pygame.K_e:
            position = 1
        elif event.key == pygame.K_q:
            position = 2
        elif event.key == pygame.K_d:
            position = 3
        elif event.key == pygame.K_a:
            position = 4
        elif event.key == pygame.K_w:
            position = 5
           
if __name__ == '__main__':
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    model = TooManyDragonsModel()
    view = PyGameTooManyDragonsView(model,screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
 