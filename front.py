from converter import *
from solver import *
from training import *
from imports import *
from database import *

class front_end:
    def __init__(x): #init
        x.win=tk.Tk()
        x.s_home()
    def s_home(x): #home page
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)

        #Style
        w,h,rel=29,2,tk.RAISED
        f_title = font.Font(family="TkDefaultFont",size=12,weight="normal")
        f_name = font.Font(family="TkDefaultFont",size=11,weight="normal")

        #Shared attribute
        x.diffs=[[20,1],[50,1],[150,1],[500,1],[500,3],[500,10]]

        #Logo
        logo = ImageTk.PhotoImage(Image.open(img_logo))
        logoL = tk.Label(image=logo)
        
        #Name and frame
        nameL = tk.Label(text='Sam Stimpson',
            width=w,height=1,font=f_name,fg='#5B0000')
        frame1 = tk.Frame()

        #Buttons
        playB = tk.Button(text='Play',command=x.s_play_options,
            master=frame1,width=w,height=h,font=f_title,relief=rel)
        leaderboardB = tk.Button(text='Leaderboard',command=x.s_leaderboard,
            master=frame1,width=w,height=h,font=f_title,relief=rel)
        debugB = tk.Button(text='Debug',command=x.s_debug,
            master=frame1,width=w,height=h,font=f_title,relief=rel)
        exitB = tk.Button(text='Exit',command=x.win.destroy,
            master=frame1,width=w,height=h,font=f_title,relief=rel)

        #Placing in GUI
        logoL.grid(row=0)
        nameL.grid(row=1)
        frame1.grid(row=2)

        playB.grid(row=0)
        leaderboardB.grid(row=1)
        debugB.grid(row=2)
        exitB.grid(row=3)
        x.win.mainloop()
    def s_play_options(x): #play options page
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        w=42
        play_relief = tk.RAISED
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")

        #Options header

        optns_image = ImageTk.PhotoImage(Image.open(img_optns))
        options_label = tk.Label(image=optns_image)
        options_label.grid(row=0)
        
        #Buttons
        customB = tk.Button(text='Create custom',command=x.s_create_custom_game,
            font=f_main,width=w,height=2,relief=play_relief)
        generateB = tk.Button(text='Generate',command=x.s_generate,
            font=f_main,width=w,height=2,relief=play_relief)
        uploadB = tk.Button(text='Upload',command=x.s_upload_stage_1,
            font=f_main,width=w,height=2,relief=play_relief)
        backB = tk.Button(text='Back',command=x.s_home,
            font=f_main,width=w,height=2,relief=play_relief)
        
        #GUI
        customB.grid(row=1)
        generateB.grid(row=2)
        uploadB.grid(row=3)
        backB.grid(row=4)

        x.win.mainloop()
    def s_create_custom_game(x):
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
        label_w = 14

        custom_image = ImageTk.PhotoImage(Image.open(img_custom))
        custom_label = tk.Label(image=custom_image)
        custom_label.grid(row=0)

        #Frame setup
        frame1 = tk.Frame()
        frame2 = tk.Frame()
        
        #Grid setup and placing
        sg=[tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1)]
        x.entries = [tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3)]
   
        for i,item in enumerate(x.entries):
            y1 = i//9
            x1 = i%9
            item.grid(row=y1%3,column=x1%3)   
        for i, sub in enumerate(sg):
            sub.grid(row=i//3,column=i%3,padx=5,pady=5)

        #Buttons
        backB = tk.Button(master=frame2,text='Back',command=x.s_play_options,
            width=label_w,font=f_main)
        x.confirmB = tk.Button(master=frame2,text='Confirm',command=x.f_check_valid_grid_creation,
            width=label_w,font=f_main)
        backB.grid(row=0,column=0)
        x.confirmB.grid(row=0,column=1)

        #GUI final
        frame1.grid(row=1,column=0)
        frame2.grid(row=2,column=0)
        x.win.mainloop()
    def s_upload_stage_1(x):
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        play_relief = tk.RAISED
        button_w = 36
        h=2
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")


        upload_i = ImageTk.PhotoImage(Image.open(img_upload))
        upload_L = tk.Label(image=upload_i)

        #Get image either from clipboard or open file
        x.clipStriB = tk.Button(text='Clipboard string',command=x.f_check_grid_string,
            width=button_w,relief=play_relief,font=f_main,height=2)
        x.clipboardB = tk.Button(text='Clipboard image',command=lambda:x.s_upload_stage_2(clipboard.paste(),'C'),
            width=button_w,relief=play_relief,font=f_main,height=2)
        x.openFileB = tk.Button(text='Open file',command=x.f_upload_open_file,
            width=button_w,relief=play_relief,font=f_main,height=2)
        backB = tk.Button(text='Back',command=x.s_play_options,
            width=button_w,relief=play_relief,font=f_main,height=2)
        
        upload_L.grid(row=0)
        x.clipStriB.grid(row=1)
        x.clipboardB.grid(row=2)
        x.openFileB.grid(row=3)
        backB.grid(row=4)
        x.win.mainloop()
    def s_upload_stage_2(x,image,button_type):
        try:

            #Converting image
            image_conversion = convert(image)
        
            #GUI stuff
            x.win.destroy()
            x.win = tk.Tk()
            x.win.title('')
            o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
            x.win.iconphoto(False, o1x1_logo)
            frame0 = tk.Frame()
            frame1 = tk.Frame(master=frame0)
            frame2 = tk.Frame()

            f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
            label_w = 27

            #First frame - editable grid and photo
            img_grid = ImageTk.PhotoImage(image_conversion.img.resize((280,280)))
            ImgLabel = tk.Label(master=frame0,image=img_grid)

            #Setting up and displaying grid
            sg=[tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1)]
            x.entries = [tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[0],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[1],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[2],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[3],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[4],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[5],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[6],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[7],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3),tk.Entry(master=sg[8],width=3)]
            for i,item in enumerate(x.entries):
                y1 = i//9
                x1 = i%9
                item.grid(row=y1%3,column=x1%3)           
            for i,item in enumerate(x.entries):
                digit = image_conversion.ans[i]
                if digit!='0':
                    item.insert(0,image_conversion.ans[i])
            for i, sub in enumerate(sg):
                sub.grid(row=i//3,column=i%3,padx=5,pady=5)

            #Buttons
            backB = tk.Button(master=frame2,text='Back',command=x.s_play_options,
                font = f_main,width=label_w)
            x.confirmB = tk.Button(master=frame2,text='Confirm',command=lambda:x.f_check_valid_grid_creation(image_conversion),
                font = f_main,width=label_w)
            backB.grid(row=0,column=0)
            x.confirmB.grid(row=0,column=1)

            #GUI placements
            frame1.grid(row=0,column=0)
            ImgLabel.grid(row=0,column=1)
            frame0.grid(row=0,column=0)
            frame2.grid(row=1,column=0)
            x.win.mainloop()
        except:
            if button_type=='C':
                x.clipboardB["fg"]='#FF0000'
            elif button_type=='O':
                x.openFileB["fg"]='#FF0000'
    def s_game(x,grid):
        
        #Setting up constraint solver for next move function
        x.game_solution = constraint(grid)
        x.grid_input = grid
        x.hints =0
        x.errors = 0

        game_relief = tk.RAISED


        #Creating window and frames
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        frame1 = tk.Frame()
        frame2 = tk.Frame()
        hint_frame = tk.Frame()
        misc_frame = tk.Frame()
        frame3 = tk.Frame()

        cell_width = 6
        cell_height = 3

        hint_label_w = 25
        button_w = 12
        used_num_w = 5

        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
        f_button = font.Font(family="TkDefaultFont",size=11,weight="normal")
        f_label = font.Font(family="TkDefaultFont",size=17,weight="normal")
        f_num = font.Font(family="TkDefaultFont",size=11,weight="normal")

        #Creating grid
        sg=[tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1),tk.Frame(master=frame1)]
        x.entries = [tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[0],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[1],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[2],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[3],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[4],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[5],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[6],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[7],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main),tk.Text(master=sg[8],width=cell_width,height=cell_height,font=f_main)]
        for i,item in enumerate(x.entries):
            y1 = i//9
            x1 = i%9
            item.grid(row=y1%3,column=x1%3)                
        for i, sub in enumerate(sg):
            sub.grid(row=i//3,column=i%3,padx=5,pady=5)
        
        #Placing uneditable labels where possible
        for i, item in enumerate(x.entries):
            if grid[i]!='0':
                y1 = i//9
                x1 = i%9
                x.entries[i].config(state=tk.DISABLED)
                x.entries[i] = tk.Label(text=f"{grid[i]}",master=item.master,width=3,bg='#ffffff',font=f_label)
                x.entries[i].grid(row=y1%3,column=x1%3)

        #Extra functions
        x.checkB = tk.Button(master=frame2,text='Check',command=lambda: x.f_get_hint(False),
            width=button_w,font=f_button)
        x.hintB = tk.Button(master=frame2,text='Hint',command=lambda: x.f_get_hint(True),
            width=button_w,font=f_button)
        x.solveB = tk.Button(master=frame2,text='Solve',command=x.f_solve_game,
            width=button_w,font=f_button)
        backB = tk.Button(master=frame2,text='Back',command=x.s_play_options,
            width=button_w,font=f_button)
        
        
        x.checkB.grid(row=0,column=0)
        x.hintB.grid(row=0,column=1)
        x.solveB.grid(row=0,column=2)
        backB.grid(row=0,column=3)

        
        x.hintLabel = tk.Label(text='Hint: None',master=hint_frame,
            width=hint_label_w,font=f_button,relief=game_relief)

        x.hints_used_label = tk.Label(text=f'Hints used: {x.hints}',master=hint_frame,
            width=hint_label_w,font=f_button,relief=game_relief)

        clear_grid_B = tk.Button(text='Clear grid',master=misc_frame,command=x.f_clear_grid,
            width=hint_label_w,font=f_button,relief=game_relief)

        x.errors_made_label = tk.Button(text=f'Errors: {x.errors}',master=misc_frame,
            width=hint_label_w,font=f_button,relief=game_relief)

        #Used numbers labels
        x.usedNumLabels = [tk.Button(master=frame3,height=2,text='1',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='2',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='3',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='4',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='5',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='6',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='7',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='8',relief=game_relief,width=used_num_w,font=f_num),tk.Button(master=frame3,height=2,text='9',relief=game_relief,width=used_num_w,font=f_num)]
        for i in range(len(x.usedNumLabels)):
            x.usedNumLabels[i].grid(row=0,column=i)

        #GUI stuff
        frame1.grid(row=0,column=0)
        frame2.grid(row=1,column=0)
        hint_frame.grid(row=2,column=0)
        x.hintLabel.grid(row=0,column=0)
        x.hints_used_label.grid(row=0,column=1)
        misc_frame.grid(row=3,column=0)
        clear_grid_B.grid(row=0,column=0)
        x.errors_made_label.grid(row=0,column=1)
        frame3.grid(row=4)



        #Timer and window set-up
        x.timer_start = perf_counter()
        x.win.mainloop()
    def s_leaderboard(x):
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")

        name_w = 16
        grid_w = 20


        leaderboard_image = ImageTk.PhotoImage(Image.open(img_lb))
        leaderboardL = tk.Label(image=leaderboard_image)

        frame1 = tk.Frame()

        miniFrame1 = tk.Frame(master=frame1)
        miniFrame2 = tk.Frame(master=frame1)

        searchNameB = tk.Label(master=miniFrame1,text='Search name',font=f_main,width=name_w)
        x.searchNameE = tk.Entry(master=miniFrame1,width=name_w)
        searchGridB = tk.Label(master=miniFrame1,text='Search grid',font=f_main,width=grid_w)
        x.searchGridE = tk.Entry(master=miniFrame1,width=grid_w)

        searchB = tk.Button(text='Search',command=x.f_return_query,master=miniFrame2,height=2,font=f_main,width=14)
        backB = tk.Button(text='Back',command=x.s_home,master=miniFrame2,height=2,font=f_main,width=14)

        

        leaderboardL.grid(row=0)
        frame1.grid(row=1)

        searchNameB.grid(row=0,column=0)
        x.searchNameE.grid(row=1,column=0)
        searchGridB.grid(row=0,column=1)
        x.searchGridE.grid(row=1,column=1)

        searchB.grid(row=0,column=0)
        backB.grid(row=0,column=1)

        

        miniFrame1.grid(row=0,column=0)
        miniFrame2.grid(row=0,column=1)
        x.query_frame = tk.Frame()

        x.win.mainloop()
    def s_generate(x):
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        f_main = font.Font(family="TkDefaultFont",size=11,weight="normal")
        w=41
        diff_w = 20

        
        generate_image = ImageTk.PhotoImage(Image.open(img_generate))
        generateL = tk.Label(image=generate_image)
        diff_frame = tk.Frame()        
        

        
        diff_array = [tk.Button(master=diff_frame,text='Level 1',width=diff_w,font=f_main,height=2,command=lambda:x.s_game(generate(x.diffs[0]).ans)),
                      tk.Button(master=diff_frame,text='Level 2',width=diff_w,font=f_main,height=2,command=lambda:x.s_game(generate(x.diffs[1]).ans)),  
                      tk.Button(master=diff_frame,text='Level 3',width=diff_w,font=f_main,height=2,command=lambda:x.s_game(generate(x.diffs[2]).ans)),  
                      tk.Button(master=diff_frame,text='Level 4',width=diff_w,font=f_main,height=2,command=lambda:x.s_game(generate(x.diffs[3]).ans)),
                      tk.Button(master=diff_frame,text='Level 5',width=diff_w,font=f_main,height=2,command=lambda:x.s_game(generate(x.diffs[4]).ans)),
                      tk.Button(master=diff_frame,text='Level 6',width=diff_w,font=f_main,height=2,command=lambda:x.s_game(generate(x.diffs[5]).ans)),  ]

        for i in range(len(diff_array)):
            diff_array[i].grid(row=i//2,column=i%2)

        backB = tk.Button(text='Back',font=f_main,width=w,command=x.s_play_options,height=2)

        generateL.grid(row=0)
        diff_frame.grid(row=1)
        
        backB.grid(row=3)
        x.win.mainloop()
    def s_win(x):
        x.final_time = perf_counter() - x.timer_start
        x.final_grid = x.grid_input
        x.win_window = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)

        width1=48
        #New win window
        win_img = ImageTk.PhotoImage(Image.open(img_win),master=x.win_window)
        win_label = tk.Label(master=x.win_window,image=win_img)

        final_mins = int(x.final_time//60)
        final_secs = int(round(x.final_time%60))

        time_label = tk.Label(master=x.win_window,text=f'Time taken: {final_mins}m {final_secs}s',
            font=("TkDefaultFont","10"),width=width1)
        name_label = tk.Label(master=x.win_window,text='Enter name [max 16 characters]:',
            font=("TkDefaultFont","10"),width=width1)
        x.score_entry = tk.Entry(master=x.win_window,
            font=("TkDefaultFont","10"),width=width1)
        x.submit_button = tk.Button(master=x.win_window,text='Submit',command=x.f_submit_score,
            font=("TkDefaultFont","10"),width=width1)
        quit_button = tk.Button(master=x.win_window,text='Quit',command=x.win_window.destroy,
            font=("TkDefaultFont","10"),width=width1)
        error_total = tk.Label(master=x.win_window,text=f'Errors: {x.errors}',
            font=("TkDefaultFont","10"),width=width1)
        hint_total = tk.Label(master=x.win_window,text=f'Hints: {x.hints}',
            font=("TkDefaultFont","10"),width=width1)

        win_label.grid(row=0)
        time_label.grid(row=1)
        error_total.grid(row=2)
        hint_total.grid(row=3)
        name_label.grid(row=4)
        x.score_entry.grid(row=5)
        x.submit_button.grid(row=6)
        quit_button.grid(row=7)

        x.win_window.mainloop()
    def s_debug(x):
        x.win.destroy()
        x.win = tk.Tk()
        x.win.title('')
        o1x1_logo = ImageTk.PhotoImage(Image.open(img_1x1))
        x.win.iconphoto(False, o1x1_logo)
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")

        debug_image = ImageTk.PhotoImage(Image.open(img_debug))
        debugL = tk.Label(image=debug_image)

        w=30
        train_digits_b = tk.Button(text='Train digits',font=f_main,command=train_digits,width=w)
        train_grid_b = tk.Button(text='Train grid',font=f_main,command=train_grid,width=w)
        clear_LB_b = tk.Button(text='Clear leaderboard',font=f_main,command=clear_table,width=w)
        backB = tk.Button(text='Back',command=x.s_home,font=f_main,width=w)

        debugL.grid(row=0,column=0)
        train_digits_b.grid(row=1)
        train_grid_b.grid(row=2)
        clear_LB_b.grid(row=3)
        backB.grid(row=4)

        x.win.mainloop()
    def f_check_valid_grid_creation(x,upload=None):
        try:
            #Getting grid from entries (dtype: array, 2D, string items)
            grid=[]
            for i in x.entries:
                grid.append([i.get().strip()])

            #Checking that length = 1 in all cases and only 123456789 appear
            errors=False
            for i in range(len(grid)):
                if len(grid[i])>1 or grid[i][0] not in '123456789':
                    x.entries[i]['fg'] = '#ff0000' #change colour of errors to red
                    errors=True
                else:
                    x.entries[i]['fg'] = '#000000' #change colour of valid to black

                    #Setting empty to zero and adding to grid string
                    if grid[i][0]=='':
                        grid[i]='0'
                    else:
                        grid[i]=grid[i][0]
            #if there are any errors, exit. otherwise:
            if errors==False:
                
                #Finalising grid, checking only 1 solution, executing
                grid2 = ''.join(grid)
                k = algorithm_x(grid2,solving='')
                print(f"Solutions: {k.sols}")
                if k.sols == 1:
                    
                    #If upload is enabled, save information
                    if upload!=None:
                        if upload.max_predict>pval:
                            upload.train(grid)

                    x.s_game(grid2)
                elif upload==None and k.sols==2:
                    x.confirmB["fg"]='#000000'
                    y = random.randint(0,len(x.diffs)-1)
                    print(f'Difficulty level: {y+1}')
                    x.s_game(generate(x.diffs[y],grid2).ans)
                    
                else:

                    #modify confirm text to red
                    x.confirmB["fg"] = '#FF0000'
        except:
            x.confirmB["fg"] = '#FF0000'            
    def f_upload_open_file(x):
        
        #Get file name then upload screen
        try:
            file = askopenfilename()
            x.s_upload_stage_2(Image.open(file),'B')
        except:
            x.openFileB["fg"]='#FF0000'
    def f_get_hint(x,hint=True):
        
        #Getting grid from entries (and sorting at the same time)
        f_label = font.Font(family="TkDefaultFont",size=17,weight="normal")
        grid=[]
        for q,entry in enumerate(x.entries):
            if type(entry)==tk.Text:

                #Getting entry text
                text = entry.get("1.0",tk.END)
                
                #Removing any spaces
                text = list(text)
                for i in range(len(text)-1,-1,-1):
                    if text[i]=='\n':
                        text.pop(i)
                    elif text[i]==' ':
                        text.pop(i)
                text = ''.join(text)

                if text == '':
                    text='0'

                #Error-checking text
                text2 = list(text)
                text2.sort()
                for i in range(10):
                    toggle=False
                    for j in range(len(text2)-1,-1,-1):
                        if text2[j]==str(i):
                            toggle=True
                            text2.pop(j)
                        elif text2[j] not in '0123456789':
                            text2.pop(j)
                    if toggle==True:
                        text2.append(str(i))
                text2 = ''.join(text2)
                if text2=='':
                    text2='0'
                
                #Updating text if incorrect (removing duplicate numbers, sorting, removing non numbers)
                if text2!=text:
                    x.entries[q].delete("1.0","end")
                    x.entries[q].insert("1.0",text2)
                    x.entries[q]['fg']='#0000ff'
                else:
                    x.entries[q]['fg']='#000000'
                
                #Adding entry contents to grid
                text2 = list(text2)
                for i in range(len(text2)):
                    text2[i] = int(text2[i])
                if text2[0]==0:
                    text2=[1,2,3,4,5,6,7,8,9]
                grid.append(text2)

            #If label, add label contents to grid
            elif type(entry)==tk.Label:
                x.entries[q]["fg"] = '#000000'
                x.entries[q]["bg"]= '#ffffff'
                x.entries[q].config(font=f_label)
                grid.append([int(entry["text"])])

        #making 2D grid 3D
        grid2 = []
        temp=[]
        for i in range(len(grid)):
            temp.append(grid[i])
            if i%9==8:
                grid2.append(temp)
                temp=[]

        #checking to see if already completed (if so terminate)
        complete=True
        for i in range(len(grid2)):
            for j in range(len(grid2[i])):
                if len(grid2[i][j])!=1 or str(grid2[i][j][0])!= x.game_solution.ans[9*i+j]:
                    complete=False
        if complete==True:
            #Placing uneditable labels where possible
            for i in range(len(grid2)):
                for j in range(len(grid2[i])):
                    if len(grid2[i][j])==1 and grid2[i][j][0]==int(x.game_solution.ans[9*i+j]) and type(x.entries[9*i+j])==tk.Text:
                        x.entries[9*i+j].delete("1.0","end")
                        x.entries[9*i+j].config(state=tk.DISABLED)
                        x.entries[9*i+j] = tk.Label(text=f"{str(grid2[i][j][0])}",master=x.entries[9*i+j].master,width=3,font=f_label)
                        x.entries[9*i+j]["bg"]='#ffffff'
                        x.entries[9*i+j].grid(row=i%3,column=j%3)
            
            #Removing available numbers
            for i in range(9):
                x.usedNumLabels[i]["text"]=' '

            x.checkB['fg']='#00ff00'
            x.hintB['fg']='#00ff00'
            x.solveB['fg']='#00ff00'

            x.checkB.configure(command=x.f_do_nothing)
            x.hintB.configure(command=x.f_do_nothing)
            x.solveB.configure(command=x.f_do_nothing)
            
            x.s_win()

        else:
            
            #Fetching new grid with only notes
            grid3 = []
            for q, entry in enumerate(x.entries):
                appended=False
                if type(entry)==tk.Text:
                    text = list(entry.get("1.0","end-1c"))
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
                        row, col, box = row_column_box(grid4,i,j)
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
                if grid2[i][j][0] != int(x.game_solution.ans[9*i+j]):
                    x.entries[9*i+j]['fg']='#ff0000'
                    x.errors+=1
                    x.errors_made_label["text"] = f'Errors: {x.errors}'
                    grid2[i][j]=[1,2,3,4,5,6,7,8,9]
                else:
                    x.entries[9*i+j].delete("1.0","end")
                    x.entries[9*i+j].config(state=tk.DISABLED)
                    x.entries[9*i+j] = tk.Label(text=f"{str(grid2[i][j][0])}",master=x.entries[9*i+j].master,width=3,font=f_label)
                    x.entries[9*i+j]["bg"]='#ffffff'
                    x.entries[9*i+j].grid(row=i%3,column=j%3)

            #Editing available numbers
            g = [0,0,0,0,0,0,0,0,0]
            for i in range(len(x.entries)):
                if type(x.entries[i])==tk.Label:
                    e = int(x.entries[i]["text"])-1
                    g[e] = g[e]+1
            for i in range(len(x.usedNumLabels)):
                if g[i]==9:
                    x.usedNumLabels[i]["text"]=' '

            #Hint feature
            if hint==True:
                
                for i in range(len(grid2)):
                    for j in range(len(grid2[i])):
                        if int(x.game_solution.ans[9*i+j]) not in grid2[i][j]:
                            grid2[i][j].append(int(x.game_solution.ans[9*i+j]))
                            grid2[i][j].sort()

                #iterating through the moves
                y = x.game_solution.next_move(grid2)[1][0]

                #Set hint label to tell which move was just executed
                x.hintLabel['text']=move_dict[y[0]]

                #Set move colour
                x.entries[y[1]*9+y[2]]['fg'] = '#ff00ff'

                #Add move set
                ystr=''
                for i in y[4]:
                    ystr+=(str(i))
                x.entries[y[1]*9+y[2]].delete('1.0',tk.END)
                x.entries[y[1]*9+y[2]].insert('1.0',ystr)
                
                x.hints+=1
                x.hints_used_label["text"] = f"Hints used: {x.hints}"                     
    def f_solve_game(x):
        f_label = font.Font(family="TkDefaultFont",size=17,weight="normal")
        for i, item in enumerate(x.entries):
            if type(x.entries[i])==tk.Text:
                x.entries[i].delete("1.0","end")
                x.entries[i].config(state=tk.DISABLED)
            y1 = i//9
            x1 = i%9
            item = tk.Label(text=f"{x.game_solution.ans[i]}",master=item.master,width=3,bg='#ffffff',font=f_label)
            item.grid(row=y1%3,column=x1%3)

        for i in range(9):
            x.usedNumLabels[i]["text"]=' '

        x.checkB['fg']='#ff0000'
        x.hintB['fg']='#ff0000'
        x.solveB['fg']='#ff0000'

        x.checkB.configure(command=x.f_do_nothing)
        x.hintB.configure(command=x.f_do_nothing)
        x.solveB.configure(command=x.f_do_nothing)
    def f_submit_score(x):
        name = x.score_entry.get()

        if len(name)<=16:
            time = round(x.final_time,2)
            grid = x.final_grid
            curDate = date.today()
            add_result(name,grid,curDate,time)
            x.win_window.destroy()
        else:
            x.submit_button["fg"]='#FF0000'      
    def f_return_query(x):
        f_main = font.Font(family="TkDefaultFont",size=10,weight="normal")
        title_relief = tk.RAISED

        name_w = 16
        grid_w = 20
        date_w = 12
        time_w = 10
        play_w = 5


        for child in x.query_frame.winfo_children():
            child.destroy()

        x.query_frame = tk.Frame(height=30)
        results_queries = []

        nameLbl = tk.Label(text='Name',master=x.query_frame,width=name_w,font=f_main,relief=title_relief)
        gridLbl = tk.Label(text='Grid',master=x.query_frame,width=grid_w,font=f_main,relief=title_relief)
        dateLbl = tk.Label(text='Date',master=x.query_frame,width=date_w,font=f_main,relief=title_relief)
        timeLbl = tk.Label(text='Time',master=x.query_frame,width=time_w,font=f_main,relief=title_relief)
        emptyLbl = tk.Button(text=' ',master=x.query_frame,font=f_main,width=play_w)

        name = x.searchNameE.get()
        grid = x.searchGridE.get()

        results = search_result(name,grid)

        nameLbl.grid(row=0,column=0)
        gridLbl.grid(row=0,column=1)
        dateLbl.grid(row=0,column=2)
        timeLbl.grid(row=0,column=3)
        emptyLbl.grid(row=0,column=4)

        if len(results)!=0:
            try:
                results_queries.append([tk.Label(text=results[0][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[0][1],master=x.query_frame,anchor="w",width=grid_w,font=f_main),tk.Label(text=results[0][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f"{int(results[0][3]//60)}m {int(round(results[0][3]%60))}s",master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[0][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[1][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[1][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[1][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[1][3]//60)}m {int(round(results[1][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[1][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[2][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[2][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[2][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[2][3]//60)}m {int(round(results[2][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[2][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[3][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[3][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[3][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[3][3]//60)}m {int(round(results[3][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[3][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[4][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[4][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[4][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[4][3]//60)}m {int(round(results[4][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[4][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[5][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[5][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[5][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[5][3]//60)}m {int(round(results[5][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[5][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[6][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[6][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[6][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[6][3]//60)}m {int(round(results[6][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[6][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[7][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[7][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[7][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[7][3]//60)}m {int(round(results[7][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[7][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[8][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[8][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[8][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[8][3]//60)}m {int(round(results[8][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[8][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[9][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[9][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[9][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[9][3]//60)}m {int(round(results[9][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[9][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[10][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[10][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[10][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[10][3]//60)}m {int(round(results[10][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[10][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[11][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[11][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[11][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[11][3]//60)}m {int(round(results[11][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[11][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[12][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[12][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[12][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[12][3]//60)}m {int(round(results[12][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[12][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[13][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[13][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[13][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[13][3]//60)}m {int(round(results[13][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[13][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
                results_queries.append([tk.Label(text=results[14][0],master=x.query_frame,width=name_w,font=f_main),tk.Label(text=results[14][1],master=x.query_frame,anchor='w',width=grid_w,font=f_main),tk.Label(text=results[14][2],master=x.query_frame,width=date_w,font=f_main),tk.Label(text=f'{int(results[14][3]//60)}m {int(round(results[14][3]%60))}s',master=x.query_frame,width=time_w,font=f_main),tk.Button(text='Play',command=lambda:x.s_game(results[14][1]),master=x.query_frame,width=play_w,font=f_main,relief=title_relief)])
            except:
                pass

            for i, result in enumerate(results_queries):
                for j in range(len(result)):
                    result[j].grid(row=i+1,column=j)

        x.query_frame.grid(row=2,column=0)
    def f_check_grid_string(x):
        try:
            stri = flatten(clipboard.paste())
            k = algorithm_x(stri,solving='')
            if k.sols==1:
                x.s_game(stri)
            else:
                x.clipStriB["fg"] = '#FF0000'
        except:
            x.clipStriB["fg"] = '#FF0000'
    def f_clear_grid(x):
        for i in range(len(x.entries)):
            if type(x.entries[i])==tk.Text:
                x.entries[i].delete("1.0","end")
    def f_do_nothing(x):
        pass
