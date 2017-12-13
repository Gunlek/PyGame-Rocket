import pygame
from pygame.locals import *
import time
import math

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
enablePhysic = False         # Enable or disable gravity effect

rocket_width = 50
rocket_height = 25
rocket_pos = [[win_width//2, win_height], math.pi/2]


def renderPhysics(actualRocketPos, deltaT):
    newPhysicCoords = actualRocketPos[0]
    global speed
    global acc
    if actualRocketPos[0][1] < win_height-rocket_height or speed!=0:
        acc = gravity
        dv = acc*deltaT
        speed += dv
        dy = speed*deltaT
        newPhysicCoords[1] = newPhysicCoords[1]-speed*deltaT
    if actualRocketPos[0][1] >= win_height and enableFloor:
        acc=0
        speed=0
        newPhysicCoords[1] = win_height
    return newPhysicCoords

def setRocketSpeed(newSpeed):
    global speed
    speed = newSpeed

def setRocketAcceleration(newAcceleration):
    global acc
    acc = newAcceleration

def moveRocket(newRocketPos):
    global rocket_pos
    rocket_pos = newRocketPos

def drawRocket():
    point_1 = [int(rocket_pos[0][0]+math.sin(rocket_pos[1])*rocket_height/2), int(rocket_pos[0][1]+math.cos(rocket_pos[1])*rocket_height/2)]
    point_2 = [int(point_1[0]+math.cos(rocket_pos[1])*rocket_width), int(point_1[1]-math.sin(rocket_pos[1])*rocket_width)]
    point_3 = [int(point_2[0]-math.sin(rocket_pos[1])*rocket_height), int(point_2[1]-math.cos(rocket_pos[1])*rocket_height)]
    point_4 = [int(point_3[0]-math.cos(rocket_pos[1])*rocket_width), int(point_3[1]+math.sin(rocket_pos[1])*rocket_width)]
    
    #rocket = pygame.draw.rect(win, GREY, (rocket_coords[0], rocket_coords[1], rocket_width, rocket_height))
    rocket = pygame.draw.polygon(win, GREY, [point_1, point_2, point_3, point_4])
    #rocket = pygame.draw.line(win, GREY, point_1, point_2)
    #pygame.draw.line(win, GREY, point_2, point_3)
    #pygame.draw.line(win, GREY, point_3, point_4)
    #pygame.draw.line(win, GREY, point_4, point_1)
    return rocket

def updateDisplay(deltaT):
    win.fill(WHITE)
    if enablePhysic:
        newCoords = renderPhysics(rocket_pos, deltaT)
    else:
        newCoords = rocket_pos[0]
    moveRocket([newCoords, rocket_pos[1]+math.pi/60])
    drawRocket()
    pygame.display.update()

#############################################    
## ------------- MAIN LOOP --------------- ##
#############################################

moveRocket([[rocket_pos[0][0], rocket_pos[0][1]-300], math.pi/2])
rocket = drawRocket()
cycle_timer = 0
frames = 0
refresh_timer = 0
loop_interval = 0.001
#setRocketSpeed(350)               #Allow user to test speed control and effects

while alive:
    if refresh_timer >= refresh_rate:
        updateDisplay(refresh_timer)
        refresh_timer = 0
        frames+=1
        #break   #TEMPORAIRE, fige la boucle de rafraichissement
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
