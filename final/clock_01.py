#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timedelta
 
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
num_places = 13

away = [False, False, False]
times_away = [datetime.now(), datetime.now(), datetime.now()]
 
 
 
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
 

def on_connect(client, userdata, flags, rc):
    global loop_flag
    print("Connected with result code "+str(rc))
    loop_flag=0
    client.publish("pi", "connected")
    client.subscribe("test")
    client.subscribe("matt")
    client.subscribe("caleb")
    client.subscribe("ben")


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))
    data = json.loads(msg.payload.decode("utf-8"))
    # print("len data: " + str(len(data)))
    # print("len regs: " + str(len(regs)))
    if not "inregions" in data:
        print(f"{msg.topic} Traveling")
        checkAway(msg.topic)
        # parseInput(msg.topic, "Traveling")
        return;
    regs = data["inregions"]
    if len(regs) > 1  and regs[0] == 'School':
        location = regs[1]
    else:
        location = regs[0]
    print(f"{msg.topic} to {location}")
    parseInput(msg.topic, location)


def checkAway(name):
    if name == "matt":
        index = 0
    elif name == "caleb":
        index = 1
    elif name == "ben":
        index=2
    else:
        print("bad name.")
        return
    
    if away[index] == False:
        times_away[index] = datetime.now()
        away[index] == True
        parseInput(name, "Traveling")
        return
    if datetime.now() - timedelta(hours=14) > times_away[index]:
        parseInput(name, "Mortal Peril")
        return
    if datetime.now() - timedelta(hours=4) > times_away[index]:
        parseInput(name, "Lost")
        return
    parseInput(name, "Traveling")
    return


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
        exit(1)
    cleanup()
# time.sleep(3)

def goTo(motor, position):
    global motor_positions
    goal = (position/num_places)*4096
    if (goal == motor_positions[motor]):
        print("already there")
        return
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
    elif place ==  "South Pole":
        pos = 1
    elif place ==  "Lamb Creek":
        pos = 2
    elif place ==  "North Pole":
        pos = 3
    elif place ==  "Work":
        pos = 4
    elif place ==  "Mortal Peril":
        pos = 5
    elif place ==  "School":
        pos = 6
    elif place ==  "The Gym":
        pos = 7
    elif place ==  "Out West":
        pos = 8
    elif place ==  "Lost":
        pos = 9
    elif place ==  "Apartment":
        pos = 10
    elif place ==  "Traveling":
        pos = 11
    elif place ==  "At Sea":
        pos = 12
        
    else:
        print("location wasn't matched w/ clock. sending home")
    goTo(motor, pos)
        
        



def main():
    try:
        client = mqtt.Client("pi")
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(username="xoemllsy", password="hdgazSRFNst3")
        print("connecting...")
        client.connect("farmer.cloudmqtt.com", port=14479)
        client.loop_forever()
    except:
        print("returning all to 0...")
        goTo(0,0)
        goTo(1,0)
        goTo(2,0)
        cleanup()
        print("Cleaned up. Bye!")
        # print(e)
        exit(1)





if __name__ == '__main__':
    main()
