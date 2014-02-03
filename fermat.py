# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 01:03:20 2014

@author: cbeery
"""
#assumes a,b, and c are integers
def check_fermat(a,b,c,n):
    x = a**n + b**n
    c_n = c**n
    
    if (x == c_n) and (n>2):
        print("Holy Smokes! Fermat was wrong!")
    else:
        print("No, that doesn't work.")
        
#ask user for inputs
def ask_for_fermat():
    prompt = "Please type an integer for "
    prompt2 = " and press enter."
    
    a = raw_input(prompt + "a" + prompt2)
    b = raw_input(prompt + "b" + prompt2)
    c = raw_input(prompt + "c" + prompt2)
    n = raw_input(prompt + "n" + prompt2)
    
    a = int(a)
    b = int(b)
    c = int(c)
    n = int(n)
    
    return (a, b, c, n)

##
a,b,c,n = ask_for_fermat()
check_fermat(a,b,c,n)