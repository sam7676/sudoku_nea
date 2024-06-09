from solver import *

from time import perf_counter
from PIL import Image
from PIL import ImageTk
import random
import pyautogui as pg                          # This for some reason modifies the font
import tkinter as tk
from tkinter.filedialog import askopenfilename
from datetime import date
from tkinter import font
from collections import defaultdict

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





gen_difficulty = [[0,1],[30,1],[100,2],[250,3]]
move_dict = {
    "One note":'Hint: One note only',
    "Partner":'Hint: Partner',
    "Bowman":'Hint: Bowman Bingo',
    "Remove":'Hint: Remove note',
}





def convert(): pass
def clear_table(): pass
def search_result(): pass   
def add_result(): pass
def train(): pass


use_square_boxes = False


# Attempt to connect to server. If not, offline mode
# Attempt to login and skip
# Menu screen with Play offline, Login, Register


# Custom function, applying a default style to Tkinter widgets
def grid(widget, row=0, col=0, 
                font_type=None, width=29, height=2, 
                relief=tk.RAISED, foreground='#5B0000', padx=0, pady=0, ipadx=0, ipady=0):
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
    widget.grid(row=row, column=col, 
                padx=padx, pady=pady,
                ipadx=ipadx, ipady=ipady)
    



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
        self.socket.emit('attempt_register', {"username":username, "password":password})
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

            multiplayer_button = tk.Button(text="Multiplayer", command=lambda : None)

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
        generate_button = tk.Button(text="Generate grid", command=self.screen_generate)
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

    # Builds a grid out of tkinter widgets for entering information. Create custom and upload.
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

    # Checks the validity of the grid we are trying to create
    def check_valid_grid_creation(self):

        # Overriding grid function using this function scope. Doesn't break anything but be aware.

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
                self.screen_game(grid_string)
            
            #If more than 1 solution, use generator and proceed to game
            elif result.sols==2:


                difficulty = random.randint(0,len(gen_difficulty)-1)

                self.screen_game(generate(gen_difficulty[difficulty],
                                     grid_string).ans)
                
            else:

                #Error - display using confirm button
                self.confirmB["fg"] = '#FF0000'
            



    # Used to process images of Sudoku grids into the application to play
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
    
    # Verify cropping of YOLO
    def screen_check_grid_model(self, image):

        self.reset_window()

        # Sizing down image (width and height max 1080)
        image_width = image.width
        image_height = image.height

        max_size = 800

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

    # Verify CNN results
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



    # Builds a grid out of tkinter widgets for the game application
    def build_game_grid(self, grid_frame):
        subgrid_frames = [tk.Frame(master=grid_frame) for i in range(9)]

        self.entries = []

        for y in range(9):
            for x in range(9):
                box_value = 3 * (y//3) + (x//3)
                self.entries.append(tk.Text(master=subgrid_frames[box_value]))
                
        for i, item in enumerate(self.entries):
            y = i//9
            x = i%9

            '''
            note: a major limitation of Tkinter is that it doesn't support letter spacing
            Either we can fit a 3x3 string in the box but it is rectangular, or a larger string but the box is square
            This is controlled by the variable use_square_boxes
            '''

            if use_square_boxes:
                grid(item, row=y%3, col=x%3, width=6, height=3)
            else:
                grid(item, row=y%3, col=x%3, width=3, height=3, ipadx=5)
            

        for i, subgrid in enumerate(subgrid_frames):
            subgrid.grid(row=i//3,
                         column=i%3,
                         padx=5,
                         pady=5)

    # Game screen
    def screen_game(self,grid_string):

        self.game_solution = constraint(grid_string)
        self.grid_input = grid_string
        self.hints =0
        self.errors = 0

        self.selected_cell = None


        self.reset_window()

        left_frame = tk.Frame()

        grid(left_frame, row=0, col=0)


        game_frame = tk.Frame(master=left_frame)
        self.build_game_grid(game_frame)

                
        #Placing uneditable labels where possible
        for i, item in enumerate(self.entries):
            if grid_string[i]!='0':
                y1 = i//9
                x1 = i%9
                self.entries[i].config(state=tk.DISABLED)
                self.entries[i] = tk.Label(text=f"{grid_string[i]}",
                                           master=item.master, bg='#ffffff')
                grid(self.entries[i], row=y1%3, col=x1%3, width=3, relief=tk.FLAT)

        grid(game_frame, row=0, col=0)

        note_frame = tk.Frame(master=left_frame)

        grid(note_frame, row=1, col=0)

        self.note_labels = []
        for i in range(9):
            note_button = tk.Button(
                text=f"{i+1}", 
                master=note_frame,
                command=lambda : None)

            self.note_labels.append(note_button)

            grid(note_button, col=i, row=0, width=4)
        

        right_frame = tk.Frame()

        grid(right_frame, row=0, col=1)

        self.check_button = tk.Button(text="Check", command=lambda: self.check_grid(show_hint=False), master=right_frame)
        grid(self.check_button, row=0, width=20)

        self.hint_button = tk.Button(text="Hint", command=lambda: self.check_grid(show_hint=True), master=right_frame)
        grid(self.hint_button, row=1, width=20)
        
        self.hints_used_label = tk.Label(text=f"Hints used: {self.hints}",master=right_frame)
        grid(self.hints_used_label, row=2, width=20)
       
        self.errors_made_label = tk.Label(text=f"Errors made: {self.errors}",master=right_frame)
        grid(self.errors_made_label, row=3, width=20)

        self.clear_grid_button = tk.Button(text="Clear grid", command=self.clear_notes, master=right_frame)
        grid(self.clear_grid_button, row=4, width=20)

        self.solve_button = tk.Button(text="Solve", command=self.solve_game, master=right_frame)
        grid(self.solve_button, row=5, width=20)

        back_button = tk.Button(text="Back", command=self.screen_play_options, master=right_frame)
        grid(back_button, row=6, width=20)

        #Timer and window set-up
        self.timer_start = perf_counter()
        self.win.mainloop()

    # Checks uniqueness of a number in a row, column or box - used to verify entries from the user
    def count_occurences(self, grid, y, x, value):

        row_counter = defaultdict(int)
        col_counter = defaultdict(int)
        box_counter = defaultdict(int)

        for cell in (grid[y][i] for i in range(9)):
            for number in cell:
                row_counter[number] += 1
        
        for cell in (grid[i][x] for i in range(9)):
            for number in cell:
                col_counter[number] += 1
        
        y1 = y%3
        x1 = x%3

        for cell in (grid[y-y1+i][x-x1+j] for j in range(3) for i in range(3)):
            for number in cell:
                box_counter[number] += 1
        
        return row_counter[value] == col_counter[value] == box_counter[value] == 1

    # Checks whether the grid is valid and complete and places a hint if necessary
    def check_grid(self,show_hint):

        #BUG: faulty notes lead to hint system not converging to answer
        # idea is to check solutions in solver.py and whether it corresponds with original answer given hints available

        flattened_grid=[]
        
        self.validate_grid()
        
        # Working through grid on screen and getting value in each cell
        for i, cell_entry in enumerate(self.entries):
            if type(cell_entry)==tk.Text:

                cell_text = cell_entry.get("1.0","end-1c")

                if cell_text == '': cell_list = []
                else:
                    cell_list = list(map(int, cell_text))

                flattened_grid.append(cell_list)

            elif type(cell_entry)==tk.Label:

                flattened_grid.append([int(cell_entry["text"])])

        grid = []
        row = []

        # Transforming grid to 3D
        for i, cell in enumerate(flattened_grid):
            row.append(cell)
            if i%9 == 8:
                grid.append(row)
                row = []

        correct = [0 for _ in range(9)]

        # Finding and checking unique notes
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):

                # checking for isolated cells
                if len(cell) != 1: continue

                # getting labels
                if type(self.entries[9*i+j]) == tk.Label:
                    correct[cell[0]-1] += 1
                    continue
                
                # checking note is unique
                if not self.count_occurences(grid, i, j, cell[0]): continue

                # compare to answer
                if cell[0] == int(self.game_solution.ans[9*i+j]):

                    correct[cell[0]-1] += 1

                    self.convert_cell_to_answer(9*i+j)

                else:

                    # incorrect, mark this as an error
                    self.entries[9*i+j]['fg']='#ff0000'
                    self.errors+=1
                    self.errors_made_label["text"] = f'Errors: {self.errors}'
                    grid[i][j]=[1,2,3,4,5,6,7,8,9]

        
        # Editing available numbers at bottom and checking for completeness
        game_complete = True
        for i in range(9):
            if correct[i] != 9:
                game_complete = False
                
            else:

                self.note_labels[i]["text"]=' '

        if game_complete:

            # Disabling buttons
            self.check_button['fg']='#00ff00'
            self.hint_button['fg']='#00ff00'
            self.solve_button['fg']='#00ff00'
            self.clear_grid_button['fg']='#00ff00'

            self.check_button.configure(command=lambda : None)
            self.hint_button.configure(command=lambda : None)
            self.solve_button.configure(command=lambda : None)
            self.clear_grid_button.configure(command=lambda : None)
            
            #Finishing game
            self.timer_end = perf_counter()
            self.screen_win()

        elif show_hint:
                
            # Inserting answer if not present
            for i, row in enumerate(grid):
                for j, cell in enumerate(row):

                    if cell == []:
                        grid[i][j] = [1,2,3,4,5,6,7,8,9]
                        continue

                    cell_answer = int(self.game_solution.ans[9*i+j])

                    if cell_answer not in cell:
                        grid[i][j].append(cell_answer)
                        grid[i][j].sort()
                
            #Getting hint
            hint_type, hint_positions, hint_old, hint_new = constraint(grid).next_move

            #Set hint label to tell which move was just executed
            self.hint_button['text'] = move_dict[hint_type]

            # Working through the moves
            for ind, position in enumerate(hint_positions):
                i, j = position

                # Ignore labels
                if type(self.entries[i*9+j]) == tk.Label: continue

                # Update entry colour
                self.entries[i*9+j]['fg'] = '#ff00ff'

                move = ''.join(str(digit) for digit in hint_new[ind])

                self.entries[i*9+j].delete('1.0',tk.END)
                self.entries[i*9+j].insert('1.0',move)
            
            #Change hints label
            self.hints += 1
            self.hints_used_label["text"] = f"Hints used: {self.hints}"                     


    def validate_grid(self):

        for ind, entry in enumerate(self.entries):
            
            if type(entry)==tk.Text:
                text = entry.get("1.0",tk.END)

                digit_arr = [False for i in range(9)]

                for char in text:

                    # Forcing text to be digits between 1 and 9
                    if char in {'1','2','3','4','5','6','7','8','9'}:
                        digit_arr[int(char)-1] = True

                new_text = ''.join(str(i+1) for i in range(9) if digit_arr[i])

                
                if text != new_text:
                    self.entries[ind].delete("1.0","end")
                    self.entries[ind].insert("1.0", new_text)
                    self.entries[ind]['fg']='#0000ff'
                else:
                    self.entries[ind]['fg']='#000000'

    def solve_game(self):

        # Turns all entries into labels
        for i in range(81):
            self.convert_cell_to_answer(i)
        
        # Disables buttons
        self.disable_game_buttons()

        # Updates remaining numbers
        for i in range(9):
            self.note_labels[i]["text"]=' '

    def disable_game_buttons(self):
        self.check_button['fg']='#ff0000'
        self.hint_button['fg']='#ff0000'
        self.solve_button['fg']='#ff0000'
        self.clear_grid_button['fg']='#ff0000'

        self.check_button.configure(command=lambda : None)
        self.hint_button.configure(command=lambda : None)
        self.solve_button.configure(command=lambda : None)
        self.clear_grid_button.configure(command=lambda : None)

    def convert_cell_to_answer(self, i):

        if type(self.entries[i]) == tk.Label: return

        # converting cell to label
        self.entries[i].delete("1.0","end")
        self.entries[i].config(state=tk.DISABLED)
        self.entries[i] = tk.Label(text=f"{self.game_solution.ans[i]}",
                            master=self.entries[i].master,
                            bg='#ffffff')
        
        y = i//9
        x = i%9

        grid(self.entries[i], row=y%3, col=x%3, width=3, relief=tk.FLAT)

    def clear_notes(self):
        for entry in self.entries:
            if type(entry) == tk.Text:
                entry.delete('1.0',tk.END)










    def time_to_string(self, seconds):

        mins = int(seconds // 60)

        seconds = seconds % 60

        milliseconds = seconds % 1

        seconds = int(seconds // 1)

        return f'{mins}:{seconds}.{int(milliseconds*100)}'

    def screen_win(self):

        self.final_time = self.timer_end - self.timer_start

        self.new_window = tk.Tk()

        congrats_label = tk.Label(text=f"Congratulations! You won in {self.time_to_string(self.final_time)}",
                                  master=self.new_window)

        congrats_label.grid(row=0)

        error_total = tk.Label(master=self.new_window,text=f'Errors: {self.errors}')
        hint_total = tk.Label(master=self.new_window,text=f'Hints: {self.hints}')

        error_total.grid(row=1)
        hint_total.grid(row=2)

        quit_button = tk.Button(text="Quit", 
                                command=self.new_window.destroy,
                                master=self.new_window)
        
        quit_button.grid(row=3)

        if self.online_mode:
            
            quit_button.configure(command=self.submit_score)

        self.new_window.mainloop()
        
    def submit_score(self):

        playerID = self.playerID
        grid_time = self.final_time
        grid_string = self.grid_input
        errors = self.errors
        hints = self.hints

        self.socket.emit('submit_score', {"playerID":playerID, 
                                          "grid_time":grid_time, 
                                          "grid_string":grid_string, 
                                          "errors":errors, 
                                          "hints":hints})

        self.new_window.destroy()



    def screen_generate(self):

        self.reset_window()

        difficulty_array = []
        for i in range(4):
            difficulty_button = tk.Button(text=f'Level {i+1}',command=lambda:self.screen_game(generate(gen_difficulty[i]).ans))
            grid(difficulty_button, row=i, col=0)
            difficulty_array.append(difficulty_button)
        


        back_button = tk.Button(text='Back',command=self.screen_play_options)

        grid(back_button, row=len(difficulty_array))
        
        self.win.mainloop()





    def process_query(self):

        #Deleting current widgets
        for child in self.query_frame.winfo_children():
            child.destroy()

        name = self.search_name_entry.get()
        grid_string = self.search_grid_entry.get()

        name_label = tk.Label(text='Name',master=self.query_frame)
        grid_label = tk.Label(text='Grid',master=self.query_frame)
        date_label = tk.Label(text='Date',master=self.query_frame)
        time_label = tk.Label(text='Time',master=self.query_frame)
        hint_label = tk.Label(text='Hints',master=self.query_frame)
        error_label = tk.Label(text='Errors',master=self.query_frame)
        empty_label = tk.Label(text='',master=self.query_frame)

        name_width = 10
        grid_width = 10
        date_width = 16
        time_width = 10
        hint_width = 4
        error_width = 6

        grid(name_label, row=0, col=0, width=name_width)
        grid(grid_label, row=0, col=1, width=grid_width)
        grid(date_label, row=0, col=2, width=date_width)
        grid(time_label, row=0, col=3, width=time_width)
        grid(hint_label, row=0, col=4, width=hint_width)
        grid(error_label, row=0, col=5, width=error_width)

        
        self.socket.emit('get_leaderboard_data', {"name": name, "grid":grid_string})
        result = self.socket.receive()[1]

        result = result["result"]

        for i, res in enumerate(result):

            name, grid_str, time, date, hints, errors = res

            time = round(float(time), 2)

            name_label = tk.Label(text=name,master=self.query_frame)
            grid_label = tk.Label(text=grid_str,master=self.query_frame)
            date_label = tk.Label(text=date,master=self.query_frame)
            time_label = tk.Label(text=time,master=self.query_frame)
            hint_label = tk.Label(text=hints,master=self.query_frame)
            error_label = tk.Label(text=errors,master=self.query_frame)

            grid(name_label, row=i+1, col=0, width=name_width)
            grid(grid_label, row=i+1, col=1, width=grid_width)
            grid(date_label, row=i+1, col=2, width=date_width)
            grid(time_label, row=i+1, col=3, width=time_width)
            grid(hint_label, row=i+1, col=4, width=hint_width)
            grid(error_label, row=i+1, col=5, width=error_width)
        


    
    def screen_leaderboard(self):
        
        self.reset_window()

        options_frame = tk.Frame()
        grid(options_frame, row=0)


        search_name_label = tk.Label(text='Search name', master=options_frame)
        self.search_name_entry = tk.Entry(master=options_frame)
        search_grid_label = tk.Label(text='Search grid', master=options_frame)
        self.search_grid_entry = tk.Entry(master=options_frame)

        search_button = tk.Button(text='Search',command=self.process_query, master=options_frame)
        back_button = tk.Button(text='Back',command=self.screen_home, master=options_frame)

        grid(search_name_label, row=0, col=0, width=15)
        grid(self.search_name_entry, row=0, col=1, width=15)
        grid(search_grid_label, row=0, col=2, width=15)
        grid(self.search_grid_entry, row=0, col=3, width=15)
        grid(search_button, row=0, col=4, width=8)
        grid(back_button, row=0, col=5, width=8)


        self.query_frame = tk.Frame(height=30)

        grid(self.query_frame, row=2)

        self.win.mainloop()














y = front_end()

