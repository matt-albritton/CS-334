#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

import time
import random
import serial

#variables for incoming input
button = 1
push = 0
power = 0
xJoy = 0
yJoy =0

#variables for snake body and such
head = [32,32]
body = [[32,32], [32-1,32], [32-2,32], [32-3,32], [32-4,32]]
direction = 'RIGHT'
change = direction
length = 4
colors = False
continuum = 0
#fruit location
fruit = [random.randrange(4,60), random.randrange(4,60)]
#serial input setup
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#screen setup
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.gpio_slowdown = 4
matrix = RGBMatrix(options = options)
canvas = matrix
#colors and fonts
green = graphics.Color(0, 255, 0)
red = graphics.Color(255, 0, 0)
font = graphics.Font()
font.LoadFont("../raspberrypi/rpi-rgb-led-matrix/fonts/7x13.bdf")
smallFont = graphics.Font()
smallFont.LoadFont("../raspberrypi/rpi-rgb-led-matrix/fonts/6x10.bdf")

#main function
def main():
    #run once on main startup
    global head, body, direction, change, length, fruit, colors, continuum  #global variables
    #growth variables
    body_growing = False
    growth = 0;
    growth_per_fruit = 3
    #original colors for crazy color mode
    red_p = 0
    green_p =255 
    blue_p = 0
    release = True
    
    #start up display
    graphics.DrawText(canvas, font, 14, 30, green, "Snake")
    graphics.DrawText(canvas, smallFont, 12, 45, red, "by matt")
    time.sleep(1)
    while button != 0:
        if ser.in_waiting > 0 and "Start" == ser.readline().decode('utf-8').rstrip():
            getInfo()
    canvas.Clear()
    time.sleep(0.3)
    
    #clear input buffer before starting
    ser.reset_input_buffer()
    while True:
        #when you get info- and the first line is "start"
        if ser.in_waiting > 0 and "Start" == ser.readline().decode('utf-8').rstrip():
            #get info and put into coresponding global variables
            getInfo()
            canvas.Clear()
            
            #change directions as needed
            if xJoy < 200 and direction != 'LEFT':
                change = 'RIGHT'
            if yJoy > 4000 and direction != 'UP':
                change = 'DOWN'
            if yJoy < 200 and direction != 'DOWN':
                change = 'UP'
            if xJoy > 4000 and direction != 'RIGHT':
                change = 'LEFT'
            if change == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
            #change head position
            if direction == 'LEFT':
                head[0] -= 1
            if direction == 'RIGHT':
                head[0] += 1
            if direction == 'DOWN':
                head[1] += 1
            if direction == 'UP':
                head[1] -= 1
            
            # change colors if joystick is pressed 
            if push == 0 and colors == True and release == True:
                colors = False
                release = False
            elif push == 0 and colors == False and release == True:
                colors = True
                release = False
            if push == 1:       #released used to not change colors over and over
                release = True
            
            if colors == True:
                continuum += 5
                continuum %= 3 * 255
                if continuum <= 255:
                    c = continuum
                    blue_p = 255 - c
                    red_p = c
                elif continuum > 255 and continuum <= 511:
                    c = continuum - 256
                    red_p = 255 - c
                    green_p = c
                else:
                    c = continuum - 512
                    green_p = 255 - c
                    blue_p = c
                my_color = graphics.Color(red_p, green_p, blue_p)
            else:
                my_color = green

            #body grows
            body.insert(0, list(head))
            if fruit[0] -1 <= head[0] <= fruit[0]+1 and fruit[1]-1 <= head[1] <=fruit[1]+1:
                length += 1
                fruit = [random.randrange(4,60), random.randrange(4,60)]
                body_growing = True
            if body_growing:
                growth += 1
                if growth > growth_per_fruit:
                    growth = 0
                    body_growing = False
            else:
                body.pop()

            #around edges
            if head[0] > 64 :
                head[0] -= 64
            if head[0] < 0:
                head[0] += 64
            if head[1] > 64 :
                head[1] -= 64
            if head[1] < 0:
                head[1] += 64
            #draw body
            for pos in body:
                graphics.DrawCircle(canvas, pos[0], pos[1],1, my_color)
            graphics.DrawCircle(canvas, fruit[0], fruit[1],1, red)
            
            #crash
            for pos in body[1:]:
                if head[0] == pos[0] and head[1] == pos[1]:
                    gameOver()
                    break
            
            graphics.DrawText(canvas, smallFont, 2, 62, red, str(length))
            if button == 0:
                gameOver()




    # except KeyboardInterrupt:
    #     sys.exit(0)


def gameOver():
    global head, body, direction, change, length, fruit, button, ser
    canvas.Clear()
    graphics.DrawText(canvas, font, 18, 20, red, "Game")
    graphics.DrawText(canvas, font, 18, 35, red, "Over")
    graphics.DrawText(canvas, font, 25, 50, green, str(length))
    button = 1
    time.sleep(1)
    ser.reset_input_buffer()
    if ser.in_waiting > 0 and "Start" == ser.readline().decode('utf-8').rstrip():
            getInfo()
    while button != 0:
        if ser.in_waiting > 0 and "Start" == ser.readline().decode('utf-8').rstrip():
            getInfo()
    x = 32
    y = 32
    head = [x,y]
    body = [[x,y], [x-1,y], [x-2,y], [x-3,y], [x-4,y]]
    direction = 'RIGHT' 
    change = direction
    length=4
    fruit = [random.randrange(4,60), random.randrange(4,60)]
    button = 1    
    time.sleep(0.2)
    ser.reset_input_buffer()
    





def getInfo():
    global power, button, push, xJoy, yJoy, ser
    power = int(ser.readline().decode('utf-8').rstrip())
    button = int(ser.readline().decode('utf-8').rstrip())
    push = int(ser.readline().decode('utf-8').rstrip())
    xJoy = int(ser.readline().decode('utf-8').rstrip())
    yJoy = int(ser.readline().decode('utf-8').rstrip())
    print(power, button, push, xJoy, yJoy)



if __name__ == '__main__':
    main()
