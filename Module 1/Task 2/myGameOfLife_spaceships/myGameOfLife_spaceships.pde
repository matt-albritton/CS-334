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
 
import java.awt.GraphicsEnvironment;
import java.awt.GraphicsDevice;


// Size of cells
int cellSize = 2;
int circleSize = 8;

// How likely for a cell to be alive at start (in percentage)
float probabilityOfAliveAtStart = 10;
float probabilityOfAliveDuring = 50;
float probAliveMid = 0;


// Variables for timer
float interval = 200;
float lastRecordedTime = 0;

//variables for new cells
float newInterval = interval*2;
int newLastRecordedTime = 0;
int newShips = 1;

// Colors for active/inactive cells
color alive = color(0, 200, 0);
color dead = color(0);
float opacity = 75;
float oOffset = 0;
//int oInterval = interval / opacity;
int oLastTime = 0;

//edges set up:
int vertExtra = 10;
int horzExtra = 0;
int fullWidth;
int fullHeight;
int simHeight, simWidth;

// Array of cells
color[][] cells; 
// Buffer to record the state of the cells and use this 
// while changing the others in the interations
color[][] cellsBuffer; 


// Pause
boolean pause = false;

void setup() {
  //for automatic display position and size
  //positionDisplay();
  size (2040, 192); //1/4 of ccam display

  //size (576, 170); // 1/8
  //size (1152, 340); //1/4
  //size (2304, 680); // 1/2
  //size (2040, 192); //1/4 of ccam display
  simHeight=width/6;
  simWidth=height*6;
  fullWidth = simWidth/cellSize + (2*horzExtra);
  fullHeight = simHeight/cellSize + (2*vertExtra);
  
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
  for (int x=0; x<simWidth/cellSize; x++) {
    for (int y=0; y<simHeight/cellSize; y++) {
      noStroke();
      if (cells[x+horzExtra][y+vertExtra]!=#000000 || cellsBuffer[x+horzExtra][y+vertExtra]!=#000000) {
        
//position transformation**********************************
        int projW = height/cellSize;
        int newY = projW - (x%projW);
        int newX;
        if (x < ((simWidth/cellSize) / 2)){
          newX = y + ((simHeight/cellSize) * (2-(x/projW)));}
        else{
          newX = y + ((simHeight/cellSize) * (3+(5-(x/projW))));}
//*********************************************************
        if (cells[x+horzExtra][y+vertExtra]!=#000000 && cellsBuffer[x+horzExtra][y+vertExtra]!=#000000) {
          fill(cells[x+horzExtra][y+vertExtra], opacity); // If stayed alive
          circle(newX*cellSize,newY*cellSize,circleSize);
        }
        else if (cells[x+horzExtra][y+vertExtra]!=#000000){
          fill(cells[x+horzExtra][y+vertExtra], oOffset); // If new alive
          circle(newX*cellSize,newY*cellSize,circleSize);
        }
        else{
          fill(cellsBuffer[x+horzExtra][y+vertExtra], opacity-oOffset); // If dying
          circle(newX*cellSize,newY*cellSize,circleSize);
        }
      }
    }
  }
  
  
  
  // Iterate if timer ticks
  if (millis()-lastRecordedTime>interval) {
    //addRandom();
    iteration();
    //addRandom();
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
  for (int i=0; i < newShips; i++){
    float fx = 10 + random(fullWidth - 20);
    int x = int(fx);
    if (random(1) > 0.5){
      cells[x][5] = getColor(x,5);
      cells[x-1][5] = getColor(x,5);
      cells[x-2][5] = getColor(x,5);
      cells[x-3][4] = getColor(x,5);
      cells[x][4] = getColor(x,5);
      cells[x][3] = getColor(x,5);
      cells[x][2] = getColor(x,5);
      cells[x-1][1] = getColor(x,5);
      cells[x-3][1] = getColor(x,5);
    }
    else{
      cells[x][fullHeight-5] = getColor(x,5);
      cells[x-1][fullHeight-5] = getColor(x,5);
      cells[x-2][fullHeight-5] = getColor(x,5);
      cells[x-3][fullHeight-4] = getColor(x,5);
      cells[x][fullHeight-4] = getColor(x,5);
      cells[x][fullHeight-3] = getColor(x,5);
      cells[x][fullHeight-2] = getColor(x,5);
      cells[x-1][fullHeight-1] = getColor(x,5);
      cells[x-3][fullHeight-1] = getColor(x,5);
    }
  }
}

color getColor(int x, int y){
  int sixth = (simWidth / cellSize) / 6;
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
     



//--------------------------------------------------------------------------
void positionDisplay() {
  surface.setResizable(true);
  
  GraphicsEnvironment g = GraphicsEnvironment.getLocalGraphicsEnvironment();
  GraphicsDevice[] devices = g.getScreenDevices();
  
  int bigWidth = 0;
  int bigHeight = 0;
  
  int smallWidth = 0;
  int smallHeight = 0;
  
  for(int i = 0; i < devices.length; i++) {
    float currWidth = devices[i].getDisplayMode().getWidth();
    float currHeight = devices[i].getDisplayMode().getHeight();
    float ratio = currWidth / currHeight;
    if(ratio > 2.0) {
      bigWidth = Math.round(currWidth);
      bigHeight = Math.round(currHeight);
    } else {
      smallWidth = Math.round(currWidth);
      smallHeight = Math.round(currHeight);
    }
  }
  
  surface.setSize(bigWidth * 2, bigHeight);
  surface.setLocation(smallWidth - 100, -30);
}
