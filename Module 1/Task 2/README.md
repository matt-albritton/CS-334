Read me for CPSC 334 - Module 1 Task 2
Matt Albritton
"The Sparkles of Life"

This document describes the structure and usage of "The Sparkles of Life" instillation for CCAM room 107. The complete / final file is "myGameOfLide_spaceships.pde". 

To run:
Download the file "myGameOfLide_spaceships.pde"- open it in Processing 4.x. The file must be in a folder of the same name, but processing will do this automatically if not done properly. If ran on the desktop in CCAM 107, the code will detect the second monitors and display as desired. The projectors must be turned on and connected properly.


Code Structure:
The code is structured on top of a simple 2d array, holding colors of the cells. Black means dead - any other color is alive.
This array is than displayed (with a specific transofmration for the six displays) with circles on each cell. The cell size and circle size can be set manually in global variables.
Based off an interval timer, the "iterate" function is called, which will go through the cell array and run the rules and update the array as needed for the next iteration (this is done with the help up a cloned buffer array). Within this iteration the r, g, and b values are averaged together (with a square / square root method) and a new cell will be the average of the other 3 cells.
Within "Draw()", the scene is updated at a framerate set in setup. It goes through the array and will display the cells as needed through the transformation. In addition, this is where the opacity is set. The opacity offset is calculated based on the time until the next interval, and is used to have the cells fade into existance, and fade out of existance. 
Spaceships are added in the "addRandom()" function, where in intervals specified by newInterval variable, a new spaceship is added randomly above or below any screen. 
Colors are determined by the x position of the pixel, and are pre-determined by screen.
Lastly positionDisplay() is used at setup to find the dimenstions of the two extra monitors and set the size of the screen to cover the two monitors, and place it so it covers them all.

Video:
https://drive.google.com/file/d/1vQZKC7I46I4SckacObwdyyDbudMcoSmI/view?usp=sharing

