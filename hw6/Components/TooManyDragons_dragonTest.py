# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 14:57:07 2014

@author: cbeery
"""

import pygame
from pygame.locals import * 
from random import random,randint,choice
import time 
from math import sqrt, exp

class TooManyDragonsModel:
    """ Encodes game state """
    
    def __init__(self,screenSize):
        """ Initiates starting state of game """
        self.screen = [0,screenSize[0],0,screenSize[1]]
    
        self.fireballs = []
        self.dragons = []
        
        self.dragon_frequency = 0
        self.spawnOfEvilCt = 0
        
    def addDragons(self):
        """ Adds a dragon instance to model """
        if self.dragon_frequency < time.clock():
            print str(self.spawnOfEvilCt) + '  ' + str(time.clock()) + '  ' + str(self.dragon_frequency)
            newDragon = Dragon(self) 
            self.dragons.append(newDragon)
            self.dragon_frequency += (10.0 * (1.9/2.0)**self.spawnOfEvilCt)
            self.spawnOfEvilCt += 1
            
    def cleanModel(self):
        """ Delete sprites that are not on screen """
        newDragonList = []
        newFireballList = []        
        
        for dragon in self.dragons:
            if dragon.x < (self.screen[1] + 2*dragon.appearance.get_width()) and dragon.x > (self.screen[0] - 2*dragon.appearance.get_width()):
                newDragonList.append(dragon)    
        for fireball in self.fireballs:
            if fireball.y < self.screen[3]:
                newFireballList.append(fireball)
                
        self.dragons = newDragonList
        self.fireballs = newFireballList
        
    def update(self):
        """ Updates game state """
        self.cleanModel()
        self.addDragons()
        for dragon in self.dragons:
            dragon.update()
        for fireball in self.fireballs:
            fireball.update()
              
#class Player:
    
class Dragon:
    """ Encodes state of dragon """
    def __init__(self,model):
        """ Initiates instance of dragon """
        
        self.model = model
        self.appearance = pygame.image.load('hero.png').convert() # asssumes one frame of animation 

        direction = choice(['left','right'])
        
        if direction == 'left':
            self.x = -self.appearance.get_width()
            self.y = randint(0,self.model.screen[3] - self.appearance.get_height())
            self.vx = 1.3
            self.mouth = [100,80]
            
        elif direction  == 'right':
            self.appearance = pygame.transform.flip(self.appearance, 1, 0)
            self.x = self.model.screen[1]
            self.y = randint(0,self.model.screen[3]*0.5)
            self.vx = randint(5,15)  * -0.15
            self.mouth = [80,80]
                
        else:
            print 'Creation of Dragon Surface Error' 
        
        self.appearance.set_colorkey(self.appearance.get_at((0,0)), RLEACCEL)  
        self.fireballCt = 1 
    
    def possiblyCreateBallofFieryDoom(self):
        """ Creates whether to create hurling fireball """   
               
        if self.fireballCt == 1:    #check if dragon isnstance has used up fireball
            #check if dragon is on screen
            if (self.x < self.model.screen[0] or self.x > self.model.screen[1]): 
                chance = 2
            elif self.x < (self.model.screen[1]*1/3):            
                chance = .996
            elif self.x > (self.model.screen[1]*2/3):
                chance = .994
            else:
                chance = .999
                
            #fire at random
            if random() > chance:
                #single fireball attack                 
                self.fireballCt = 0   
                newFireball = Fireball(self.model,self.x + self.mouth[0], self.y + self.mouth[1])
                
                #add to list of fireballs
                self.model.fireballs.append(newFireball)
                               
    def update(self):
        """ Updates status of dragon """
        self.x += self.vx
        self.possiblyCreateBallofFieryDoom()
        
        
class Fireball:
    """ Creates a fiery fireball of DOOOMMM """
    def __init__(self, model, x, y):
        """ Initiates instance of dragon """
        self.model = model
        self.color = (250,60,10)
        self.x = x
        self.y = y
        
        #find location to aim
        xCenter = (self.model.screen[1]-self.model.screen[0]) / 2.0
        yBottom = self.model.screen[3]
        
        #allow aiming discrepancy
        xOffset = randint(-130,130)
        
        #slope to achieve aim
        ySlope = (yBottom - y)
        xSlope = xCenter + xOffset - x
        
        mag = sqrt(ySlope**2 + xSlope**2)
   
        #nset velocities
        self.vx = xSlope/mag * 1.5
        self.vy = ySlope/mag * 1.5
        
    def update(self):
        """ Updates status of fireball """
        self.x += self.vx
        self.y += self.vy
                
    
#class ScoreText:
    
    
class TooManyDragonsView:
    """ Creates rendered view of game state for user """   
    def __init__(self,model,screen):      
        self.model = model
        self.screen = screen
        
        self.background = pygame.image.load('grass.jpg').convert()
        self.size = self.background.get_size()
        
    def draw(self):
        self.screen.blit(self.background, (0,0))  #erase all objects on screen
        
        for dragon in self.model.dragons:
            self.screen.blit(dragon.appearance,(dragon.x,dragon.y))
        
        for fireball in self.model.fireballs:
            pygame.draw.circle(self.screen, fireball.color, (int(fireball.x),int(fireball.y)), 10)
            
        pygame.display.update()
    
#class TooManyDragonsController:
#    """ Manipulates game state based on keyboard input """
    

if __name__ == '__main__':
    pygame.init()
  
    screenSize = (800,600)    #note: change for background image size
    screen = pygame.display.set_mode(screenSize)   
    
    model = TooManyDragonsModel(screenSize)
    view = TooManyDragonsView(model,screen)
#    controller = TooManyDragonsController(model)
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
#            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        pygame.time.delay(10) #this compared to speed will determine reaction time and image smoothness

    pygame.quit()   
    
    

    
    
    