This is the control code to be uploaded to the ESP32 for my Module 4 build. It controls a small "rc car" that is controlled
via bluetooth from the BlueFruit app. It combines the BLE_uart example from esp32, as well as the AccelStepper library
and the esp32Servo library. It allows the user to connect to the device via bluetooth on the app, and after opening the
accelerometer, control the car.

This code will create a bluetooth signal automatically, and all that needs to be done is use the BlueFruit app to connect
and open an accelerometer from the control tab. 
