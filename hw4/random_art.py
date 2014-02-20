# -*- coding: utf-8 -*-
"""
Edited on Feb 18 2014

@author: Claire E Beery
"""

from random import randint
from math import sin, cos, pi
import Image

def build_random_function(min_depth, max_depth):
    """ generates a nested list that describes a composite function in the 
    form of ['function', argument 1, argument 2] where each argument can be 
    a function
    
    possible component functions: sin(pi*a), cos(pi*a), a*b, (a-b)/2, a**2
    
    inputs: min_depth,  describes the smallest amount of nesting any branch 
                        of the composite function should have
            max_depth,  describes the largest amount of nestinng any branch 
                        of the composite function can have 
    
    """

    if min_depth > 1:   #add layers until minimum depth is achieved
        return recurse(min_depth,max_depth)
    else:
        depth = randint(1,max_depth)    # assign random depth to check against
        
        if depth == 1:  #is assigned depth is reached, end branch
            return base()
        else:           # else add more branches/depth
            return recurse(min_depth,max_depth) 


def base():
    """creates the base case for build_random_function"""
    
    operations = ["x","y"]
    end_op = operations[randint(0,1)] #picks x or y for the base input 
    
    return end_op
    
def recurse(min_depth, max_depth):
    """impliments the recursion of build_random_function"""
    
    # creates a list of possible functions 
    ops = ["prod","diff_halves","sin_pi","cos_pi","squared"] 
    
    #picks a function to use 
    nxt_op_index = randint(0,4)
    nxt_op = ops[nxt_op_index]
    
    # creates first input for function (recursive of build_random_function)
    firstInput = build_random_function(min_depth -1, max_depth -1)

    # if function needs more than 1 input is needed, create it
    # return the chosen function and its inputs
    if nxt_op_index == 0 or nxt_op_index == 1:       
        secondInput = build_random_function(min_depth -1, max_depth -1)
        return [nxt_op,firstInput,secondInput]
    else:
        return [nxt_op,firstInput]
    
def evaluate_random_function(f, x, y):
    """ evaluates the value of a multiple layer composite function 
    
    possible component functions: sin(pi*a), cos(pi*a), a*b, (a-b)/2, a**2, x, y
    
    inputs: f, the composite function in the form of ['function', argument 1, argument 2]
            x, value of the base function x
            y, value of the base function y
    """
    
    # unpack f
    function = f[0]

    #base
    if function == "x":
        return x
    elif function == "y":
        return y
    else:          

        # find input values
        input1 = evaluate_random_function(f[1],x,y)        
        if len(f) == 3: # if input2 exists
            input2 = evaluate_random_function(f[2],x,y) 
    
        #function definitions
        if function == "prod":
            return input1*input2
        elif function == "diff_halves":
            return (input1 - input2) / 2.0
        elif function == "sin_pi":
            return sin(input1*pi)
        elif function == "cos_pi":
            return cos(input1*pi)
        elif function == "squared":
            return input1**2

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        inputs: val, value to be remapped
                input_interval_start, min of starting range
                input_interval_end, max of starting range
                output_interval_start, min of desired range
                output_interval_end, max of desired range
    """
    
    val = val - input_interval_start
    val = val / (input_interval_end - input_interval_start)
    val = val * (output_interval_end - output_interval_start)
    val = val + output_interval_start
    
    return val
    
    
   # name compliments of "A Funny Thing Happened on the Way to the Forum" 
   # come see the FWOP performance the 20th, 21st, 27th, or 28th at Sorenson 
   # theater
   
   
def pretty_little_picture():   
    # build functions for the primary colors
    blue = build_random_function(3,7)
    red = build_random_function(3,7)
    green = build_random_function(3,7)
    
    # create an empty color image using PIL 
    img_size = 350
    im = Image.new("RGB",(img_size,img_size))

    for i in range(0,img_size -1):
        x = remap_interval(i,0.0,img_size -1.0,-1.0,1.0)
        for k in range(0,img_size -1):
            y = remap_interval(i,0.0,img_size-1.0,-1.0,1.0)
            
            # find individual color values
            b = evaluate_random_function(blue, x, y)
            r = evaluate_random_function(red, x, y)
            g = evaluate_random_function(green, x, y)
            
            # remap to color scale
            b = int(remap_interval(b,0.0,img_size-1,0.0,255.0))
            r = int(remap_interval(r,0.0,img_size-1,0.0,255.0))
            g = int(remap_interval(g,0.0,img_size-1,0.0,255.0))
    
            # set pixels
            im.putpixel((i,k), (r,g,b))
      
    im.save("image.bmp")      
            
if __name__ == '__main__':
    pretty_little_picture()
    