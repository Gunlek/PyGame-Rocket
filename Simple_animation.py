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

framerate = 60                 # frames per second
refresh_rate = 1/framerate     # refresh every 1/framerate of seconds

gravity = -9.81*50

acc = gravity
speed = 0
enableFloor = True          # is there a floor on the down side of the frame

rocket_width = 25
rocket_height = 50
rocket_coords = [win_width//2-rocket_width/2, win_height-rocket_height]

def renderPhysics(actualCoords, deltaT):
    newPhysicCoords = actualCoords
    global speed
    global acc
    if actualCoords[1] < win_height-rocket_height or speed!=0:
        acc = gravity
        dv = acc*deltaT
        speed += dv
        dy = speed*deltaT
        newPhysicCoords[1] = newPhysicCoords[1]-speed*deltaT
    if actualCoords[1] >= win_height-rocket_height and enableFloor:
        acc=0
        speed=0
        newPhysicCoords[1] = win_height-rocket_height
    return newPhysicCoords

def setRocketSpeed(newSpeed):
    global speed
    speed = newSpeed

def setRocketAcceleration(newAcceleration):
    global acc
    acc = newAcceleration

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
cycle_timer = 0
frames = 0
refresh_timer = 0
loop_interval = 0.001
#setRocketSpeed(350)               #Allow user to test speed control and effects
moveRocket([rocket_coords[0], rocket_coords[0]-90])

while alive:
    if refresh_timer >= refresh_rate:
        updateDisplay(refresh_timer)
        refresh_timer = 0
        frames+=1
        if cycle_timer >= 1:
            cycle_timer = 0
            frames = 0
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            alive = False
            break
    refresh_timer += loop_interval
    cycle_timer += loop_interval
    time.sleep(loop_interval)
