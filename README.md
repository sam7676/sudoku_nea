# sudoku_nea

This is my first project which I used for my A level Computer Science NEA (non-exam assessment), which was worth 20% of my A level grade.
I initially set out to create a Sudoku solver as I was regularly playing the game at the time, and this was completed relatively quickly. 
However, I wanted to try out neural networks for the first time, and so I built an object detection system / R-CNN involving inputting a Sudoku grid from a given image.
I also needed for my project some sort of persistent storage, so I created a database storing name, grid, time and date.

This was then all merged to build a full-scale app using Tkinter. 
Most of my time was spent developing an additional hint system that fetches the grid from the application and figures out the next move to do.
Putting all this together I created this fully-working Sudoku app.

To get it to work, download all the files, install all necessary libraries, click on "Debug" upon launch and train both the digits and grid to get the neural networks.
Note that these files are big, may take several minutes to train (depending on your processing power), and take up to 500MB each.
