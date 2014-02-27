# -*- coding: utf-8 -*-
"""
Edited on Feb 18 2014

@author: Claire E Beery
"""

from random import randint
from math import sin, cos, pi
import Image


## SS: Rather than having the recurse() method and the build_random_function() method, you could
##     have one build_random_function() method that calls itself in order to build up a function
##     if you're interested, here's an example:
## 
# xy_options = ["x", "y"]
# function_options = [["prod", 2],["cos_pi", 1],["sin_pi", 1],["cube", 1],["reverse", 1]]
# def build_random_function(min_depth, max_depth):
#     if max_depth == 0 or (min_depth == 0 and randint(0,1) == 1):
#         return [xy_options[randint(0,1)]]
#     else: 
#         selected_function = function_options[randint(0,4)]
#         if selected_function[1] == 1:
#             return [selected_function[0], build_random_function(min_depth - 1, max_depth - 1)]
#         elif selected_function[1] == 2:
#             return [selected_function[0], build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]

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
    
## SS: Passed my tests :)
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

## SS: Failed 2 of my tests:
# FAILED - remap_interval_unit_tests()
#     Test 1 FAILED: 
#         Input value: 175
#         Input range: [0, 350]
#         Output range: [-1, 1]
#         Expected Output: 0.0
#         Actual Output: -1
#     Test 4 FAILED: 
#         Input value: 0
#         Input range: [-1, 1]
#         Output range: [0, 255]
#         Expected Output: 127.5
#         Actual Output: 0
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
    
    # val = val - input_interval_start
    # val = val / (input_interval_end - input_interval_start)
    # val = val * (output_interval_end - output_interval_start)
    # val = val + output_interval_start
    
    # return val

    slope = (float(output_interval_end) - float(output_interval_start))/(float(input_interval_end) - float(input_interval_start))
    return slope * (val - float(input_interval_start)) + float(output_interval_start)
    
    
   # name compliments of "A Funny Thing Happened on the Way to the Forum" 
   # come see the FWOP performance the 20th, 21st, 27th, or 28th at Sorenson 
   # theater
   
## SS: You know what this function reminds me of? Pretty Little Liars :) and yes, I watch it :) 
def pretty_little_picture():   
    # build functions for the primary colors
    blue = build_random_function(3,7)
    red = build_random_function(3,7)
    green = build_random_function(3,7)
    
    # create an empty color image using PIL 
    img_size = 350
    im = Image.new("RGB",(img_size,img_size))

    for i in range(0,img_size -1):
        x = remap_interval(i,0,img_size -1,-1,1)
        for k in range(0,img_size -1):
            y = remap_interval(i,0,img_size-1,-1,1)
            
            # find individual color values
            b = evaluate_random_function(blue, x, y)
            r = evaluate_random_function(red, x, y)
            g = evaluate_random_function(green, x, y)
            
            # remap to color scale
            b = remap_interval(b,0,img_size-1,0,255)
            r = remap_interval(r,0,img_size-1,0,255)
            g = remap_interval(g,0,img_size-1,0,255)
    
            # set pixels

            ## SS: the line below gave me errors, this is the correct implementation (at least for me):
            ##     im.putpixel([i,k], (int(r),int(g),int(b)))   

            im.putpixel((i,k), [r,g,b])
      
    im.show()      
            
## SS: All of the images that I saw were completely black. This does not appear to be working correctly.
if __name__ == '__main__':
    pretty_little_picture()
    