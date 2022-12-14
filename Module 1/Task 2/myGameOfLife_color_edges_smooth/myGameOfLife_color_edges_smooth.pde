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
int circleSize = 25;

// How likely for a cell to be alive at start (in percentage)
float probabilityOfAliveAtStart = 10;
float probabilityOfAliveDuring = 30;

// Variables for timer
float interval = 200;
float lastRecordedTime = 0;

//variables for new cells
int newInterval = 500;
int newLastRecordedTime = 0;

// Colors for active/inactive cells
color alive = color(0, 200, 0);
color dead = color(0);
float opacity = 40;
float oOffset = 0;
//int oInterval = interval / opacity;
int oLastTime = 0;

//edges set up:
int vertExtra = 40;
int horzExtra = 40;
int fullWidth = 570/cellSize + (2*horzExtra);
int fullHeight = 170/cellSize + (2*vertExtra);

// Array of cells
color[][] cells; 
// Buffer to record the state of the cells and use this 
// while changing the others in the interations
color[][] cellsBuffer; 

// Pause
boolean pause = false;

void setup() {
  size (576, 170); // 1/8
  //size (1152, 340); //1/4
  //size (2304, 680); // 1/2
  fullWidth = width/cellSize + (2*horzExtra);
  fullHeight = height/cellSize + (2*vertExtra);
  
  // Instantiate arrays 
  cells = new color[fullWidth][fullHeight];
  cellsBuffer = new color[fullWidth][fullHeight];

  // This stroke will draw the background grid
  stroke(48);

  noSmooth();

  // Initialization of cells
  for (int x=0; x<fullWidth; x++) {
    for (int y=0; y<fullHeight; y++) {
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
        //cells[x][y] = getColor(x,y);
      }
      cellsBuffer[x][y] = #000000; // Save state of each cell
    }
  }
  // Fill in black in case cells don't cover all the windows
  background(0); 
}


void draw() {
  clear();

  oOffset = ((millis()-lastRecordedTime)/interval) * opacity;

  //if (millis()-oLastTime>oInterval) {
  //  oOffset = oOffset + 1;
  //  oLastTime = millis();
  //  if (oOffset > opacity){
  //    oOffset = 0;
  //  }
  //}

  //Draw grid
  for (int x=0; x<width/cellSize; x++) {
    for (int y=0; y<height/cellSize; y++) {
      noStroke();
      if (cells[x+horzExtra][y+vertExtra]!=#000000 || cellsBuffer[x+horzExtra][y+vertExtra]!=#000000) {
        if (cells[x+horzExtra][y+vertExtra]!=#000000 && cellsBuffer[x+horzExtra][y+vertExtra]!=#000000) {
          fill(cells[x+horzExtra][y+vertExtra], opacity); // If alive
          circle(x*cellSize,y*cellSize,circleSize);
        }
        else if (cells[x+horzExtra][y+vertExtra]!=#000000){
          fill(cells[x+horzExtra][y+vertExtra], oOffset); // If alive
          circle(x*cellSize,y*cellSize,circleSize);
        }
        else{
          fill(cellsBuffer[x+horzExtra][y+vertExtra], opacity-oOffset); // If alive
          circle(x*cellSize,y*cellSize,circleSize);
        }
      }
    }
  }
  
  
  // Iterate if timer ticks
  if (millis()-lastRecordedTime>interval) {
    iteration();
    lastRecordedTime = millis();
    oOffset = 0;
    oLastTime = millis();

  }
  // Iterate if longer random timer ticks
  if (millis()-newLastRecordedTime>newInterval) {
    addRandom();
    newLastRecordedTime = millis();
  }
}


void iteration() { // When the clock ticks
  // Save cells to buffer (so we opeate with one array keeping the other intact)
  for (int x=0; x<fullWidth; x++) {
    for (int y=0; y<fullHeight; y++) {
      cellsBuffer[x][y] = cells[x][y];
    }
  }

  // Visit each cell:
  for (int x=0; x<fullWidth; x++) {
    for (int y=0; y<fullHeight; y++) {
      // And visit all the neighbours of each cell
      float rTotal = 0;
      float gTotal = 0;
      float bTotal = 0;
      int neighbours = 0; // We'll count the neighbours
      for (int xx=x-1; xx<=x+1;xx++) {
        for (int yy=y-1; yy<=y+1;yy++) {  
          if (((xx>=0)&&(xx<fullWidth))&&((yy>=0)&&(yy<fullHeight))) { // Make sure you are not out of bounds
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
        if (neighbours == 3) {
          cells[x][y] = color((rTotal/neighbours), (gTotal/neighbours), (bTotal/neighbours)); // Only if it has 3 neighbours
        }
      } // End of if
    } // End of y loop
  } // End of x loop
} // End of function


void addRandom(){
// Restart: reinitialization of cells
  for (int x=0; x<fullWidth; x++) {
    for (int y=0; y<fullHeight; y++) {
      if(x>horzExtra-5 && y>vertExtra-5 && x<(fullWidth-horzExtra+5) && y<(fullHeight-vertExtra+5)){
         break;
      }
      if (random(100) < probabilityOfAliveDuring) {
        float r = random(256);
        float g = random(256);
        float b = random(256);
        cells[x][y] = getColor(x,y);
        //if(x<fullWidth/2){
        //  cells[x][y] = color(255,0,0);
        //}
        //else{
        //  cells[x][y] = color(0,0,255);
        //}
      }
    }
  }
}

color getColor(int x, int y){
  int sixth = (width / cellSize) / 6;
  if (x < horzExtra + sixth){
      return #db2e2e;}
  else if (x < horzExtra + sixth*2){
      return #2edbd8;}
  else if (x < horzExtra + sixth*3){
      return #cd2edb;}
  else if (x < horzExtra + sixth*4){
      return #2edb34;}
  else if (x < horzExtra + sixth*5){
      return #dbb82e;}
  return #312edb;
}
     
    
