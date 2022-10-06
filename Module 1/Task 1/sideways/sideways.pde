//Sideways is a program to help map projectors in CCAM 107
//it runs by displaying a large fullscreen window that has the length and width
//needed to span all 6 projectors. It displays RBG split into 3 segments (width-wise)
// and then lets the user click to move a gray bar horizontal(on computer display, 
//vertical on projector display) or use the arrow keys to place it. This can be placed
//in key parts of the screen, and pressing shift prints out that x coordinate.

//Import necessary java libs for screen mapping
import java.awt.GraphicsEnvironment;
import java.awt.GraphicsDevice;

//place the display in the top left corner of the second display
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
  surface.setLocation(smallWidth, 0);
}

//set up and call positionDisplay
int x = 0; //cur x cordinate of gray bar
void setup() {
  //positionDisplay();
  size (576,170);
  print("1/3: " + width/3 + ". 2/3: " + width*2/3 + ". end: " + width);

}


void draw() {
  clear();
  setBackground();  //set background as rgb
  fill(100);
  //tint(255, 127);
  rect(0, 0, x, height);  //draw grey rectangle to cur x coordinate
  if (keyPressed){  
    switch(keyCode){
      case LEFT:      //shift gray box left or right with arrows
        x = x - 1;
        break;
      case RIGHT:
        x = x + 1;
        break;
      case SHIFT:    //on shift print x value
        print("\n" + x);
        break;
      
    }
  }      //on click, move to xMouse
  if (mousePressed && mouseButton == LEFT){
    x = mouseX;
  }
}

//set background to 1/3 r, 1/3 g, 1/3b
void setBackground(){
  fill(255,0,0);
  rect(0, 0, width/3, height);
  fill(0,255,0);
  rect(width/3, 0, width/3, height);
  fill(0,0,255);
  rect(width*2/3, 0, width/3, height);
}
