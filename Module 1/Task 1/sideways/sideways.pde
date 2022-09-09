
import java.awt.GraphicsEnvironment;
import java.awt.GraphicsDevice;

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

int x = 0;
void setup() {
  positionDisplay();
  print("1/3: " + width/3 + ". 2/3: " + width*2/3 + ". end: " + width);

}

void draw() {
  clear();
  setBackground();
  fill(100);
  //tint(255, 127);
  rect(0, 0, x, height);
  if (keyPressed){
    switch(keyCode){
      case LEFT:
        x = x - 1;
        break;
      case RIGHT:
        x = x + 1;
        break;
      case SHIFT:
        print("\n" + x);
        break;
      
    }
  }
  if (mousePressed && mouseButton == LEFT){
    x = mouseX;
  }
}

void setBackground(){
  fill(255,0,0);
  rect(0, 0, width/3, height);
  fill(0,255,0);
  rect(width/3, 0, width/3, height);
  fill(0,0,255);
  rect(width*2/3, 0, width/3, height);
}
