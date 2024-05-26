# sudoku_nea / SmartSudoku

---

### Description
This is my first project which I used for my A level Computer Science NEA (non-exam assessment), which was worth 20% of my A level grade.   
I initially set out to create a Sudoku solver as I was regularly playing the game at the time, and this was completed relatively quickly.    
However, I wanted to try out neural networks for the first time, and so I built an object detection system / R-CNN, allowing inputting of a Sudoku grid from an image.   
Since then, I have been continually building this project, working on implementing a variety of new features.   

---

### Legacy (working) version
Please note the current repository may not run/be fully functional as I work on adding new features.   
If you would like to try out the legacy version of this application, check out the link below:  

https://github.com/sam7676/sudoku_nea/tree/df9d3c556937f8632f38d3170dc2bb4d8edaa396   

---
### Current state
This project is currently being expanded heavily.   
So far, I have:   
- implemented an account system with logins
- separated the project into a client exe and a server application to support multiple users running the same server

To-do - I am currently working on/look to improve in the future:   
- rewriting the codebase to clean up any messiness set from a few years ago
- improving the app's UI
- using YOLO instead of R-CNN for a massive speed increase
- introducing multiplayer
- adding support for killer sudoku
- adding a killer sudoku solver
- adding a killer sudoku object detection system
- transforming the project into a web project / web app, to be played on a variety of devices

---

### Features
- **Solver**: Able to solve any grid using a constraint programming solver or a backtracking solver
- **Hint feature**: Utilising the constraint programming solver, click on the hint feature for labelled suggestions on what to do next. Repeatedly clicking the hint feature will result in the constraint solver completing the game for you.
- **Generator**: Generates a grid with a unique solution. Includes a difficulty setting
- **Leaderboard**: Each grid contains a leaderboard with name and time taken to solve
- **Object detection system**: Takes an image as input and processes any Sudoku grids within the image into the app

---

### Upcoming features
- **Account**: Contains recent games played and time taken. Necessary for multiplayer
- **Multiplayer matches**: Two users will be matched together and assigned a grid, with the aim to complete the grid before the other.
- **ELO ranking system**: Matches will have the option to be competitive, using an ELO system to amend rankings after each match
- **Multiplayer play-together**: Users will be able to collaborate together on a grid, sharing notes in real-time
- **Killer Sudoku**: Will implement Killer Sudoku once I've done all the above

---
