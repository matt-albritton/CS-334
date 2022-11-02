# importing required library
import pygame
import time
 
# activate the pygame library .
pygame.init()
X = 800
Y = 480
 
# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))
scrn.fill((110, 63, 107))
 
# set the pygame window name
pygame.display.set_caption('image')
 
# create a surface object, image is drawn on it.
angry = pygame.image.load("angry.jpg").convert()
sleeping = pygame.image.load("sleep.jpg").convert()
 
# Using blit to copy content from one surface to other
scrn.blit(angry, ((X-angry.get_width())//2, (Y-angry.get_height())//2))
 
# paint screen one time
pygame.display.flip()
status = True
while (status):
    current = angry
    scrn.blit(current, ((X-current.get_width())//2, (Y-current.get_height())//2))
    pygame.display.flip()

    time.sleep(1);
    current = sleeping
    scrn.blit(current, ((X-current.get_width())//2, (Y-current.get_height())//2))
    pygame.display.update()

    
    time.sleep(1)
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