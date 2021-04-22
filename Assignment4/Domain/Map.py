import pickle
from random import random
from utilities import *
import numpy as np
import pygame
from PriorityQueue import PriorityQueue
import math
from typing import *


def manhattanHeuristic(xi, yi, xf, yf):
    return abs(xi - xf) + abs(yi - yf)


def euclideanHueristic(xi, yi, xf, yf):
    return int(math.sqrt((xi - xf) ** 2 + (yi - yf) ** 2))


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

        self.roadAStar = {}
        self.actualCosts = {}

        self.surveilled_area = 0

    def randomMap(self, fill=0.2):
        self.surface = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def get_size(self):
        return self.n, self.m

    def place_senzors(self, list_of_positions: List[Tuple[int, int]]):
        for senzor in list_of_positions:
            self.surface[senzor[0]][senzor[1]] = 2

    def give_senzor_energy(self, position: Tuple[int, int], energy) -> int:

        original_surveillance = self.surveilled_area
        # returns how much has added to the surveilled area


        x, y = position[0], position[1]
        if self.surface[x][y] != 2:
            raise Exception('There is no fucking senzor there.')

        # UP
        xf = x - 1
        step = 1
        while (xf >= 0) and (self.surface[xf][y] in [0, 3]) and step <= energy:
            self.surface[xf][y] = 3
            xf = xf - 1
            step += 1

        # DOWN
        xf = x + 1
        step = 1
        while (xf < self.n) and (self.surface[xf][y] in [0, 3]) and step <= energy:
            self.surface[xf][y] = 3
            xf = xf + 1
            step += 1


        # LEFT
        yf = y + 1
        step = 1
        while (yf < self.m) and (self.surface[x][yf] in [0, 3]) and step <= energy:
            self.surface[x][yf] = 3
            yf = yf + 1
            step += 1


        # RIGHT
        yf = y - 1
        step = 1
        while (yf >= 0) and (self.surface[x][yf] in [0, 3]) and step <= energy:
            self.surface[x][yf] = 3
            yf = yf - 1
            step += 1

        # Find out how much has changed
        surveilled = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 2:
                    surveilled += 1
        added = surveilled - self.surveilled_area
        self.surveilled_area = surveilled
        return added


    @property
    def number_of_senzors(self):
        n = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 2:
                    n += 1
        return n





    def get_neighbours(self, xi, yi):
        # returns the list of neighbours of the square xi, yi
        possibilities = [(xi+1, yi), (xi-1, yi), (xi, yi+1), (xi, yi-1)]

        # squares have coordinates between 0 and 19
        first_cut = list(filter(lambda t: (0 <= t[0] <= 19 and 0 <= t[1] <= 19), possibilities))

        return list(filter(lambda t: (self.surface[t[0]][t[1]] == 0 or self.surface[t[0]][t[1]] >= 2) , first_cut))


    def searchAStar(self, initialX, initialY, finalX, finalY, h = manhattanHeuristic):

        self.roadAStar = {}
        self.actualCosts = {}

        visited = set()
        toVisit = PriorityQueue()
        toVisit.add((initialX, initialY), h(initialX, initialY, finalX, finalY)) # add the initial position to the priority queue
        self.roadAStar[(initialX, initialY)] = None
        self.actualCosts[(initialX, initialY)] = 0
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
            neighbours = self.get_neighbours(node[0], node[1])

            # we'll replace the nodes already in the quese if we can find a better evaluation
            for n in neighbours:
                if n not in visited:

                    # if the neighbour hasn't been reached previously
                    if self.actualCosts.get((n[0], n[1])) is None:
                        self.actualCosts[(n[0], n[1])] = 1 + self.actualCosts[(node[0], node[1])]
                        estimated_to_finish = self.actualCosts[(n[0], n[1])] + h(n[0], n[1], finalX, finalY)
                        toVisit.add(n, estimated_to_finish)
                        self.roadAStar[(n[0], n[1])] = (node[0], node[1])


                    else:
                        #only if we found a shorter path to the neighbour
                        distance_to_neighbour = 1 + self.actualCosts[(node[0], node[1])]
                        if distance_to_neighbour < self.actualCosts[(n[0], n[1])]:
                            self.actualCosts[(n[0], n[1])] = distance_to_neighbour
                            estimated_to_finish = self.actualCosts[(n[0], n[1])] + h(n[0], n[1], finalX, finalY)
                            toVisit.update(n, estimated_to_finish)
                            self.roadAStar[(n[0], n[1])] = (node[0], node[1])

        # if a route was found, contruct it using the road from the drone
        if found == True:
            route = []
            route.append((finalX, finalY))
            while(self.roadAStar[route[-1]] != None):
                route.append(self.roadAStar[route[-1]])
            return list(reversed(route))

        return []


