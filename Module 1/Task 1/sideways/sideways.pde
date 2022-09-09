
int x = 0;
void setup() {
  size(640, 360);
  //fullScreen();
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
