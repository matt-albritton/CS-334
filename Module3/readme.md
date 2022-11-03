Module 3 Task 2
Matt Albritton

Pumpkin 

This project is a wifi based interactive art peiece. It consists of a physical pumpkin containing an ESP32 and sensors,
a bed with magenets, and a 5in monitor hooked to a raspberry pi 4. As the user interacts with the pumkpin - touches, moves etc -
an animated pumpkin on the screen reacts live with resulting emotions

This project has two scripts running: baby_sensor.ino running on the esp32, and comibned.py on the pi. The esp must be hooked
up to a peizo touch sensor and a Adafruit_MPU6050 accelerometer/gyro. The pi must be hooked up to the display.

The circuit diagram can be found on my Notion page- as well as futher explination of the project.

