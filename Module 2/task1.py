import time
from gpiozerio import Button, PWMLED

button = Button(2)
switch = Button(3)
joystick = Button(4)
joystick_x = Button(5)
joystick_y = Button(6)
red = PWMLED(7)
blue = PWMLED(8)

red.value = 1
blue.value = 1

while True:
    if button._ispressed:
        print("button is pressed")
    else:
        print("button is not pressed")
    if switch._ispressed:
        print("switch is off")
    else:
        print("switch is not off")
    if joystick._ispressed:
        print("joystick is pressed")
    else:
        print("joystick is not pressed")
    if joystick_x._ispressed:
        print("joystick is left")
    else:
        print("joystick is not left")
    if joystick_y._ispressed:
        print("joystick is up")
    else:
        print("joystick is not up")