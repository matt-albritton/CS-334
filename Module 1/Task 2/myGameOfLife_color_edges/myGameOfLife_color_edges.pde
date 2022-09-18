/**
 * Game of Life
 * by Joan Soler-Adillon.
 *
 * Press SPACE BAR to pause and change the cell's values 
 * with the mouse. On pause, click to activate/deactivate 
 * cells. Press 'R' to randomly reset the cells' grid. 
 * Press 'C' to clear the cells' grid. The original Game 
 * of Life was created by John Conway in 1970.
 */

// Size of cells
int cellSize = 5;
int circleSize = 20;

// How likely for a cell to be alive at start (in percentage)
float probabilityOfAliveAtStart = 30;
float probabilityOfAliveDuring = 0;

// Variables for timer
int interval = 50;
int lastRecordedTime = 0;

//variables for new cells
int newInterval = 100;
int newLastRecordedTime = 0;

// Colors for active/inactive cells
color alive = color(0, 200, 0);
color dead = color(0);
int opacity = 40;

// Array of cells
color[][] cells; 
// Buffer to record the state of the cells and use this 
// while changing the others in the interations
color[][] cellsBuffer; 

// Pause
boolean pause = false;

void setup() {
  size (570, 170);

  // Instantiate arrays 
  cells = new color[width/cellSize][height/cellSize];
  cellsBuffer = new color[width/cellSize][height/cellSize];

  // This stroke will draw the background grid
  stroke(48);

  noSmooth();

  // Initialization of cells
  for (int x=0; x<width/cellSize; x++) {
    for (int y=0; y<height/cellSize; y++) {
      float state = random (100);
      if (state > probabilityOfAliveAtStart) { 
        state = 0;
        cells[x][y] = #000000; 
      }
      else {
        state = 1;
        float r = random(256);
        float g = random(256);
        float b = random(256);
        cells[x][y] = color(r,g,b);
      }
      //cells[x][y] = int(state); // Save state of each cell
    }
  }
  // Fill in black in case cells don't cover all the windows
  background(0); 
}


void draw() {
  clear();

  //Draw grid
  for (int x=0; x<width/cellSize; x++) {
    for (int y=0; y<height/cellSize; y++) {
      if (cells[x][y]!=#000000) {
        noStroke();
        fill(cells[x][y], opacity); // If alive
        circle(x*cellSize,y*cellSize,circleSize);
      }
    }
  }
  // Iterate if timer ticks
  if (millis()-lastRecordedTime>interval) {
    if (!pause) {
      iteration();
      lastRecordedTime = millis();
    }
  }
  // Iterate if longer random timer ticks
  if (millis()-newLastRecordedTime>newInterval) {
    addRandom();
    newLastRecordedTime = millis();
  }
}


void iteration() { // When the clock ticks
  // Save cells to buffer (so we opeate with one array keeping the other intact)
  for (int x=0; x<width/cellSize; x++) {
    for (int y=0; y<height/cellSize; y++) {
      cellsBuffer[x][y] = cells[x][y];
    }
  }

  // Visit each cell:
  for (int x=0; x<width/cellSize; x++) {
    for (int y=0; y<height/cellSize; y++) {
      // And visit all the neighbours of each cell
      float rTotal = 0;
      float gTotal = 0;
      float bTotal = 0;
      int neighbours = 0; // We'll count the neighbours
      for (int xx=x-1; xx<=x+1;xx++) {
        for (int yy=y-1; yy<=y+1;yy++) {  
          if (((xx>=0)&&(xx<width/cellSize))&&((yy>=0)&&(yy<height/cellSize))) { // Make sure you are not out of bounds
            if (!((xx==x)&&(yy==y))) { // Make sure to to check against self
              if (cellsBuffer[xx][yy]!=#000000){
                neighbours ++; // Check alive neighbours and count them
                rTotal = rTotal + red(cellsBuffer[xx][yy]);
                gTotal = gTotal + green(cellsBuffer[xx][yy]);
                bTotal = bTotal + blue(cellsBuffer[xx][yy]);
                
              }
            } // End of if
          } // End of if
        } // End of yy loop
      } //End of xx loop
      // We've checked the neigbours: apply rules!
      if (cellsBuffer[x][y]!=#000000) { // The cell is alive: kill it if necessary
        if (neighbours < 2 || neighbours > 3) {
          cells[x][y] = #000000; // Die unless it has 2 or 3 neighbours
        }
      } 
      else { // The cell is dead: make it live if necessary      
//*******   MAKING ALIVE CELLS *******************************************************
        if (neighbours == 3 ) {
          cells[x][y] = color((rTotal/3), (gTotal/3), (bTotal/3)); // Only if it has 3 neighbours
        }
      } // End of if
    } // End of y loop
  } // End of x loop
} // End of function


void addRandom(){
// Restart: reinitialization of cells
  for (int x=0; x<width/cellSize; x++) {
    for (int y=0; y<height/cellSize; y++) {
      float state = random (100);
      if (state < probabilityOfAliveDuring) {
        state = 1;
        cells[x][y] = #FFFFFF; // Save state of each cell
      }
    }
  }
}
