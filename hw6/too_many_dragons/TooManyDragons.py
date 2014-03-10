# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 14:57:07 2014

@author: cbeery
"""

import pygame
from pygame.locals import * 
from random import random,randint,choice
import time 
from math import sqrt

class TooManyDragonsModel:
    """ Encodes game state """
    
    def __init__(self,screenSize):
        """ Initiates starting state of game """
        self.screen = [0,screenSize[0],0,screenSize[1]]
        #initiate lists for fireballs and dragons, which will be used to keep track of multiple instances later 
        self.fireballs = []
        self.dragons = []
        self.hero = Hero(self)
        
        self.dragon_frequency = 0
        self.spawnOfEvilCt = 0
        
        self.score = 0
        
    def addDragons(self):
        """ Adds a dragon instance to model """
        if self.dragon_frequency < time.clock():
            newDragon = Dragon(self) 
            self.dragons.append(newDragon)
            #the rate of dragon appearances increases as more dragons appear, until there are TOO MANY DRAGONS
            self.dragon_frequency += (6.0 * (1.9/2.0)**self.spawnOfEvilCt)
            self.spawnOfEvilCt += 1
            
    def cleanModel(self):
        """ Delete sprites that are not on screen """
        newDragonList = []
        newFireballList = []        
        #things are on the screen are the only ones on the relevant lists
        for dragon in self.dragons:
            if dragon.x < (self.screen[1] + 2*dragon.icon.get_width()) and dragon.x > (self.screen[0] - 2*dragon.icon.get_width()):
                newDragonList.append(dragon)    
        for fireball in self.fireballs:
            if fireball.y < self.screen[3]-100 and fireball.y > self.screen[2]:
                newFireballList.append(fireball)
                
        self.dragons = newDragonList
        self.fireballs = newFireballList
        
    def globalCheckCollisions(self):
        """ check for fireball collisions """
        newFireballList = []
        global score
        global running
        global position
        
        for fireball in self.fireballs:
            
            dragonIndex = 0
            for dragon in self.dragons:
                if fireball.bounced:                    
                    if self.checkCollision(fireball, [dragon.x,dragon.y,dragon.icon.get_width(),dragon.icon.get_height()]):
                        del self.dragons[dragonIndex]
                        #5 points per kill
                        score += 5
                        break
                    dragonIndex += 1             
            else:		
                if self.checkCollision(fireball, [self.hero.hitbox.x,self.hero.hitbox.y,self.hero.hitbox.width,self.hero.hitbox.height]):
                    if fireball.bounced == False: 
                        #different behavior for vertical shield position
                        if position == 5:                            
                            fireball.vx = fireball.vx
                            fireball.vy = - fireball.vy
                        else:
                            fireball.vx = - fireball.vx
                            fireball.vy = - fireball.vy
                        score += 1
                        #tell fireball it has bounced                        
                        fireball.bounced = 1
                    newFireballList.append(fireball)
                elif self.checkCollision(fireball, [self.hero.x,self.hero.y,self.hero.icon.get_width(),self.hero.icon.get_height()]):
                    #if fireball hits heroine, game over                    
                    running = 0
                else:
                    newFireballList.append(fireball)
                    
        self.fireballs = newFireballList   
                 
    def checkCollision(self,attacker,attackee):
        """ Does fireball hit rect? """
        collision = 0
        if attacker.x > attackee[0] and attacker.x < (attackee[0] + attackee[2]):
            if attacker.y > attackee[1] and attacker.y < (attackee[1] + attackee[3]):
                collision = 1
        return collision
    
    def update(self):
        """ Updates game state """
        self.globalCheckCollisions()        
        self.cleanModel()
        self.addDragons()
        self.hero.update()
        for dragon in self.dragons:
            dragon.update()
        for fireball in self.fireballs:
            fireball.update()
        
              
class Hero:
    """Encodes the state of the player character in Too Many Dragons"""
    def __init__(self,model):
        self.model = model
        self.icon = pygame.image.load('hero0.png').convert()
        self.hitbox = Hitbox(self)
        
        self.x = int ((self.model.screen[1]-self.model.screen[0] - self.icon.get_width()) / 2.0 )
        self.y = int (self.model.screen[3] - self.icon.get_height() - 100)
        
    def update(self):
        global position
        #change icon based on keypress
        self.icon = pygame.image.load('hero'+str(position)+'.png').convert()
        self.icon.set_colorkey((255,0,234), RLEACCEL)
        self.hitbox.update()
        
class Hitbox:
    """Encodes the state of the invisible fireball-blocking hitbox in Too Many Dragons"""
    def __init__(self,center):
        self.x = 0
        self.y = 0
        self.width = 26
        self.height = 26
        self.center = center
        
    def update(self):
        """Hitbox position varies based on the position of the heroine as input by the key commands"""
        global position
        if position == 0:
            self.x = 1000
            self.y = 1000
        elif position == 1:
            self.x = self.center.x + self.center.icon.get_width() -.5*self.width
            self.y = self.center.y - .5*self.height
        elif position == 2:
            self.x = self.center.x - .5*self.width
            self.y = self.center.y - .5*self.height
        elif position == 3:
            self.x = self.center.x + self.center.icon.get_width() -.5*self.width
            self.y = self.center.y - self.height + self.center.icon.get_height() 
        elif position == 4:
            self.x = self.center.x - .5*self.width
            self.y = self.center.y - self.height + self.center.icon.get_height()          
        elif position == 5:
            self.x = self.center.x
            self.y = self.center.y - .5*self.height

    
class Dragon:
    """ Encodes state of dragon """
    def __init__(self,model):
        """ Initiates instance of dragon """
        
        self.model = model
        self.icon = pygame.image.load('dargon1.png').convert() # asssumes one frame of animation 
        self.counter = 1
        self.lastswitch = 0
        #dragon spawns on random side of the screen
        self.direction = choice(['left','right'])
        
        if self.direction == 'left':
            self.x = -self.icon.get_width()
            self.y = randint(0,self.model.screen[3] - self.icon.get_height()-150)
            self.vx = 1.3
            self.mouth = [85,80]
            
        elif self.direction  == 'right':
            self.icon = pygame.transform.flip(self.icon, 1, 0)
            self.x = self.model.screen[1]
            self.y = randint(0,self.model.screen[3] - self.icon.get_height()-150)
            self.vx = randint(5,15)  * -0.15
            self.mouth = [5,80] #mouth location for shooting great balls of fire from
                
        else:
            print 'Creation of Dragon Surface Error' 
        #make the pink background of the dragon .png invisible (easier than using transparent images)
        self.icon.set_colorkey((255,0,234), RLEACCEL)  
        self.fireballCt = 1 
        self.isAlive = 1
    
    def possiblyCreateBallofFieryDoom(self):
        """ Creates whether to create hurling fireball """   
               
        if self.fireballCt == 1:    #check if dragon isnstance has used up fireball
            #check if dragon is on screen
            if (self.x < self.model.screen[0] or self.x > self.model.screen[1]): 
                chance = 2
            elif self.x < (self.model.screen[1]*1/3):            
                chance = .995
            elif self.x > (self.model.screen[1]*2/3):
                chance = .995
            else:
                chance = .998
                
            #fire at random
            if random() > chance:
                #single fireball attack                 
                self.fireballCt = 0   
                newFireball = Fireball(self.model,self.x + self.mouth[0], self.y + self.mouth[1])
                
                #add to list of fireballs
                self.model.fireballs.append(newFireball)
                
    def vary_dragon(self):
        """makes the dragon flap its wings using a time counter within each instance"""
        if time.clock() - self.lastswitch >= .4:
            if self.counter == 4:
                self.counter = 1
            else:
                self.counter += 1
            self.lastswitch = time.clock()
            self.icon = pygame.image.load('dargon'+str(self.counter)+'.png').convert()
            self.icon.set_colorkey((255,0,234), RLEACCEL) 
            #make sure to flip depending on side of origin
            if self.direction == 'right':
                self.icon = pygame.transform.flip(self.icon, 1, 0)
                
    def update(self):
        """ Updates status of dragon """
        self.vary_dragon()
        self.x += self.vx
        self.possiblyCreateBallofFieryDoom()     
    

        
class Fireball:
    """ Creates a fiery fireball of DOOOMMM """
    def __init__(self, model, x, y):
        """ Initiates instance of dragon """
        self.model = model
        self.color = (250,150,0)
        self.x = x
        self.y = y
        self.r = 10
        self.bounced = 0
        
        #find location to aim
        xCenter = (self.model.screen[1]-self.model.screen[0]) / 2.0
        yBottom = self.model.screen[3] - 100 - model.hero.icon.get_height()*0.5
        
        #allow aiming discrepancy
        xOffset = randint(-25,25)
        
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
                
class TooManyDragonsView:
    """ Creates rendered view of game state for user """      
    
    def __init__(self,model,screen):          
        self.model = model
        self.screen = screen
        self.lastswitch = 0
        self.counter = 1
        self.background = pygame.image.load('Frame1.png').convert()
        self.size = self.background.get_size() 
        
    def vary_background(self):
        """changes the background image to create a pretty gif. see vary_dragon above"""
        if time.clock() - self.lastswitch >= .1:
            if self.counter == 8:
                self.counter = 1
            else:
                self.counter += 1
            self.lastswitch = time.clock()
            self.background = pygame.image.load('Frame'+str(self.counter)+'.png').convert()
            
    def scoreDisplay(self):
        """draws the score counter in the bottom left corner using .png sprites"""
        global score        
        lastDigits = 5
        for num in str(score):
            y = 370 
            x = lastDigits
            numPic = pygame.image.load(str(num) + '.png').convert()
            self.screen.blit(numPic,(x,y))    
            #add width of previous image before appending next one
            lastDigits += numPic.get_width() 
        
    def draw(self):
        """render the game model for Too Many Dragons"""
        self.vary_background()
        self.screen.blit(self.background, (0,0))  #erase all objects on screen
        self.screen.blit(model.hero.icon,(model.hero.x,model.hero.y))
        self.scoreDisplay()
        
        for dragon in self.model.dragons:
            self.screen.blit(dragon.icon,(dragon.x,dragon.y))
        
        for fireball in self.model.fireballs:
            pygame.draw.circle(self.screen, fireball.color, (int(fireball.x),int(fireball.y)), fireball.r)
    
        pygame.display.update()
    
class TooManyDragonsController:
    """ Manipulates game state based on keyboard input """
    def __init__(self, model):
        self.model = model
   
    def handle_pygame_event(self, event):    
        """keyboard controls"""
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
    
    position = 0
    score = 0
    
    screenSize = (640,400)    #note: change for background image size
    screen = pygame.display.set_mode(screenSize)   
    
    #mvc game design woooo
    model = TooManyDragonsModel(screenSize)
    view = TooManyDragonsView(model,screen)
    controller = TooManyDragonsController(model)
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        pygame.time.delay(10) #this compared to speed will determine reaction time and image smoothness
    #game over behavior: show a death screen, wait, then quit
    screen.blit(pygame.image.load('gameover.png').convert(),(0,0))
    view.scoreDisplay()
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
    
    