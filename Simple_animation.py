import pygame
from pygame.locals import *
import time

pygame.init()

win_height = 480
win_width= 640

WHITE = (238, 238, 238)
GREY = (33, 33, 33)

win = pygame.display.set_mode((win_width, win_height), RESIZABLE)
win.fill(WHITE)


alive = True

framerate = 60        # frames per second
refresh_rate = 1/framerate   # refresh every 1/framerate of seconds

gravity = -9.81*40

acc = gravity
speed = 0

rocket_width = 25
rocket_height = 50
rocket_coords = [win_width//2-rocket_width/2, win_height-rocket_height]

def renderPhysics(actualCoords, deltaT):
    newPhysicCoords = actualCoords
    if actualCoords[1] < win_height-rocket_height:
        acc = -gravity
        dv = acc*deltaT
        global speed
        speed += dv
        dy = speed*deltaT
        newPhysicCoords[1] = newPhysicCoords[1]+speed*deltaT
    return newPhysicCoords

def moveRocket(new_coords):
    global rocket_coords
    rocket_coords = new_coords

def drawRocket():
    rocket = pygame.draw.rect(win, GREY, (rocket_coords[0], rocket_coords[1], rocket_width, rocket_height))
    return rocket

def updateDisplay(deltaT):
    win.fill(WHITE)
    newCoords = renderPhysics(rocket_coords, deltaT)
    moveRocket(newCoords)
    drawRocket()
    pygame.display.update()

#############################################    
## ------------- MAIN LOOP --------------- ##
#############################################

rocket = drawRocket()
refresh_timer = 0
loop_interval = 0.001
moveRocket([rocket_coords[0], rocket_coords[0]-90])

while alive:
    if refresh_timer >= refresh_rate:
        #print("REFRESH")
        #print(refresh_timer)
        updateDisplay(refresh_timer)
        refresh_timer = 0
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            alive = False
            break
    #moveRocket([rocket_coords[0], rocket_coords[1]-0.5])
    refresh_timer += loop_interval
    time.sleep(loop_interval)
