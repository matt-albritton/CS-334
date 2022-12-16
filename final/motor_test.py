#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
 
in1_1 = 2 
in2_1 = 3 
in3_1 = 4 
in4_1 = 17 

in1_2 = 22 
in2_2 = 10 
in3_2 = 9 
in4_2 = 11 

in1_3 = 6
in2_3 = 13
in3_3 = 19
in4_3 = 26
# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002
step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
direction = False # True for clockwise, False for counter-clockwise
 
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

motor_pins = [[in1_1,in2_1,in3_1,in4_1],[in1_2,in2_2,in3_2,in4_2], [in1_3,in2_3,in3_3,in4_3]] 
motors_step_counter = [0,0,0]
# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1_1, GPIO.OUT )
GPIO.setup( in3_1, GPIO.OUT )
GPIO.setup( in2_1, GPIO.OUT )
GPIO.setup( in4_1, GPIO.OUT )

GPIO.setup( in1_2, GPIO.OUT )
GPIO.setup( in3_2, GPIO.OUT )
GPIO.setup( in2_2, GPIO.OUT )
GPIO.setup( in4_2, GPIO.OUT )

GPIO.setup( in1_3, GPIO.OUT )
GPIO.setup( in3_3, GPIO.OUT )
GPIO.setup( in2_3, GPIO.OUT )
GPIO.setup( in4_3, GPIO.OUT )
# initializing
GPIO.output( in1_1, GPIO.LOW )
GPIO.output( in2_1, GPIO.LOW )
GPIO.output( in3_1, GPIO.LOW )
GPIO.output( in4_1, GPIO.LOW )

GPIO.output( in1_2, GPIO.LOW )
GPIO.output( in2_2, GPIO.LOW )
GPIO.output( in3_2, GPIO.LOW )
GPIO.output( in4_2, GPIO.LOW )

GPIO.output( in1_3, GPIO.LOW )
GPIO.output( in2_3, GPIO.LOW )
GPIO.output( in3_3, GPIO.LOW )
GPIO.output( in4_3, GPIO.LOW )

motor_positions = [0, 0, 0]
num_places = 12
 
 
 
def cleanup():
    GPIO.output( in1_1, GPIO.LOW )
    GPIO.output( in2_1, GPIO.LOW )
    GPIO.output( in3_1, GPIO.LOW )
    GPIO.output( in4_1, GPIO.LOW )

    GPIO.output( in1_2, GPIO.LOW )
    GPIO.output( in2_2, GPIO.LOW )
    GPIO.output( in3_2, GPIO.LOW )
    GPIO.output( in4_2, GPIO.LOW )
    
    GPIO.output( in1_3, GPIO.LOW )
    GPIO.output( in2_3, GPIO.LOW )
    GPIO.output( in3_3, GPIO.LOW )
    GPIO.output( in4_3, GPIO.LOW )
 
 
def travel(motor, steps):
    try:
        i = 0
        for i in range(steps):
            for pin in range(0, len(motor_pins[motor])):
                GPIO.output( motor_pins[motor][pin], step_sequence[motors_step_counter[motor]][pin] )
            if direction==True:
                motors_step_counter[motor] = (motors_step_counter[motor] - 1) % 8
            elif direction==False:
                motors_step_counter[motor] = (motors_step_counter[motor] + 1) % 8
            else: # defensive programming
                print( "uh oh... direction should *always* be either True or False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )
    except KeyboardInterrupt:
        cleanup()
        exit
    cleanup()
# time.sleep(3)

def goTo(motor, position):
    global motor_positions
    goal = (position/num_places)*4096
    if (motor_positions[motor] < goal):
        to_get_there = goal-motor_positions[motor]
    else:
        to_get_there = 4096-motor_positions[motor] + goal
    motor_positions[motor] = goal
    travel(motor, int(to_get_there))

def parseInput(name, place):
    pos = 0
    if name == "matt":
        motor = 0
    elif name == "caleb":
        motor = 1
    elif name == "ben":
        motor=2
    else:
        print("not valid name")
    if place == "Home":
        pos = 0
    elif place ==  "Work":
        pos = 1
    elif place ==  "Dorm":
        pos = 2
    elif place ==  "West":
        pos = 3
    elif place ==  "Traveling":
        pos = 4
    else:
        print("location wasn't matched w/ clock. sending home")
    goTo(motor, pos)
        
        



def main():
    parseInput("matt", "Home")
    parseInput("caleb", "Home")
    parseInput("ben", "Home")




if __name__ == '__main__':
    main()
    GPIO.cleanup()
