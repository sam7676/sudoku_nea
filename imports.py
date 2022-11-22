from time import perf_counter
import os
from PIL import Image
from PIL import ImageGrab
from PIL import ImageTk
import random
import cv2
import tensorflow as tf
import numpy as np
import clipboard
import pyautogui as pg                          # This for some reason modifies the font
from itertools import product
import statistics
import tkinter as tk
from tkinter.filedialog import askopenfilename
import sqlite3
from datetime import date
from tkinter import font

img_size = 500                  #size of potential grids
digit_size = img_size//10       #size of potential digits
split_rate = 0.8                #splitting training and test data of NN
pval = 0.999                    #minimal probability for a grid prediction to be accurate
meanpval =0.5                   #mean of 5 items, if lower then terminate grid selection
img_set = 5                     #size of stack for taking the mean of
epoch_rate = 15                 #number of iterations of neural network training
gen_difficulty = [[0,1],[30,1],[100,2],[250,3]]
grid_model_location =   'models\\grid_model.h5'
digit_model_location =  'models\\digit_model.h5'
grid_location =         'grids'
digit_location =        'digits'
image_location =        'images'
img_logo =              'images\\logo.png'
img_lb =                'images\\leaderboard.png'
img_optns =             'images\\options.png'
img_upload =            'images\\upload.png'
img_win =               'images\\win.png'
img_debug =             'images\\debug.png'
img_generate =          'images\\generate.png'
img_1x1 =               'images\\1x1.png'
img_custom =            'images\\custom.png'
database_location =     'leaderboard.sqlite3'

move_dict = {
    1:'Hint: One note only',
    2:'Hint: Partner',
    3:'Hint: Bowman',
    4:'Hint: Remove note',
}

def resize_images(image,img_size):

    #resizes image and returns image and whether it has been modified or not

    if type(image)==str:
        if '.png' in image or '.jpg' in image or '.jpeg' in image or '.gif' in image:
            img = Image.open(image)
        else:
            img = ImageGrab.grabclipboard()
    else:
        img = image
    width = img.width
    height = img.height
    
    if not(height==width and height==img_size):
        if height>width:
            new_width = int(round(width/(height/img_size)))
            img = img.resize((new_width,img_size))

            extra = (img_size-new_width)//2
            new_img = Image.new('RGB',(img_size,img_size), (0,0,0))
            new_img.paste(img,(extra,0))
        else:
            new_height = int(round(height/(width/img_size)))
            img = img.resize((img_size,new_height))

            extra = (img_size-new_height)//2
            new_img = Image.new('RGB',(img_size,img_size), (0,0,0))
            new_img.paste(img,(0,extra))

        return [new_img,True]
    else:
        return [img,False]

def resize_stretch(image,img_size):
    if type(image)==str:
        if '.png' in image or '.jpg' in image or '.jpeg' in image or '.gif' in image:
            img = Image.open(image)
        else:
            img = ImageGrab.grabclipboard()
    else:
        img = image
    
    if img.size==(img_size,img_size):
        return [img,False]
    return [img.resize((img_size,img_size)),True]

def get_name():
    #generates random name for file
    s=''
    for i in range(16):
        s+=chr(random.randint(65,90))
    return s

def flatten(inp):
    #if any spaces are in given string, removes them and returns new string
    text = ''
    for i in inp:
        if i != ' ':
            text+=i
    return text

def expand(inp):
    #Adds regular spaces to string interpreted as 1D grid, to make it more readable
    a=''
    for i in range(len(inp)):
        a+=inp[i]
        if i%3==2:
            a+=' '
    return a

' list of subroutines:  '

' converter.py:                     '
# convert.init(inp)                 -> uses object detection network, returns grid string                    
# convert.train(solution)           -> saves digits to digit folder and grid to grid folder if saving allowed  

' database.py:                      '
# add_result(name,grid,date,time)   -> adds result in shown format to SQL table                       
# search_result(name,grid)          -> returns SQL query for the name and/or the grid. First 15 items  
# clear_table()                     -> deletes and creates SQL table, effectively wiping it 

' front.py:                         '
# front_end.init()                  -> initiates front end of program           

' imports.py                        '
# resize_images(image,img_size)     -> returns new image and whether resize has taken place or not      
# resize_stretch(image,img_size)    -> returns new image and whether resize has taken place or not      
# get_name()                        -> returns random string of 16 characters used for naming conventions 
# flatten(inp)                      -> returns string and removes all spaces from string for formatting   
# expand(inp)                       -> returns string and adds spaces to string for readability             

' solver.py                         '
# create_grid(nums,complex)         -> returns grid object (2D if complex=False, 3D if complex=True)       
# print_grid(grid)                  -> prints grid from either either 3D object or string                
# export_answer(grid)               -> converts grid object to string export (2D or 3D)                        
# store_grid(grid)                  -> returns duplicate grid object that                                        
# constraint.init(nums)             -> uses constraint solver and returns string answer         
# constraint.next_move(nums)        -> given grid input, returns appended grid and hint array    
# algorithm_x.init(nums)            -> initiates algorithm x solver
# generate.init()                   -> returns valid grid in string form  

' training.py                       '
# train_grid()                      -> trains grid model from grid images in folder     
# train_digits()                    -> trains digit model from digit images in folder  

' useful attributes                 '
# convert.saving                    -> whether saving is allowed for current converter object
# convert.ans                       -> conversion results (string)
# convert.img                       -> most accurate grid image
# constraint.ans                    -> constraint solver answer (string)
# constraint.moves                  -> constraint move list (array) [ID, y, x, old, new, layers]
# algorithm_x.sols                  -> algorithm x number of solutions
# generate.ans                      -> generated grid (string)

