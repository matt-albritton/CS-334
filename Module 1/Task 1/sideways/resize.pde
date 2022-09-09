import java.awt.GraphicsEnvironment;
import java.awt.GraphicsDevice;

void positionDisplay() {
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
      break;
    } else {
      smallWidth = Math.round(currWidth);
      smallHeight = Math.round(currHeight);
    }
  }
  
  surface.setSize(bigWidth * 2, bigHeight);
  surface.setLocation(100, 100);
}

void setup() {
  surface.setResizable(true);
  positionDisplay();
}
