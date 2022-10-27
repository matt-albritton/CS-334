
int pushButton = 15;
int joyButton = 21;
int powerButton = 22;
// int xIn = A6;
// int yIn = 23;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT_PULLUP);
  pinMode(joyButton, INPUT_PULLUP);
  pinMode(powerButton, INPUT_PULLUP);
  
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int buttonState = digitalRead(pushButton);
  int joyButtonState = digitalRead(joyButton);
  int power = digitalRead(powerButton);
  int xJoy = analogRead(A7);
  int yJoy = analogRead(A6);
  // print out the state of the button:
  Serial.println("Start");
  Serial.println(power);
  Serial.println(buttonState);
  Serial.println(joyButtonState);
  Serial.println(xJoy);
  Serial.println(yJoy);

  // Serial.write(power);
  // Serial.write(buttonState);
  // Serial.write(joyButtonState);
  // Serial.write(xJoy);
  // Serial.write(yJoy);
  if (power == 0){
    delay(30);
  }
  else{
    delay(75);        // delay in between reads for stability
  }
}
