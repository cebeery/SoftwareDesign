# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 23:46:43 2014

@author: cbeery
"""

# grid prints a n by n grid of box such that pipes 
# and hyphens form walls and plus signs form corners
#   input: sidelength, this is the number of boxes 
#       form one side of the grid; 
#       assumes non-negative integer
#   "output": displays grid 
# 

wallChar = 4 #the number of chars in a wall 
heightGoal = 0 #counts reps for vert walls
j = 0  # tracks current box height

def make_grid(sideLength):
    global j
    j = 0   #resets j
    
    if(j < sideLength):
        make_top(sideLength)
        make_rest(sideLength)

def make_rest(s):
    global j
    if (j < s):
        make_walls(s)
        make_top(s)
        
        j = j + 1     
        make_rest(s)
 
#makes one horizonal set of walls    
def make_top(s):
    print('+' + (' -'*wallChar + ' +')*s)    
 
#makes one set of box length of vertical walls   
def make_walls(s): 
    global heightGoal
    if(heightGoal < wallChar): 
        print('|'),
        print((' '*wallChar*2 + '| ')*s )  
        
        heightGoal = heightGoal + 1;       
        make_walls(s)
    else:
        heightGoal = 0 #reset height goal
        
        
##
make_grid(3)
make_grid(4)

