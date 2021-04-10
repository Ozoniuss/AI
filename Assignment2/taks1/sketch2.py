

# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np
import math
from PriorityQueue import PriorityQueue


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW= (255, 255, 0)
BROWN = (165, 42, 42)


#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        destination = pygame.Surface((20, 20))
        roadGreedy = pygame.Surface((20, 20))
        roadAStar = pygame.Surface((20, 20))
        common_road = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        destination.fill(RED)
        roadGreedy.fill(GREEN)
        roadAStar.fill(YELLOW)
        common_road.fill(BROWN)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                if (self.surface[i][j] == 2):
                    imagine.blit(destination, (j * 20, i *20))
                if (self.surface[i][j] == 3):
                    imagine.blit(roadGreedy, (j * 20, i * 20))
                if (self.surface[i][j] == 4):
                    imagine.blit(roadAStar, (j * 20, i *20))
                if (self.surface[i][j] == 5):
                    imagine.blit(common_road, (j * 20, i * 20))

        return imagine


    def get_neighbours(self, xi, yi):
        possibilities = [(xi+1, yi), (xi-1, yi), (xi, yi+1), (xi, yi-1)]

        # squares have coordinates between 0 and 19
        first_cut = list(filter(lambda t: (0 <= t[0] <= 19 and 0 <= t[1] <= 19), possibilities))

        return list(filter(lambda t: (self.surface[t[0]][t[1]] == 0 or self.surface[t[0]][t[1]] >= 2) , first_cut))


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.roadGreedy = {}
        self.roadAStar = {}
        self.actualCosts = {}

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                 self.y = self.y + 1

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))

        return mapImage


def searchAStar(mapM, droneD, initialX, initialY, finalX, finalY, h):
    visited = set()
    toVisit = PriorityQueue()
    toVisit.add((initialX, initialY), h(initialX, initialY, finalX, finalY)) # add the initial position to the priority queue
    droneD.roadAStar[(initialX, initialY)] = None
    droneD.actualCosts[(initialX, initialY)] = 0
    found = False

    while((not toVisit.isEmpty()) and (not found)):

        # no route had been found
        if toVisit.isEmpty():
            return False

        #add the next spot to the visited
        node = toVisit.pop()[0]
        visited.add(node)
        # node is equal to the destination
        if node == (finalX, finalY):
            found = True

        # add the neighbours with respective priorities
        neighbours = mapM.get_neighbours(node[0], node[1])

        # we'll replace the nodes already in the quese if we can find a better evaluation
        for n in neighbours:
            if n not in visited:

                # if the neighbour hasn't been reached previously
                if droneD.actualCosts.get((n[0], n[1])) is None:
                    droneD.actualCosts[(n[0], n[1])] = 1 + droneD.actualCosts[(node[0], node[1])]
                    estimated_to_finish = droneD.actualCosts[(n[0], n[1])] + h(n[0], n[1], finalX, finalY)
                    toVisit.add(n, estimated_to_finish)
                    droneD.roadAStar[(n[0], n[1])] = (node[0], node[1])


                else:
                    #only if we found a shorter path to the neighbour
                    distance_to_neighbour = 1 + droneD.actualCosts[(node[0], node[1])]
                    if distance_to_neighbour < droneD.actualCosts[(n[0], n[1])]:
                        droneD.actualCosts[(n[0], n[1])] = distance_to_neighbour
                        estimated_to_finish = droneD.actualCosts[(n[0], n[1])] + h(n[0], n[1], finalX, finalY)
                        toVisit.update(n, estimated_to_finish)
                        droneD.roadAStar[(n[0], n[1])] = (node[0], node[1])

    # if a route was found, contruct it using the road from the drone
    if found == True:
        route = []
        route.append((finalX, finalY))
        while(droneD.roadAStar[route[-1]] != None):
            route.append(droneD.roadAStar[route[-1]])

        print("end")

        return list(reversed(route))

    return []


# h represents the heuristic
def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY, h):

    visited = set()
    toVisit = PriorityQueue()
    toVisit.add((initialX, initialY), h(initialX, initialY, finalX, finalY)) # add the initial position to the priority queue
    droneD.roadGreedy[(initialX, initialY)] = None
    found = False

    while((not toVisit.isEmpty()) and (not found)):

        # no route had been found
        if toVisit.isEmpty():
            return False

        #add the next spot to the visited
        node = toVisit.pop()[0]
        visited.add(node)
        # node is equal to the destination
        if node == (finalX, finalY):
            found = True

        # add the neighbours with respective priorities
        neighbours = mapM.get_neighbours(node[0], node[1])


        for n in neighbours:
            if (not toVisit.contains(n)) and (n not in visited):
                toVisit.add(n, h(n[0], n[1], finalX, finalY))
                droneD.roadGreedy[(n[0], n[1])] = (node[0], node[1])

    # if a route was found, contruct it using the road from the drone
    if found == True:
        route = []
        route.append((finalX, finalY))
        while(droneD.roadGreedy[route[-1]] != None):
            route.append(droneD.roadGreedy[route[-1]])

        print("end")

        return list(reversed(route))

def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [(5,7),(5,8),(5,9),(5,10),(5,11),(6,11),(7,11)]

def displayWithPath(image, path):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))

    return image


def manhattanHeuristic(xi, yi, xf, yf):
    return abs(xi - xf) + abs(yi - yf)

def euclideanHueristic(xi, yi, xf, yf):
    return int(math.sqrt((xi-xf)**2 + (yi-yf)**2))


# define a main function
def main():

    # we create the map
    m = Map()
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")


    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    #create drona
    d = Drone(x, y)

    #create destination
    m.surface[2][4] = 2



    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)


    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    print('A*')
                    finished = searchAStar(m, d, d.x, d.y, 2, 4, manhattanHeuristic)
                    if finished != False:
                        for pos in finished:
                            if m.surface[pos[0]][pos[1]] == 3 or m.surface[pos[0]][pos[1]] == 5:
                                m.surface[pos[0]][pos[1]] = 5
                            else:
                                m.surface[pos[0]][pos[1]] = 4


                if event.key == pygame.K_DOWN:
                    print('GREEDY')
                    finished3 = searchGreedy(m, d, d.x, d.y, 2, 4, manhattanHeuristic)
                    print(finished3)
                    if finished3 != False:
                        for pos in finished3:
                            if m.surface[pos[0]][pos[1]] == 4 or m.surface[pos[0]][pos[1]] == 5:
                                m.surface[pos[0]][pos[1]] = 5
                            else:
                                m.surface[pos[0]][pos[1]] = 3





        screen.blit(d.mapWithDrone(m.image()),(0,0))
        pygame.display.flip()

    #path = dummysearch()
    #screen.blit(displayWithPath(m.image(), path),(0,0))

    pygame.display.flip()
    time.sleep(1)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()