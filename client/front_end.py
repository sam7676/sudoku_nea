from solver import *

from time import perf_counter
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
import random
import clipboard
import pyautogui as pg                          # This for some reason modifies the font
import tkinter as tk
from tkinter.filedialog import askopenfilename
from datetime import date
from tkinter import font
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import threading

import socketio

import object_detection


image_location =        'images'
img_logo =              'images\\logo.png'
img_lb =                'images\\leaderboard.png'
img_optns =             'images\\options.png'
img_upload =            'images\\upload.png'
img_win =               'images\\win.png'
img_train =             'images\\train.png'
img_generate =          'images\\generate.png'
img_1x1 =               'images\\1x1.png'
img_custom =            'images\\custom.png'

pval = 0.95



gen_difficulty = [[0,1],[30,1],[100,2],[250,3]]
move_dict = {
    "One note":'Hint: One note only',
    "Partner":'Hint: Partner',
    "Bowman":'Hint: Bowman Bingo',
    "Remove":'Hint: Remove note',
}

def get_row(grid,y1):
    return [[grid[y1][0],y1,0],[grid[y1][1],y1,1],[grid[y1][2],y1,2],[grid[y1][3],y1,3],[grid[y1][4],y1,4],[grid[y1][5],y1,5],[grid[y1][6],y1,6],[grid[y1][7],y1,7],[grid[y1][8],y1,8]]
def get_col(grid,x1):
    return [[grid[0][x1],0,x1],[grid[1][x1],1,x1],[grid[2][x1],2,x1],[grid[3][x1],3,x1],[grid[4][x1],4,x1],[grid[5][x1],5,x1],[grid[6][x1],6,x1],[grid[7][x1],7,x1],[grid[8][x1],8,x1]]
def get_box(grid,y1,x1):
    modY = y1%3
    modX = x1%3
    return [[grid[y1-(modY)][x1-(modX)],y1-(modY),x1-(modX)],[grid[y1-(modY)][x1-(modX)+1],y1-(modY),x1-(modX)+1],
            [grid[y1-(modY)][x1-(modX)+2],y1-(modY),x1-(modX)+2],[grid[y1-(modY)+1][x1-(modX)],y1-(modY)+1,x1-(modX)],
            [grid[y1-(modY)+1][x1-(modX)+1],y1-(modY)+1,x1-(modX)+1],[grid[y1-(modY)+1][x1-(modX)+2],y1-(modY)+1,x1-(modX)+2],
            [grid[y1-(modY)+2][x1-(modX)],y1-(modY)+2,x1-(modX)],[grid[y1-(modY)+2][x1-(modX)+1],y1-(modY)+2,x1-(modX)+1],
            [grid[y1-(modY)+2][x1-(modX)+2],y1-(modY)+2,x1-(modX)+2]]




def convert(): pass
def clear_table(): pass
def search_result(): pass   
def add_result(): pass
def train(): pass


widget_width = 29
widget_height = 2
widget_relief = tk.RAISED
widget_font = None
widget_title_font = None
widget_foreground = '#5B0000'


# Attempt to connect to server. If not, offline mode
# Attempt to login and skip
# Menu screen with Play offline, Login, Register


# Custom function, applying a default style to Tkinter widgets
def grid(widget, row=0, col=0, 
                font_type=None, width=29, height=2, 
                relief=tk.RAISED, foreground='#5B0000'):
    """
    Applies a default style to a Tkinter widget.

    Args:
        widget (tk.Widget): The widget to apply the style to.
        row (int): The row position of the widget in the grid.
        col (int): The column position of the widget in the grid.
        font_type (str): The font style to apply to the widget.
                         Valid values are 'title' or 'regular'.
        width (int): The width of the widget.
        height (int): The height of the widget.
        relief (tk.constants.RELIEF_CONSTANT): The relief style of the widget.
        foreground (str): The foreground color of the widget.
    """
    # Set up default font styles
    regular_font = font.Font(family="TkDefaultFont",size=11,weight="normal")
    title_font = font.Font(family="TkDefaultFont",size=12,weight="normal")
    cell_font = font.Font(family="TkDefaultFont",size=25,weight="normal")

    # Determine the font style to apply to the widget
    if font_type == None:
        font_style = regular_font
    elif font_type == 'title':
        font_style = title_font
    elif font_type == 'cell':
        font_style = cell_font

    # Apply the style to the widget
    if isinstance(widget, (tk.Label, tk.Button, tk.Text)):
        widget.configure(font=font_style, width=width, height=height, relief=relief, fg=foreground)
    elif isinstance(widget, tk.Entry):
        widget.configure(width=width, relief=relief, fg=foreground)

    # Place the widget in the grid
    widget.grid(row=row, column=col)
    



class front_end:

    # Initialises the application
    def __init__(self):

        #Create window
        self.win=tk.Tk()
        self.win.resizable(False, False)
        
        #Get access token
        token = open('client/access_token.txt','r').readline()

        #Configure app login options
        self.online_mode = True
        self.playerID = None

        #Attempt to login
        try:
            #Generate socket to connect to server
            self.socket = socketio.SimpleClient()
            self.socket.connect('http://localhost:5000')

            # Attempting to validate token and verify login
            self.socket.emit('check_token', {"token":token})
            result = self.socket.receive()

            # Parsing JSON to receive potential player ID
            result = result[1]["result"]

            if result is not None:
                self.playerID = result

        except:
            self.socket = None
            self.online_mode = False


        #Login, or go offline mode
        if self.online_mode == False or self.playerID is not None:
            self.screen_home()

        self.screen_menu()
        plt.ion()

    # Function for clearing the window and restarting it
    def reset_window(self):
        self.win.destroy()
        self.win = tk.Tk()
        self.win.title('')
        self.win.resizable(False, False)
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        self.win.iconphoto(False, o1x1_logo)



    # Menu screen for anyone not able to automatically login
    def screen_menu(self):
        self.reset_window()

        offline_screen_button = tk.Button(text="Play offline", command=self.offline_transition)
        grid(offline_screen_button, row=0)


        login_screen_button = tk.Button(text="Login", command=self.screen_login)
        grid(login_screen_button,row=1)

        register_screen_button = tk.Button(text="Register", command=self.screen_register)
        grid(register_screen_button,row=2)

        self.win.mainloop()

    # Used to trigger offline mode
    def offline_transition(self):
        self.online_mode = False
        self.socket.disconnect()
        self.screen_home()

    # Login screen
    def screen_login(self):

        self.reset_window()
        
        login_label = tk.Label(text="Login")
        grid(login_label, row=0)

        username_label = tk.Label(text='Username:')
        self.username_input = tk.Entry()

        grid(username_label, row=1, col=0)
        grid(self.username_input, row=1, col=1)
        
        password_label = tk.Label(text="Password:")
        self.password_input = tk.Entry()

        grid(password_label, row=2, col=0)
        grid(self.password_input, row=2, col=1)

        
        submit_button = tk.Button(text="Go", command=self.attempt_login)
        grid(submit_button, row=3, col=0)

        back_button = tk.Button(text="Back",command=self.screen_menu)
        grid(back_button, row=3, col=1)

        self.win.mainloop()

    # Helper function for screen_login
    def attempt_login(self):

        username = self.username_input.get()
        password = self.password_input.get()

        # Attempting to login
        self.socket.emit('attempt_login', {"username":username, "password":password})
        json = self.socket.receive()[1]

        playerID = json["id"]
        token = json["token"]

        if playerID is not None:
            self.playerID = playerID

            token_file = open('client/access_token.txt','w')
            token_file.write(token)
            token_file.close()
            self.screen_home()

    # Register screen
    def screen_register(self):
        self.reset_window()

        username_label = tk.Label(text="Username")
        self.username_input = tk.Entry()

        grid(username_label, row=0, col=0)
        grid(self.username_input, row=0, col=1)

        password_label = tk.Label(text="Password")
        self.password_input = tk.Entry()

        grid(password_label, row=1, col=0)
        grid(self.password_input, row=1, col=1)

        register_button = tk.Button(text="Register", command=self.attempt_register)

        grid(register_button, row=2, col=0)

        back_button = tk.Button(text="Back", command=self.screen_menu)
        
        grid(back_button, row=2, col=1)

        self.win.mainloop()

    # Helper function for screen_register
    def attempt_register(self):

        username = self.username_input.get()
        password = self.password_input.get()

        # Attempting to register
        self.socket.emit('attempt_login', {"username":username, "password":password})
        json = self.socket.receive()[1]

        playerID = json["id"]
        token = json["token"]

        if playerID is not None:
            self.playerID = playerID

            token_file = open('client/access_token.txt','w')
            token_file.write(token)
            token_file.close()
            self.screen_home()




    # Home page
    def screen_home(self):
        self.reset_window()

       
        play_button = tk.Button(text="Play", command=self.screen_play_options)


        grid(play_button, row=0)

        if self.online_mode:

            multiplayer_button = tk.Button(text="Multiplayer", command=self.screen_multiplayer)

            leaderboard_button = tk.Button(text="Leaderboard", command=self.screen_leaderboard)

            log_out_button = tk.Button(text="Log out", command=self.log_out)

            grid(multiplayer_button, row=1)
            grid(leaderboard_button, row=2)
            grid(log_out_button, row=3)

        exit_button = tk.Button(text="Exit", command=self.win.destroy)

        grid(exit_button, row=4)

        self.win.mainloop()

    # Helper function to log out of account
    def log_out(self):

        # Clearing the access token ID
        file = open('client/access_token.txt','w')
        file.write('')
        file.close()

        self.playerID = None
        self.screen_menu()
        

    # Play options
    def screen_play_options(self): 

        self.reset_window()

        create_custom_button = tk.Button(text="Create custom game", command=self.screen_create_custom_game)
        generate_button = tk.Button(text="Generate grid", command=self.s_generate)
        upload_button = tk.Button(text="Upload image", command=self.screen_upload)
        back_button = tk.Button(text="Back", command=self.screen_home)

        grid(create_custom_button, row=0)
        grid(generate_button, row=1)
        grid(upload_button, row=2)
        grid(back_button, row=3)

        self.win.mainloop()


    # Creating a custom grid to play
    def screen_create_custom_game(self):
        self.reset_window()

        grid_frame = tk.Frame()

        self.build_entry_grid(grid_frame)
            
        button_frame = tk.Frame()
            
        back_button = tk.Button(text="Back", command=self.screen_play_options, master=button_frame)
        confirm_button = tk.Button(text="Confirm", command=self.check_valid_grid_creation, master=button_frame)


        grid(back_button, row=0, col=0)
        grid(confirm_button, row=0, col=1)

        grid(grid_frame, row=0)
        grid(button_frame, row=1)


        self.win.mainloop()



    def build_entry_grid(self, grid_frame):
        subgrid_frames = [tk.Frame(master=grid_frame) for i in range(9)]

        self.entries = []

        for y in range(9):
            for x in range(9):
                box_value = 3 * (y//3) + (x//3)
                self.entries.append(tk.Text(master=subgrid_frames[box_value]))
                
        for i, item in enumerate(self.entries):
            y = i//9
            x = i%9
            grid(item, row=y%3, col=x%3, width=2, height=1, font_type='cell')

        for i, subgrid in enumerate(subgrid_frames):
            subgrid.grid(row=i//3,
                         column=i%3,
                         padx=5,
                         pady=5)


    def screen_upload(self):
        self.reset_window()


        self.open_file_button = tk.Button(text='Open file',command=self.open_image_file)
        grid(self.open_file_button, row=0, col=0)

        back_button = tk.Button(text="Back", command=self.screen_play_options)
        grid(back_button, row=1, col=0)

        self.win.mainloop()


    def open_image_file(self):

        """
        Opens a file dialog and displays the upload screen if a file is selected.
        """
        try:
            file_path = askopenfilename()
            image = Image.open(file_path)
            self.screen_check_grid_model(image)
            
        except FileNotFoundError:
            self.open_file_button["fg"]='#FF0000'
            print("File not found")
        


    def screen_check_grid_model(self, image):

        self.reset_window()

        # Sizing down image (width and height max 1080)
        image_width = image.width
        image_height = image.height

        max_size = 1440

        if image_width > image_height:
            width = max_size
            height = int(round(image_height * width / image_width))

        else:
            height = max_size
            width = int(round(image_width * height / image_height))
        
        resized_image = image.resize((width, height))
        imageTk = ImageTk.PhotoImage(resized_image)

        # Building canvas and assigning events
        self.canvas= tk.Canvas(width=width, height=height)
        self.canvas.create_image(0, 0, image=imageTk, anchor="nw")
        
        self.canvas.bind("<Button-1>", self.left_click_canvas)
        self.canvas.bind("<Button-3>", self.right_click_canvas)

        grid(self.canvas, row=0, col=0)

        # Canvas variables (for drawing on canvas)
        self.left_canvas_cords = None
        self.right_canvas_cords = None
        self.identifiers = []

        # Getting initial image bounds if possible
        bounds = object_detection.process_canvas(resized_image, 'bounds')
        if bounds is not None:
            x1, y1, x2, y2 = bounds

            self.left_canvas_cords = (x1, y1)
            self.right_canvas_cords = (x2, y2)
        
        self.make_rectangle_canvas()
        

        # Confirm and back buttons
        confirm_back_frame = tk.Frame()
        
        back_button = tk.Button(master=confirm_back_frame, text="Back", command = self.screen_upload)
        self.confirm_button = tk.Button(master=confirm_back_frame, text="Confirm", command= lambda: self.screen_check_digit_model(resized_image)) 

        grid(confirm_back_frame, row=1)
        grid(back_button, row=0, col=0)
        grid(self.confirm_button, row=0, col=1)

        self.win.mainloop()


    def left_click_canvas(self, event):
        x, y = event.x, event.y
        self.left_canvas_cords = (x,y)
        self.make_rectangle_canvas()

    def right_click_canvas(self, event):
        x, y = event.x, event.y
        self.right_canvas_cords = (x,y)
        self.make_rectangle_canvas()
        

    def make_rectangle_canvas(self):
        """
        Update the canvas with a rectangle that represents the coordinates of the user's clicks.
        If the user has clicked twice, the rectangle will be drawn between the two clicks.
        If the user has clicked once, a small pixel will be drawn around the click.
        """

        # Clear previous rectangles
        for identifier in self.identifiers:
            self.canvas.delete(identifier)

        # Update coordinates to ensure max
        if self.left_canvas_cords and self.right_canvas_cords:

            x1 = min(self.left_canvas_cords[0], self.right_canvas_cords[0])
            y1 = min(self.left_canvas_cords[1], self.right_canvas_cords[1])

            x2 = max(self.left_canvas_cords[0], self.right_canvas_cords[0])
            y2 = max(self.left_canvas_cords[1], self.right_canvas_cords[1])

            self.left_canvas_cords = (x1, y1)
            self.right_canvas_cords = (x2, y2)

            # Draw rectangle between the two clicks
            self.identifiers.append(self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="", outline="red", width=2
            ))

        if self.left_canvas_cords:
            # Draw small rectangle around left click
            left_change = (self.left_canvas_cords[0] - 3, self.left_canvas_cords[1] - 3,
                           self.left_canvas_cords[0] + 3, self.left_canvas_cords[1] + 3)
            
            self.identifiers.append(self.canvas.create_rectangle(
                left_change, fill="green", width=2, outline="green"
            ))

        if self.right_canvas_cords:
            # Draw small rectangle around right click
            right_change = (self.right_canvas_cords[0] - 3, self.right_canvas_cords[1] - 3,
                            self.right_canvas_cords[0] + 3, self.right_canvas_cords[1] + 3)

            self.identifiers.append(self.canvas.create_rectangle(
                right_change, fill="blue", width=2, outline="blue"
            ))


    def screen_check_digit_model(self, image):

        if self.left_canvas_cords is None or self.right_canvas_cords is None:
            self.confirm_button["fg"] = '#ff0000'
            return

        # Crop image
        x1, y1 = self.left_canvas_cords
        x2, y2 = self.right_canvas_cords

        grid_image = image.crop((x1, y1, x2, y2))

        grid_string = object_detection.process_grid(grid_image)

        self.reset_window()

        images_frame = tk.Frame()
        grid_frame = tk.Frame(master = images_frame)

        self.build_entry_grid(grid_frame)

        for i, guess in enumerate(grid_string):
            if guess != '0':          
                self.entries[i].insert("1.0", guess)

        resized_image = grid_image.resize((570, 570))

        tk_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(master=images_frame, image=tk_image)


        grid(images_frame, row=0, col=0)
        grid(grid_frame, row=0, col=0)


        # Need to manually grid images
        image_label.grid(row=0, column=1)


        button_frame = tk.Frame()

        back_button = tk.Button(text="Back", master=button_frame, command=self.screen_upload)
        self.confirm_button = tk.Button(text="Confirm", master=button_frame, command= self.check_valid_grid_creation)

        grid(back_button, row=0, col=0)
        grid(self.confirm_button, row=0, col=1)
       
        grid(button_frame, row=1, col=0)

        

        
        self.win.mainloop()



    def s_game(self,grid):
        #Setting up constraint solver for next move function
        self.game_solution = constraint(grid)
        self.grid_input = grid
        self.hints =0
        self.errors = 0
        
        #Creating window and frames
        self.win.destroy()
        self.win = tk.Tk()
        self.win.title('')
        self.win.resizable(False, False)
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        self.win.iconphoto(False, o1x1_logo)
        frame1 = tk.Frame()
        frame2 = tk.Frame()
        hint_frame = tk.Frame()
        misc_frame = tk.Frame()
        frame3 = tk.Frame()

        #Style
        cell_width = 6
        cell_height = 3
        hint_label_w = 25
        button_w = 12
        used_num_w = 5
        game_relief = tk.RAISED

        #Fonts and text sizes
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
        f_button = font.Font(family="TkDefaultFont",size=11,weight="normal")
        f_label = font.Font(family="TkDefaultFont",size=17,weight="normal")
        f_num = font.Font(family="TkDefaultFont",size=11,weight="normal")

        #Creating grid
        sg=[tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1)]
        self.entries = [tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main)]
        for i,item in enumerate(self.entries):
            y1 = i//9
            x1 = i%9
            item.grid(row=y1%3,column=x1%3)                
        for i, sub in enumerate(sg):
            sub.grid(row=i//3,column=i%3,padx=5,pady=5)
        
        #Placing uneditable labels where possible
        for i, item in enumerate(self.entries):
            if grid[i]!='0':
                y1 = i//9
                x1 = i%9
                self.entries[i].config(state=tk.DISABLED)
                self.entries[i] = tk.Label(text=f"{grid[i]}",master=item.master,width=3,bg='#ffffff',font=f_label)
                self.entries[i].grid(row=y1%3,column=x1%3)

        #Extra functions
        self.checkB = tk.Button(master=frame2,text='Check',command=lambda: self.f_get_hint(False),
            width=button_w,font=f_button)
        self.hintB = tk.Button(master=frame2,text='Hint',command=lambda: self.f_get_hint(True),
            width=button_w,font=f_button)
        self.solveB = tk.Button(master=frame2,text='Solve',command=self.f_solve_game,
            width=button_w,font=f_button)
        backB = tk.Button(master=frame2,text='Back',command=self.screen_play_options,
            width=button_w,font=f_button)
        self.checkB.grid(row=0,column=0)
        self.hintB.grid(row=0,column=1)
        self.solveB.grid(row=0,column=2)
        backB.grid(row=0,column=3)

        #Extra functions 2
        self.hintLabel = tk.Label(text='Hint: None',master=hint_frame,
            width=hint_label_w,font=f_button,relief=game_relief)
        self.hints_used_label = tk.Label(text=f'Hints used: {self.hints}',master=hint_frame,
            width=hint_label_w,font=f_button,relief=game_relief)
        clear_grid_B = tk.Button(text='Clear grid',master=misc_frame,command=self.f_clear_grid,
            width=hint_label_w,font=f_button,relief=game_relief)
        self.errors_made_label = tk.Button(text=f'Errors: {self.errors}',master=misc_frame,
            width=hint_label_w,font=f_button,relief=game_relief)

        #Used numbers labels
        self.usedNumLabels = [tk.Button(master=frame3,height=2,text='1',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='2',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='3',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='4',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='5',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='6',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='7',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='8',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='9',relief=game_relief,width=used_num_w,font=f_num)]
        for i in range(len(self.usedNumLabels)):
            self.usedNumLabels[i].grid(row=0,column=i)

        #GUI stuff
        frame1.grid(row=0,column=0)
        frame2.grid(row=1,column=0)
        hint_frame.grid(row=2,column=0)
        self.hintLabel.grid(row=0,column=0)
        self.hints_used_label.grid(row=0,column=1)
        misc_frame.grid(row=3,column=0)
        clear_grid_B.grid(row=0,column=0)
        self.errors_made_label.grid(row=0,column=1)
        frame3.grid(row=4)

        #Timer and window set-up
        self.timer_start = perf_counter()
        self.win.mainloop()

    def s_leaderboard(self):
        #Create window and set style
        self.win.destroy()
        self.win = tk.Tk()
        self.win.title('')
        self.win.resizable(False, False)
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        self.win.iconphoto(False, o1x1_logo)
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
        name_w = 16
        grid_w = 20

        #Leaderboard image and frames
        leaderboard_image = ImageTk.PhotoImage(Image.open(img_lb))
        leaderboardL = tk.Label(image=leaderboard_image)
        frame1 = tk.Frame()
        miniFrame1 = tk.Frame(master=frame1)
        miniFrame2 = tk.Frame(master=frame1)

        #Search frames
        searchNameB = tk.Label(master=miniFrame1,text='Search name',font=f_main,width=name_w)
        self.searchNameE = tk.Entry(master=miniFrame1,width=name_w)
        searchGridB = tk.Label(master=miniFrame1,text='Search grid',font=f_main,width=grid_w)
        self.searchGridE = tk.Entry(master=miniFrame1,width=grid_w)
        searchB = tk.Button(text='Search',command=self.f_return_query,master=miniFrame2,height=2,font=f_main,width=14)
        backB = tk.Button(text='Back',command=self.screen_home,master=miniFrame2,height=2,font=f_main,width=14)

        #GUI stuff
        leaderboardL.grid(row=0)
        frame1.grid(row=1)
        searchNameB.grid(row=0,column=0)
        self.searchNameE.grid(row=1,column=0)
        searchGridB.grid(row=0,column=1)
        self.searchGridE.grid(row=1,column=1)
        searchB.grid(row=0,column=0)
        backB.grid(row=0,column=1)
        miniFrame1.grid(row=0,column=0)
        miniFrame2.grid(row=0,column=1)
        self.query_frame = tk.Frame()
        self.win.mainloop()

    def s_generate(self):
        #Create window and style
        self.win.destroy()
        self.win = tk.Tk()
        self.win.title('')
        self.win.resizable(False, False)
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        self.win.iconphoto(False, o1x1_logo)
        f_main = font.Font(family="TkDefaultFont",size=11,weight="normal")
        w=41

        #Set frame and image
        generate_image = ImageTk.PhotoImage(Image.open(img_generate))
        generateL = tk.Label(image=generate_image)
        diff_frame = tk.Frame()        
        

        #Generate buttons
        diff_array = [tk.Button(master=diff_frame,text='Level 1',width=w,font=f_main,height=2,command=lambda:self.s_game(generate(gen_difficulty[0]).ans)),
                      tk.Button(master=diff_frame,text='Level 2',width=w,font=f_main,height=2,command=lambda:self.s_game(generate(gen_difficulty[1]).ans)),  
                      tk.Button(master=diff_frame,text='Level 3',width=w,font=f_main,height=2,command=lambda:self.s_game(generate(gen_difficulty[2]).ans)),  
                      tk.Button(master=diff_frame,text='Level 4',width=w,font=f_main,height=2,command=lambda:self.s_game(generate(gen_difficulty[3]).ans)),]
        for i in range(len(diff_array)):
            diff_array[i].grid(row=i)

        #Other buttons and GUI
        backB = tk.Button(text='Back',font=f_main,width=w,command=self.screen_play_options,height=2)
        generateL.grid(row=0)
        diff_frame.grid(row=1)
        backB.grid(row=3)
        self.win.mainloop()

    def s_win(self):
        #Create window
        self.final_time = perf_counter() - self.timer_start
        self.final_grid = self.grid_input
        self.win_window = tk.Toplevel()
        self.win_window.title('')
        self.win_window.resizable(False, False)
        ww_o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        self.win_window.iconphoto(False, ww_o1x1_logo)

        #Style and image
        width1=48
        win_img = ImageTk.PhotoImage(Image.open(img_win),master=self.win_window)
        win_label = tk.Label(master=self.win_window,image=win_img)

        #Getting final minutes and seconds
        final_mins = int(self.final_time//60)
        final_secs = int(round(self.final_time%60))

        #Setting labels and buttons
        time_label = tk.Label(master=self.win_window,text=f'Time taken: {final_mins}m {final_secs}s',
            font=("TkDefaultFont","10"),width=width1)
        name_label = tk.Label(master=self.win_window,text='Enter name [max 16 characters]:',
            font=("TkDefaultFont","10"),width=width1)
        self.score_entry = tk.Entry(master=self.win_window,
            font=("TkDefaultFont","10"),width=width1)
        self.submit_button = tk.Button(master=self.win_window,text='Submit',command=self.f_submit_score,
            font=("TkDefaultFont","10"),width=width1)
        quit_button = tk.Button(master=self.win_window,text='Quit',command=self.win_window.destroy,
            font=("TkDefaultFont","10"),width=width1)
        error_total = tk.Label(master=self.win_window,text=f'Errors: {self.errors}',
            font=("TkDefaultFont","10"),width=width1)
        hint_total = tk.Label(master=self.win_window,text=f'Hints: {self.hints}',
            font=("TkDefaultFont","10"),width=width1)

        #GUI stuff
        win_label.grid(row=0)
        time_label.grid(row=1)
        error_total.grid(row=2)
        hint_total.grid(row=3)
        name_label.grid(row=4)
        self.score_entry.grid(row=5)
        self.submit_button.grid(row=6)
        quit_button.grid(row=7)
        self.win_window.mainloop()

    def check_valid_grid_creation(self):

        grid = []
        for entry in self.entries:
            grid.append(entry.get("1.0", tk.END).strip())


        #Checking that length = 1 in all cases and only 123456789 appear
        error_found = False
        for i, text in enumerate(grid):

            if len(text) == 0:
                grid[i] = '0'
                self.entries[i]['fg'] = '#000000' #All fine, reset colour

            else:
                if len(text) > 1 or text[0] not in '123456789':
                    self.entries[i]['fg'] = '#ff0000' #Mark it red to specify it needs changing
                    error_found = True

                else:
                    self.entries[i]['fg'] = '#000000' #All fine, reset colour
                    grid[i] = text[0]


        if not error_found:
    
            # checking only 1 solution to grid
            grid_string = ''.join(grid)

            result = algorithm_x(grid_string)

            if result.sols == 1:

                #Go to main game
                self.s_game(grid_string)
            
            #If more than 1 solution, use generator and proceed to game
            elif result.sols==2:


                difficulty = random.randint(0,len(gen_difficulty)-1)

                self.s_game(generate(gen_difficulty[difficulty],
                                     grid_string).ans)
                
            else:

                #Error - display using confirm button
                self.confirmB["fg"] = '#FF0000'
            

    def f_get_hint(self,hint=True):
        #Getting grid from entries (and sorting at the same time)
        f_label = font.Font(family="TkDefaultFont",size=17,weight="normal")
        grid=[]
        
        #Validating user input
        self.f_validate_grid()
        
        #Going through grid and adding to grid array
        for q,entry in enumerate(self.entries):
            if type(entry)==tk.Text:

                #Getting cell text, setting empty cell values to 0, adding contents to grid
                text2 = entry.get("1.0","end-1c")
                if text2=='':
                    text2='0'
                text2 = list(text2)
                for i in range(len(text2)):
                    text2[i] = int(text2[i])
                if text2[0]==0:
                    text2=[1,2,3,4,5,6,7,8,9]
                grid.append(text2)

            #If label, add label contents to grid
            elif type(entry)==tk.Label:
                self.entries[q]["fg"] = '#000000'
                self.entries[q]["bg"]= '#ffffff'
                self.entries[q].config(font=f_label)
                grid.append([int(entry["text"])])

        #making 2D grid 3D
        grid2 = []
        temp=[]
        for i in range(len(grid)):
            temp.append(grid[i])
            if i%9==8:
                grid2.append(temp)
                temp=[]

        #checking to see if grid already completed (if so terminate)
        complete=True
        for i in range(len(grid2)):
            for j in range(len(grid2[i])):
                if len(grid2[i][j])!=1 or str(grid2[i][j][0])!= self.game_solution.ans[9*i+j]:
                    complete=False
        if complete==True:

            #Placing uneditable labels where possible
            for i in range(len(grid2)):
                for j in range(len(grid2[i])):
                    if len(grid2[i][j])==1 and grid2[i][j][0]==int(self.game_solution.ans[9*i+j]) and type(self.entries[9*i+j])==tk.Text:
                        self.entries[9*i+j].delete("1.0","end")
                        self.entries[9*i+j].config(state=tk.DISABLED)
                        self.entries[9*i+j] = tk.Label(text=f"{str(grid2[i][j][0])}",master=self.entries[9*i+j].master,width=3,font=f_label)
                        self.entries[9*i+j]["bg"]='#ffffff'
                        self.entries[9*i+j].grid(row=i%3,column=j%3)
            
            #Removing available numbers
            for i in range(9):
                self.usedNumLabels[i]["text"]=' '

            #Disabling buttons
            self.checkB['fg']='#00ff00'
            self.hintB['fg']='#00ff00'
            self.solveB['fg']='#00ff00'
            self.checkB.configure(command=self.f_do_nothing)
            self.hintB.configure(command=self.f_do_nothing)
            self.solveB.configure(command=self.f_do_nothing)
            
            #Finishing game
            self.s_win()

        else:
            
            #Fetching new grid with only notes
            grid3 = []
            for q, entry in enumerate(self.entries):
                appended=False
                if type(entry)==tk.Text:
                    text = list(entry.get("1.0","end-1c"))
                    for i in range(len(text)-1,-1,-1):
                        if text[i]=='\n' or text[i]==' ':
                            text.pop(i)
                    grid3.append([int(i) for i in text])
                    appended=True
                if appended==False:
                    grid3.append([])

            #2D -> 3D
            grid4 = []
            temp=[]
            for i in range(len(grid3)):
                temp.append(grid3[i])
                if i%9==8:
                    grid4.append(temp)
                    temp=[]

            #Checking cells with unique notes
            items_to_keep = []
            for i in range(len(grid4)):
                for j in range(len(grid4)):
                    if len(grid4[i][j])==1:
                        row = get_row(grid4,i)
                        col = get_col(grid4,j)
                        box = get_box(grid4,i,j)
                        keepItem = True
                        for a in range(len(row)):
                            if grid4[i][j][0] in row[a][0] and [i,j]!=[row[a][1],row[a][2]]:
                                keepItem=False
                            if grid4[i][j][0] in col[a][0] and [i,j]!=[col[a][1],col[a][2]]:
                                keepItem=False
                            if grid4[i][j][0] in box[a][0] and [i,j]!=[box[a][1],box[a][2]]:
                                keepItem=False
                        if keepItem==True:
                            items_to_keep.append([i,j])

            #Testing these cells - either mark text as red or create label
            for i,j in items_to_keep:
                if grid2[i][j][0] != int(self.game_solution.ans[9*i+j]):
                    self.entries[9*i+j]['fg']='#ff0000'
                    self.errors+=1
                    self.errors_made_label["text"] = f'Errors: {self.errors}'
                    grid2[i][j]=[1,2,3,4,5,6,7,8,9]
                else:
                    self.entries[9*i+j].delete("1.0","end")
                    self.entries[9*i+j].config(state=tk.DISABLED)
                    self.entries[9*i+j] = tk.Label(text=f"{str(grid2[i][j][0])}",master=self.entries[9*i+j].master,width=3,font=f_label)
                    self.entries[9*i+j]["bg"]='#ffffff'
                    self.entries[9*i+j].grid(row=i%3,column=j%3)

            #Editing available numbers (bottom of window)
            g = [0,0,0,0,0,0,0,0,0]
            for i in range(len(self.entries)):
                if type(self.entries[i])==tk.Label:
                    e = int(self.entries[i]["text"])-1
                    g[e] = g[e]+1
            for i in range(len(self.usedNumLabels)):
                if g[i]==9:
                    self.usedNumLabels[i]["text"]=' '

            #Hint feature
            if hint==True:

                #Adding answer to grid (if not in already)
                for i in range(len(grid2)):
                    for j in range(len(grid2[i])):
                        if int(self.game_solution.ans[9*i+j]) not in grid2[i][j]:
                            grid2[i][j].append(int(self.game_solution.ans[9*i+j]))
                            grid2[i][j].sort()

                #Getting move
                hint_type, hint_pos, hint_old, hint_new = constraint(grid2).next_move

                #Set hint label to tell which move was just executed
                self.hintLabel['text']=move_dict[hint_type]

                # Hint format:
                # Type, indices, old, new

                # Working through the moves
                for ind, z in enumerate(hint_pos):
                    i, j = z

                    if type(self.entries[i*9+j]) == tk.Label:
                        continue

                    self.entries[i*9+j]['fg'] = '#ff00ff'

                    #Add move set
                    ystr=''
                    for digit in hint_new[ind]:
                        ystr+=(str(digit))


                    self.entries[i*9+j].delete('1.0',tk.END)
                    self.entries[i*9+j].insert('1.0',ystr)
                
                #Change hints label
                self.hints+=1
                self.hints_used_label["text"] = f"Hints used: {self.hints}"                     

    def f_solve_game(self):
        #Style
        f_label = font.Font(family="TkDefaultFont",size=17,weight="normal")
        
        #Going through grid
        for i, item in enumerate(self.entries):
            
            #Setting all cells as labels (uneditable)
            if type(self.entries[i])==tk.Text:
                self.entries[i].delete("1.0","end")
                self.entries[i].config(state=tk.DISABLED)
            y1 = i//9
            x1 = i%9
            item = tk.Label(text=f"{self.game_solution.ans[i]}",master=item.master,width=3,bg='#ffffff',font=f_label)
            item.grid(row=y1%3,column=x1%3)

        #Removing text from used number labels
        for i in range(9):
            self.usedNumLabels[i]["text"]=' '

        #Disabling buttons
        self.checkB['fg']='#ff0000'
        self.hintB['fg']='#ff0000'
        self.solveB['fg']='#ff0000'
        self.checkB.configure(command=self.f_do_nothing)
        self.hintB.configure(command=self.f_do_nothing)
        self.solveB.configure(command=self.f_do_nothing)

    def f_submit_score(self):
        #Getting name
        name = self.score_entry.get()

        #Checking name is valid
        if len(name)<=16 and len(name)>=0:
            
            #checking the input doesn't only consist of spaces
            non_space = False 
            for i in name:
                if i!=' ':
                    non_space=True 
            if non_space:

                #Setting user information and adding to database
                time = round(self.final_time,2)
                grid = self.final_grid
                curDate = date.today()
                add_result(name,grid,curDate,time)
                self.win_window.destroy()

            else:
                #Disallowing input
                self.submit_button["fg"]='#FF0000'      
        else:
            
            #Disallowing input
            self.submit_button["fg"]='#FF0000'      

    def f_return_query(self):
        #Setting style
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
        title_relief = tk.RAISED
        name_w = 16
        grid_w = 20
        date_w = 12
        time_w = 10
        play_w = 5

        #Deleting current widgets
        for child in self.query_frame.winfo_children():
            child.destroy()

        #Setting title labels and frame
        self.query_frame = tk.Frame(height=30)
        results_queries = []
        nameLbl = tk.Label(text='Name',master=self.query_frame,width=name_w,font=f_main,relief=title_relief)
        gridLbl = tk.Label(text='Grid',master=self.query_frame,width=grid_w,font=f_main,relief=title_relief)
        dateLbl = tk.Label(text='Date',master=self.query_frame,width=date_w,font=f_main,relief=title_relief)
        timeLbl = tk.Label(text='Time',master=self.query_frame,width=time_w,font=f_main,relief=title_relief)
        emptyLbl = tk.Button(text=' ',master=self.query_frame,font=f_main,width=play_w)

        #Querying name, grid input
        name = self.searchNameE.get()
        grid = self.searchGridE.get()
        results = search_result(name,grid)
        
        #GUI
        nameLbl.grid(row=0,column=0)
        gridLbl.grid(row=0,column=1)
        dateLbl.grid(row=0,column=2)
        timeLbl.grid(row=0,column=3)
        emptyLbl.grid(row=0,column=4)
        
        #Adding all results of query to window
        try:
            results_queries.append([tk.Label(text=results[0][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[0][1],master=self.query_frame,anchor="w",width=grid_w,font=f_main),tk.Label(text=results[0][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f"{int(results[0][3]//60)}m {int(round(results[0][3]%60))}s",master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[0][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[1][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[1][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[1][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[1][3]//60)}m {int(round(results[1][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[1][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[2][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[2][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[2][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[2][3]//60)}m {int(round(results[2][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[2][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[3][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[3][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[3][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[3][3]//60)}m {int(round(results[3][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[3][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[4][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[4][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[4][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[4][3]//60)}m {int(round(results[4][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[4][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[5][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[5][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[5][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[5][3]//60)}m {int(round(results[5][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[5][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[6][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[6][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[6][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[6][3]//60)}m {int(round(results[6][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[6][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[7][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[7][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[7][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[7][3]//60)}m {int(round(results[7][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[7][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[8][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[8][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[8][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[8][3]//60)}m {int(round(results[8][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[8][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[9][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[9][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[9][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[9][3]//60)}m {int(round(results[9][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[9][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[10][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[10][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[10][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[10][3]//60)}m {int(round(results[10][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[10][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[11][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[11][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[11][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[11][3]//60)}m {int(round(results[11][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[11][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[12][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[12][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[12][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[12][3]//60)}m {int(round(results[12][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[12][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[13][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[13][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[13][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[13][3]//60)}m {int(round(results[13][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[13][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
            results_queries.append([tk.Label(text=results[14][0],master=self.query_frame,width=name_w,font=f_main),tk.Label(text=results[14][1],master=self.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[14][2],master=self.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[14][3]//60)}m {int(round(results[14][3]%60))}s',master=self.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:self.s_game(results[14][1]),master=self.query_frame,width=play_w,font=f_main,relief=title_relief)])
        except:
            pass
        
        #Adding empty labels (to ensure height is constant for all queries)
        for i in range(len(results_queries),15):
            results_queries.append([tk.Label(text=' ',master=self.query_frame,width=name_w,font=f_main),tk.Label(text=' ',master=self.query_frame,anchor="w",width=grid_w,font=f_main),tk.Label(text=' ',master=self.query_frame,width=date_w,font=f_main),tk.Label(text=' ',master=self.query_frame,width=time_w,font=f_main),tk.Button(text=' ',master=self.query_frame,width=play_w,font=f_main,relief=tk.FLAT)])

        #Placing
        for i, result in enumerate(results_queries):
            for j in range(len(result)):
                result[j].grid(row=i+1,column=j)

        #Placing in window
        self.query_frame.grid(row=2,column=0)

    def f_check_clipboard(self):
        clip = clipboard.paste()
        
        #Checking input has 1 solution -> play game or return error
        try:

            #if clipboard is tring
            if len(clip)>0:

                #if clipboard is URL
                if 'http' in clip:
                    img = Image.open(BytesIO(requests.get(clip).content))
                    self.s_upload_stage_2(img,'C')
            
                else:

                    #if clipboard is grid string
                    stri = clip
                    k = algorithm_x(stri)
                    if k.sols==1:
                        self.s_game(stri)
                    elif k.sols==2:
                        y = random.randint(0,len(gen_difficulty)-1)
                        print(f'Difficulty level: {y+1}')
                        self.s_game(generate(gen_difficulty[y],stri).ans)

                    else:
                        self.clipboardB["fg"] = '#FF0000'
            else:
                #if clipboard is image
                self.s_upload_stage_2(clip,'C')
        except:
            self.clipboardB["fg"] = '#FF0000'

    def f_clear_grid(self):
        for i in range(len(self.entries)):
            if type(self.entries[i])==tk.Text:
                self.entries[i].delete("1.0","end")

    def f_validate_grid(self):
        #Iterating through cells
        for q,entry in enumerate(self.entries):

            #Getting entry text            
            if type(entry)==tk.Text:
                text = entry.get("1.0",tk.END)
                
                #Forcing text to be only digits
                text = list(text)
                for i in range(len(text)-1,-1,-1):
                    if text[i] not in {'1','2','3','4','5','6','7','8','9'}:
                        text.pop(i)
                    else:
                        text[i] = int(text[i])

                #Sorting and ensuring each num only appears once
                text.sort()
                for i in range(len(text)-1,0,-1):
                    if text[i]==text[i-1]:
                        text.pop(i)
                    else:
                        text[i] = str(text[i])
                if len(text)>0:
                    text[0]=str(text[0])
                text = ''.join(text)

                #Placing in grid if input has changed
                textOld = entry.get("1.0","end-1c")
                if textOld!=text:
                    self.entries[q].delete("1.0","end")
                    self.entries[q].insert("1.0",text)
                    self.entries[q]['fg']='#0000ff'
                else:
                    self.entries[q]['fg']='#000000'

    def f_do_nothing(self):
        #This function does nothing.
        pass


    def f_train_digits(self):
        #Disable start, back
        self.startB["fg"] = '#FF0000'
        self.backB["fg"] = '#FF0000'
        self.epochsLabel["fg"] = '#FF0000'
        
        self.startB["command"] = self.f_do_nothing
        self.backB["command"] = self.f_do_nothing

        t = threading.Thread(target=self.train_digit_model)
        t.start()


    def f_train_grid(self):
        #Disable start, back
        self.startB["fg"] = '#FF0000'
        self.backB["fg"] = '#FF0000'
        self.epochsLabel["fg"] = '#FF0000'
        
        self.startB["command"] = self.f_do_nothing
        self.backB["command"] = self.f_do_nothing

        t = threading.Thread(target=self.train_grid_model)
        t.start()

        
    def train_digit_model(self):
        try:
            epoch_rate = int(self.epochsEntry.get())
            train_obj = train(self.win)
            train_obj.train_digits(epoch_rate)
            self.startB["fg"] = '#000000'
        except:
            pass
        
        #Re-enable start, back
        self.backB["fg"] = '#000000'
        self.epochsLabel["fg"] = '#000000'
        
        self.startB["command"] = self.f_train_digits
        self.backB["command"] = self.screen_home


    def train_grid_model(self):
        try:
            epoch_rate = int(self.epochsEntry.get())
            train_obj = train(self.win)
            train_obj.train_grid(epoch_rate)
            self.startB["fg"] = '#000000'
        except:
            pass
        
        #Re-enable start, back
        self.backB["fg"] = '#000000'
        self.epochsLabel["fg"] = '#000000'
        
        self.startB["command"] = self.f_train_grid
        self.backB["command"] = self.screen_home


    def screen_multiplayer(self):
        pass

    def screen_leaderboard(self):
        pass



y = front_end()

