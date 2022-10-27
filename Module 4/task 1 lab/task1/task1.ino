//include libraries for each
#include <Stepper.h>
#include <ESP32Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position
int servoPin = 12;

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution

// ULN2003 Motor Driver Pins
#define IN1 17 //19
#define IN2 5 //18
#define IN3 18 //5
#define IN4 19 //17

// initialize the stepper library
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);

void setup() {
  // set the speed at 5 rpm
  myStepper.setSpeed(5);
  // initialize the serial port
  Serial.begin(115200);

  //servo:
  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(servoPin, 0, 3500); // attaches the servo on pin 18 to the servo object
}

void loop() {
  // step one revolution in one direction:
  myStepper.step(stepsPerRevolution);
  //pos = +10 degrees, reset at 180
  pos = (pos + 10) % 182;
  Serial.println(pos);
  //step servo 10 degrees
  myservo.write(int(pos));
  //if going back from 180 to 0, give it a bit more time
  if (pos == 0){
    delay (500);
  }
  delay(100);

}