# sudoku_nea

This is my first project which I used for my A level Computer Science NEA (non-exam assessment), which was worth 20% of my A level grade.
I initially set out to create a Sudoku solver as I was regularly playing the game at the time, and this was completed relatively quickly. 
However, I wanted to try out neural networks for the first time, and so I built an object detection system / R-CNN, allowing inputting of a Sudoku grid from an image.

Features:
- **Solver**: I developed my own constraint programming solver, able to use information about the board to update it and reduce possibilities, similar to how a human would play Sudoku. I also incorporated code for Algorithm X, an optimised backtracking solver, which is used to quickly get the number of solutions to a given grid.
- **Hint feature**: Utilising the constraint programming solver, a human can click on the hint feature for labelled suggestions on what to do next. Repeatedly clicking the hint feature will result in the constraint solver completing the game for you.
- **Generator**: A feature capable of generating a Sudoku grid with a unique solution. Difficulty levels are also included, which are based on the number of iterations the generator may take. I utilised Algorithm X to randomly create a solved game, and I removed numbers repeatedly until the game was unique. Finally, I evaluated how long this game would take to solve using my constraint solver.
- **Leaderboard**: Once players complete the game, they may upload their name, the grid they solved, and the time taken, to a leaderboard. This leaderboard can be searched by name and grid to find grids previously players have completed and compare scores.
- **Object detection system**: This system is capable of inputting any given image, searching this image for any Sudoku grids, grabbing the grid using a bounding box, reading the numbers in the grid, and inputting it into the application to play. Also, this is a self-updating system, and images sent in are used for training and are uploaded using a data pipeline. This uses selective search to find regions of high interest within the initial image, then a neural network to choose the region with maximal probability of being a grid. This grid is then split up into 81 cells, which go through a second neural network for classifying the digits.
- **Reinforcement learning trainer**: This feature is more of a play-around feature, but users can upload a 4x4 grid with a unique solution and watch a Deep Q-Network attempt to learn to backtrack. Initially, the trainer attempts randomly guessing the value of each cell, however it can begin to learn whether a given guess is good or bad and eventually is able to learn the solution.

If you want to understand the code, I have inserted comments everywhere roughly explaining what each code section does. Additionally, in imports.py, I have documented all my important subroutines and useful class attributes and explained what they do.

To get it to work, download all the files, install all necessary libraries, click on "Train" upon launch and train both the digits and grid to save the neural networks to your machine.
Note that these files are big, may take several minutes to train (depending on your processing power), and may take up to 500MB each.


CURRENTLY REVAMPING SUDOKU_NEA

SmartSudoku

- Client application
- Server in the background
- Pairing works through the server

Login
Register

Play
Leaderboard
Multiplayer
Train
Sign out

[Play]
Generate
Create custom
Image upload
Back

[Leaderboard]
Board times
ELO ranking

[Multiplayer]
Your ELO
Random match
Play a friend [enter username]

Server
Table 1
Username | password (hashed) | ELO

Table 2
Username | board ID | date | time taken

Training will be ran on server, and compiled into client

Codebase:
server 
    database.py
    database.sqlite
    yolo_training.py
    digit_training.py
    multiplayer_hosting.py
    run_server.py // calls other files with a HTTP call
client
    // bundled into .exe
    solver.py [updated]
    object_detection.py
    front_end.py
    multiplayer.py
digits
    // images with annotations
grids
    // images with annotations
models
    // weights provided
images
    // any images loaded into the client

Project scope ideas
- Build into web app, expand into cloud
- Build into mobile app
- I want to try AR but this is a long way off