# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame, time
from utils import *
from domain import *



# class GUI:
#     def __init__(self):
#         pygame.init()
#         self.running, self.algorithm = True, False
#         self.UP_KEY = False
#         self.DOWN_KEY = False
#         self.START_KEY = False
#         self.BACK_KEY = False
#         self.DISPLAY_W, self.DISPLAY_H = 480, 270
#         self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
#         self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
#         self.font_name = pygame.font.get_default_font()
#
#
#     def game_loop(self):
#         while self.algorithm:
#             self.check_events()
#             if self.START_KEY:
#                 self.algorithm = False
#             self.display.fill(BLACK)
#             self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
#             self.window.blit(self.display, (0,0))
#             pygame.display.update()
#             self.reset_keys()
#
#
#     def check_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running, self.algorithm = False, False
#
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     self.START_KEY = True
#                 if event.key == pygame.K_BACKSPACE:
#                     self.BACK_KEY = True
#                 if event.key == pygame.K_DOWN:
#                     self.DOWN_KEY = True
#                 if event.key == pygame.K_UP:
#                     self.UP_KEY = True
#
#     def reset_keys(self):
#         self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
#
#     def draw_text(self, text, size, x, y ):
#         font = pygame.font.Font(self.font_name,size)
#         text_surface = font.render(text, True, WHITE)
#         text_rect = text_surface.get_rect()
#         text_rect.center = (x,y)
#         self.display.blit(text_surface,text_rect)

def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()

def displayMapImage(screen, image, drone_x, drone_y):
    drona = pygame.image.load("drona.png")
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        screen.blit(image, (0,0))
        screen.blit(drona, (drone_y * 20, drone_x * 20))
        pygame.display.flip()
    pygame.quit()

def movingDrone(currentMap, path, speed = 1,  markSeen = True):
    # animation of a drone on a path
    
    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))

    drona = pygame.image.load("drona.png")
        
    for i in range(len(path)):
        screen.blit(image(currentMap), (0,0))
        
        if markSeen:
            brick = pygame.Surface((20,20))
            brick.fill(GREEN)
            for j in range(i+1):
                for var in v:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + var[0] < currentMap.n and  
                            0 <= y + var[1] < currentMap.m) and 
                           currentMap.surface[x + var[0]][y + var[1]] != 1):
                        x = x + var[0]
                        y = y + var[1]
                        screen.blit(brick, ( y * 20, x * 20))
        
        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()
        time.sleep(0.5 * speed)            
    closePyGame()


def image(currentMap, colour = BLUE, background = WHITE):
    # creates the image of a map
    
    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20,20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if (currentMap.surface[i][j] == 1):
                imagine.blit(brick, ( j * 20, i * 20))
                
    return imagine

def mapWithDrone(mapImage, x, y):
    drona = pygame.image.load("drona.png")
    mapImage.blit(drona, (y * 20, x * 20))

    return mapImage
    