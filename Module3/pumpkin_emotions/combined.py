# importing required library
import pygame
import time
import socket
from statistics import mean
 
#socket setup
UDP_IP = "172.29.27.189"
UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

X = 800
Y = 480

# activate the pygame library .
pygame.init()

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y), pygame.FULLSCREEN)
#scrn = pygame.display.set_mode((X, Y))

scrn.fill((110, 63, 107))
font = pygame.font.Font('freesansbold.ttf', 32)


# set the pygame window name
pygame.display.set_caption('image')

angry = pygame.image.load("angry.jpg").convert()
sleeping = pygame.image.load("sleep.jpg").convert()
crying = pygame.image.load("crying.jpg").convert()
happy = pygame.image.load("happy.jpg").convert()
scared = pygame.image.load("scared.jpg").convert()
yawn = pygame.image.load("yawn.jpg").convert()
sick = pygame.image.load("sick.jpg").convert()

hall_past = [70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70]
touch_past = [500 for x in range(100)]

#state global variables
just_home = False
t_start_happy = time.time()
is_angry = False
t_start_angry = time.time()
just_away = False
t_start_sad = time.time()
is_waking = False
just_waking = False
t_start_waking = time.time()
is_sick = False
t_start_sick = time.time()

def main():
    global hall_past
    status = True
    while (status):
        #get input
        data, addr = sock.recvfrom(1024)
        print("received message: %s" %data)
        dataList = data.decode("utf-8").split(" ")
        print("hall avg: " + str(mean(hall_past)))
        print("touch: " + dataList[1])
        # print("x: " + dataList[2])
        # print("y: " + dataList[3])
        # print("z: " + dataList[4])

        hall_past.insert(0, int(dataList[0]))
        hall_past.pop()
        print(hall_past)
        touch_past.insert(0, int(dataList[1]))
        touch_past.pop()
        print("touch avg: " + str(mean(touch_past)))

        current = getCurrent(dataList)
        scrn.fill((110, 63, 107))

        scrn.blit(current, ((X-current.get_width())//2, (Y-current.get_height())//2))

        # text = font.render(dataList[1], True, (0, 0, 0), (0, 255, 0))
        # textRect = text.get_rect()
        # textRect.center = (X -100, Y - 100)
        # scrn.blit(text, textRect)

        pygame.display.flip()

        
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
        for i in pygame.event.get():
    
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if i.type == pygame.QUIT:
                status = False
    
    # deactivates the pygame library
    pygame.quit()

def getCurrent(dataList):
    global just_home, t_start_happy, is_angry, t_start_angry, just_away, t_start_sad, is_waking, t_start_waking, just_waking
    global is_sick, t_start_sick, hall_past, touch_past
    if is_sick:
        if (time.time() > t_start_sick + 3):
            is_sick = False
            is_angry = False
            # t_start_angry = time.time() -1
        return sick
    if is_angry:
        if (time.time() > t_start_angry + 1) and (float(dataList[2]) > 2 or float(dataList[3]) > 2 or float(dataList[4]) > 2):
                is_sick = True
                t_start_sick = time.time()
                return sick
        if (time.time() > t_start_angry + 3):
            is_angry = False
            t_start_sad = time.time()
        return angry
    elif float(dataList[2]) > 2 or float(dataList[3]) > 2 or float(dataList[4]) > 2:
        is_angry = True
        just_home = True
        t_start_angry = time.time()
        return angry  
    elif is_waking:
        if just_waking:
            t_start_waking = time.time()
            just_waking = False
        # if time.time() > t_start_waking + 0.5:
        #     return yawn
        if time.time() > t_start_waking + 0.5 and int(dataList[1]) > 1.4*mean(touch_past):
            is_waking = False
            just_home = True
            return happy
        if time.time() > t_start_waking + 2:
            is_waking = False
            just_home = False
        return yawn
    elif just_away == False and time.time() < t_start_sad + 1:
        return scared
    elif float(mean(hall_past)) < 85: #on magnets / home
        just_away = True
        if (just_home):
            t_start_happy = time.time()
            just_home = False 
        if (time.time() > t_start_happy + 5):
            if int(dataList[1]) >  1.4*mean(touch_past):
                just_waking = True
                is_waking = True
            return sleeping
        if (time.time() > t_start_happy + 3):
            return yawn
        return happy
    elif just_home == False and time.time() < t_start_happy + 1:
        return happy
    else:   #still and away from home
        just_home = True
        if (just_away):
            t_start_sad = time.time()
            just_away = False
        if time.time() > t_start_sad + 5:
            if int(dataList[1]) >  1.4*mean(touch_past):
                t_start_sad = time.time()
                return scared
            return crying
        return scared



if __name__ == '__main__':
    main()
