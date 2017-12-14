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

FPS = 0

alive = True

framerate = 90                 # frames per second
refresh_rate = 1/framerate     # refresh every 1/framerate of seconds

gravity = -9.81*50

acc = gravity
speed = [0, 0]
enableFloor = True          # is there a floor on the down side of the frame
enablePhysic = True        # Enable or disable gravity effect

rightKeyDown = False
leftKeyDown = False
spaceKeyDown = False

rocket_width = 50
rocket_height = 25
rocket_pos = [[win_width//2, win_height], math.pi/2]
rocketVector = [[win_width//2, win_height], [0, 1]]


def renderPhysics(actualRocketPos, deltaT):
    newPhysicCoords = actualRocketPos
    global speed
    global acc
    global rocketVector
    if rocketVector[0][1] < win_height or speed!=0:
        acc = gravity
        dvy = acc*deltaT
        speed[1] += dvy
        dx = speed[0]*deltaT
        dy = speed[1]*deltaT
        angle = getVectorAngle(rocketVector[1])
        newPhysicCoords[0] = newPhysicCoords[0]+speed[0]*deltaT
        newPhysicCoords[1] = newPhysicCoords[1]-speed[1]*deltaT
    if rocketVector[0][1] >= win_height and enableFloor:
        acc=0
        speed=[0, 0]
        setRocketSpeed([0, 600])
        newPhysicCoords[1] = win_height
    return newPhysicCoords

def setRocketSpeed(newSpeed):
    global speed
    speed[0] = newSpeed[0]
    speed[1] = newSpeed[1]

def getRocketSpeed():
    global speed
    return (speed[0], speed[1])

def setRocketAcceleration(newAcceleration):
    global acc
    acc = newAcceleration

def moveRocket(newRocketPos):
    global rocketVector
    rocketVector[0] = newRocketPos
    rocketVector[1] = getRocketVector()[1]
    

def drawRocket():
    global rocketVector
    rocketAngle = getVectorAngle(rocketVector[1])
    point_1 = [int(rocketVector[0][0]+math.sin(rocketAngle)*rocket_height/2), int(rocketVector[0][1]+math.cos(rocketAngle)*rocket_height/2)]
    point_2 = [int(point_1[0]+math.cos(rocketAngle)*rocket_width), int(point_1[1]-math.sin(rocketAngle)*rocket_width)]
    point_3 = [int(point_2[0]-math.sin(rocketAngle)*rocket_height), int(point_2[1]-math.cos(rocketAngle)*rocket_height)]
    point_4 = [int(point_3[0]-math.cos(rocketAngle)*rocket_width), int(point_3[1]+math.sin(rocketAngle)*rocket_width)]
    
    rocket = pygame.draw.polygon(win, GREY, [point_1, point_2, point_3, point_4])
    #rocket = pygame.draw.line(win, GREY, point_1, point_2)
    #rocket =pygame.draw.line(win, GREY, point_2, point_3)
    #pygame.draw.line(win, GREY, point_3, point_4)
    #pygame.draw.line(win, GREY, point_4, point_1)
    return rocket

def getRocketVector():
    global rocketVector
    angle = getVectorAngle(rocketVector[1])
    point_1 = [rocketVector[0][0], rocketVector[0][1]]
    point_2 = [point_1[0]+math.cos(angle)*rocket_width*2, point_1[1]+math.sin(angle)*rocket_width*2]

    vector = [point_2[0]-point_1[0], point_2[1]-point_1[1]]

    return [point_1, vector]

def drawVector(origin, vector):
    pygame.draw.line(win, (255, 0, 0), origin, [rocketVector[0][0]+rocketVector[1][0], rocketVector[0][1]-rocketVector[1][1]])

def getVectorAngle(vector):
    norme = math.sqrt(vector[0]**2+vector[1]**2)
    cosAngle = vector[0]/norme
    sinAngle = vector[1]/norme

    angle=math.acos(cosAngle) if math.asin(sinAngle)>=0 else 2*math.pi - math.acos(cosAngle)
        
    return angle

def setVectorAngle(vector, angle):
    norme = math.sqrt(vector[0]**2+vector[1]**2)
    xPos = int(norme*math.cos(angle))
    yPos = int(norme*math.sin(angle))
    
    return [xPos, yPos]
    
def eventHandler():
    global rocketVector
    global rightKeyDown
    global leftKeyDown
    global spaceKeyDown
    rightKeyDown = pygame.key.get_pressed()[K_RIGHT]
    leftKeyDown = pygame.key.get_pressed()[K_LEFT]
    spaceKeyDown = pygame.key.get_pressed()[K_SPACE]
    angle = getVectorAngle(rocketVector[1])
    if leftKeyDown:
        angle = getVectorAngle(rocketVector[1])
        rocketVector[1] = setVectorAngle(rocketVector[1], angle+math.pi/200)
    elif rightKeyDown:
        angle = getVectorAngle(rocketVector[1])
        rocketVector[1] = setVectorAngle(rocketVector[1], angle-math.pi/200)
    if spaceKeyDown:
        setRocketSpeed([350*math.cos(angle), 350*math.sin(angle)])
    return False

def updateDisplay(deltaT):  
    global rocketVector
    global FPS
    win.fill(WHITE)
    if enablePhysic:
        newCoords = renderPhysics(rocketVector[0], deltaT)
    else:
        newCoords = rocketVector[0]
    rocketVector[0] = newCoords
    moveRocket(newCoords)
    #angle = getVectorAngle(rocketVector[1])
    #rocketVector[1] = setVectorAngle(rocketVector[1], angle)
    rocketVector = getRocketVector()
    drawVector(rocketVector[0], rocketVector[1])
    drawRocket()

    FPSCounterText = pygame.font.SysFont('arial', 25)
    FPSCounter = FPSCounterText.render("FPS: "+str(FPS), 1, (255, 0, 0))
    win.blit(FPSCounter, (10, 0))
    
    pygame.display.update()

def controlInterface():
    #TODO: Implement control interface using TKinter
    return False

#############################################    
## ------------- MAIN LOOP --------------- ##
#############################################

moveRocket([rocketVector[0][0], rocketVector[0][1]-300])
rocketVector[1] = setVectorAngle(rocketVector[1], 0)
rocket = drawRocket()
frames = 0
refresh_timer = 0
loop_interval = 0.001
lastRefresh = time.time()
#setRocketSpeed(350)               #Allow user to test speed control and effects

while alive:
    eventHandler()
    if time.time() - lastRefresh >= 1:
        FPS = frames
        frames = 0
        lastRefresh = time.time()
    if refresh_timer >= refresh_rate:
        updateDisplay(refresh_timer)
        refresh_timer = 0
        frames+=1
        #break   #TEMPORAIRE, fige la boucle de rafraichissement
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            alive = False
            break
    refresh_timer += loop_interval
    time.sleep(loop_interval)
