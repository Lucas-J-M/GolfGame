##################IMPORTS################
import pygame
import numpy as np
import math
##################TUPLES################
background_colour = (44, 184, 9)
(width, height) = (700, 700)
screen = pygame.display.set_mode((width, height))
##################COLORS################
golfballcolor = pygame.Color(255,255,255)
polecolor = pygame.Color(86, 94, 94)
holecolor = pygame.Color(102, 101, 101)
flagcolor = pygame.Color(171, 12, 15)
linecolor = pygame.Color(255, 255, 255, 100)
wallcolor = pygame.Color(82, 55, 21)
##################BOOLS################
running = True
dragging = False
moveball = False
roundstart = False
##################LISTS################
leftlist = []
toplist = []
wallwidthlist = []
wallheightlist = []
##################INTS################
deceleration = .999
# Setting the position of the ball and flag init
ballstartposx, ballstartposy = np.random.randint(100, width - 100), np.random.randint(100, height -100)
randomflagposx, randomflagposy = np.random.randint(50, width - 50), np.random.randint(50, height - 50)

pygame.display.set_caption('Mini Golf') #Setting window caption
pygame.display.flip()
while running:
    # Updating game
    screen.fill(background_colour)
    mousepos = pygame.mouse.get_pos()
    ##################################
    #Creating randomized walls
    if not roundstart:
        leftlist = []
        toplist = []
        wallwidthlist = []
        wallheightlist = []
        for i in range(np.random.randint(0, 10)):
            left = np.random.randint(0, width)
            top = np.random.randint(0, width)
            randomwallwidth = np.random.randint(width/20, width/2)
            randomwallheight = np.random.randint(height/20, height/2)
            leftlist.append(left)
            toplist.append(top)
            wallwidthlist.append(randomwallwidth)
            wallheightlist.append(randomwallheight)
    #Appending wall properties to seperate lists
    ##################################
    ##################################
    #Placing walls down
    for i in range(len(leftlist)):
        Rectangle = pygame.Rect(leftlist[i], toplist[i], wallwidthlist[i], wallheightlist[i])
        pygame.draw.rect(screen, wallcolor, Rectangle)
    if not roundstart:
        while screen.get_at((ballstartposx, ballstartposy)) == wallcolor or screen.get_at((ballstartposx + 20, ballstartposy)) == wallcolor or screen.get_at((ballstartposx - 20, ballstartposy)) == wallcolor or screen.get_at((ballstartposx, ballstartposy + 20)) == wallcolor or screen.get_at((ballstartposx, ballstartposy - 20)) == wallcolor:
            ballstartposx, ballstartposy = np.random.randint(100, width - 100), np.random.randint(100, height -100)
        while screen.get_at((randomflagposx, randomflagposy)) == wallcolor or screen.get_at((randomflagposx + 20, randomflagposy)) == wallcolor or screen.get_at((randomflagposx - 20, randomflagposy)) == wallcolor or screen.get_at((randomflagposx, randomflagposy + 20)) == wallcolor or screen.get_at((randomflagposx, randomflagposy -20)) == wallcolor:
            randomflagposx, randomflagposy = np.random.randint(50, width - 50), np.random.randint(50, height - 50)
    #While loops ensure that the ball and hole are not on a wall
    ##################################
    ##################################
    #Making hole
    pygame.draw.circle(screen, golfballcolor, (ballstartposx, ballstartposy), 10.0, 10)
    pygame.draw.circle(screen,holecolor, (randomflagposx, randomflagposy), 20.0, 20)
    pygame.draw.line(screen, polecolor, (randomflagposx, randomflagposy), (randomflagposx, randomflagposy - width/20), 5)
    pygame.draw.polygon(screen, flagcolor, ((randomflagposx, randomflagposy - width/40), (randomflagposx, randomflagposy - width/20), (randomflagposx + width/40, randomflagposy + width/30)), 10)
    ##################################
    roundstart = True #Stops randomizing position of walls, hole, and ball
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP: #Detecting if player released their mouse left click (launch the golfball)
            if dragging:
                dragging = False
                moveball = True
        if event.type == pygame.MOUSEBUTTONDOWN and screen.get_at(mousepos) == golfballcolor and not moveball: #Detecting when the player wants to launch the ball but they need to start the drag at the balls current position
            dragging = True
    if dragging: #Creates a line depending on where the player is dragging to
        pygame.draw.line(screen, linecolor, (ballstartposx, ballstartposy), mousepos, 10)
        dx = mousepos[0] - ballstartposx #Finds horizontal component of force
        dy = mousepos[1] - ballstartposy #Finds vertical component of force
    if moveball:
        dx*=deceleration #Slows down the ball by how much it moves each frame
        dy*=deceleration
        ballstartposx = (ballstartposx - (dx/200)) #moves the ball with force dx/200 as dx gets closer to 0 as time moves on
        ballstartposy = (ballstartposy - (dy/200)) #Same thing but with y force
        ##################################
        #Wall and sides collision detection and directional reversal
        if ballstartposx <= 10 or ballstartposx >= width - 10: #If the ball hits the sides
            dx = -dx #Reverse direction
        if ballstartposy <= 10 or ballstartposy >= height - 10: #If ball hits the top or bottom
            dy = -dy #Reverse direction
        #In try/except block because if pixel is out of range with screen.get_at then it returns an error (only happens when ball is close to sides of window)
        try:
            if screen.get_at([math.floor(ballstartposx)+ 10, math.floor(ballstartposy)]) == wallcolor: #The following 4 if statements check for wall collisions and then reverse the direction of the ball
                dx = -dx
            if screen.get_at([math.floor(ballstartposx) - 10, math.floor(ballstartposy)]) == wallcolor:
                dx = -dx
            if screen.get_at([math.floor(ballstartposx), math.floor(ballstartposy) + 10]) == wallcolor:
                dy = -dy
            if screen.get_at([math.floor(ballstartposx), math.floor(ballstartposy) - 10]) == wallcolor:
                dy = -dy
        except Exception as e:
            pass
        ##################################
        #After a certain slow speed (like 2 pixels) the ball stops moving
        pygame.draw.circle(screen, golfballcolor, (ballstartposx, ballstartposy), 10.0, 10)
        if np.abs(dx) < 2 and np.abs(dy) < 2:
            moveball = False
        ##################################
    ##################################
    #The following if statements check if the ball is in the hole
    if (ballstartposx >= randomflagposx - 20 and ballstartposx <= randomflagposx + 20):
        if (ballstartposy >= randomflagposy - 20 and ballstartposy <= randomflagposy + 20):
            moveball = False
            ballstartposx, ballstartposy = np.random.randint(100, width - 100), np.random.randint(100, height -100) #Re-init ball pos
            randomflagposx, randomflagposy = np.random.randint(50, width - 50), np.random.randint(50, height - 50) #Re-init hole pos
            roundstart = False
       
    pygame.display.update() #Updates the display every loop iteration
