from Domain.Drone import Ant
from Domain.Map import *
from typing import *
import copy
class Service:
    def __init__(self, map : Map, starting_position:Tuple[int, int]):
        self.__map = map
        self.__paths_matrix = {}

        # keys are senzor lables, values are positions
        self.__senzors_positions = {}

        # keys are tuples (2 senzors), values the paths between them
        self.__distances_between_senzors = {}

        # pheromone between senzors is also going to be shared
        self.__pheromone_between_senzors = {}

        # keys are senzors, paths are energies
        self.__max_senzor_energy = {}

        self.__starting_position = starting_position

    @property
    def number_of_senzors(self):
        return len(self.__senzors_positions)

    @property
    def starting_position(self):
        return self.__starting_position

    def getMap(self):
        return self.__map

    def saveMap(self, file):
        self.__map.saveMap(file)

    def loadMap(self, file):
        self.__map.loadMap(file)

    def get_distances_between_senzors(self):
        return self.__distances_between_senzors

    def find_senzors_positions(self):
        # this finds all the senzors on a given map

        # clear all the senzors before starting
        self.__senzors_positions = {}

        current_senzor = 1
        for i in range(self.__map.n):
            for j in range(self.__map.m):
                if self.__map.surface[i][j] == 2:
                    self.__senzors_positions[current_senzor] = (i,j)
                    current_senzor += 1

    def find_distances_between_all_senzors(self):

        #INCLUDES DISTANCES FROM STARTING POINT (0) TO ALL THE SENZORS

        # clear old distances
        self.__distances_between_senzors = {}

        for i in range(1, self.number_of_senzors):
            for j in range(i+1, self.number_of_senzors + 1):
                ix = self.__senzors_positions[i][0]
                iy = self.__senzors_positions[i][1]
                fx = self.__senzors_positions[j][0]
                fy = self.__senzors_positions[j][1]
                path = self.__map.searchAStar(ix, iy, fx, fy)
                self.__distances_between_senzors[(i,j)] = len(path)
                self.__distances_between_senzors[(j,i)] = len(path)

            # from the drone now
            ix = self.__starting_position[0]
            iy = self.__starting_position[1]
            fx = self.__senzors_positions[i][0]
            fy = self.__senzors_positions[i][1]
            path = self.__map.searchAStar(ix, iy, fx, fy)
            self.__distances_between_senzors[(0, i)] = len(path)
            self.__distances_between_senzors[(i, 0)] = len(path)

        # and to the last senzor
        ix = self.__starting_position[0]
        iy = self.__starting_position[1]
        fx = self.__senzors_positions[self.number_of_senzors][0]
        fy = self.__senzors_positions[self.number_of_senzors][1]
        path = self.__map.searchAStar(ix, iy, fx, fy)
        self.__distances_between_senzors[(0, self.number_of_senzors)] = len(path)
        self.__distances_between_senzors[(self.number_of_senzors, 0)] = len(path)


    def initialize_pheromone_between_senzors(self):
        self.__pheromone_between_senzors = {} # clear it up before

        # also consider the starting point
        #print(self.__distances_between_senzors)
        for i in range(0, self.number_of_senzors):
            for j in range(i+1, self.number_of_senzors + 1):
                self.__pheromone_between_senzors[(i, j)] = 1 / self.__distances_between_senzors[(i,j)]
                self.__pheromone_between_senzors[(j, i)] = 1 / self.__distances_between_senzors[(j,i)]



    def find_max_senzor_energy(self, senzor):
        x, y = self.__senzors_positions[senzor][0], self.__senzors_positions[senzor][1]
        readings=[0,0,0,0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.__map.surface[xf][y] in [0,3])):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__map.n) and (self.__map.surface[xf][y] in [0,3])):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__map.m) and (self.__map.surface[x][yf] in [0,3])):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__map.surface[x][yf] in [0,3])):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1
        return max(readings)

    def initialize_all_parameters(self):
        self.find_senzors_positions()
        self.find_distances_between_all_senzors()
        self.initialize_pheromone_between_senzors()
        print('positions, ' + str(self.__senzors_positions))
        print('distances, ' + str(self.__distances_between_senzors))
        print('pheromones, ' + str(self.__pheromone_between_senzors))


    def generation(self, q0, alpha, beta, rho, energy):

        antSet = []
        for _ in range(self.number_of_senzors):
            antSet.append(Ant(self.getMap(),
                              self.__starting_position,
                              energy))

        for _ in range(self.number_of_senzors + 1):

            for ant in antSet:
                if ant.energy <= 0:
                    continue
                ant.addMove(q0, alpha, beta, self.__distances_between_senzors,
                            self.__pheromone_between_senzors)

                # derease the energy with the length of the path

                ant.energy -= self.__distances_between_senzors[(ant.path[-2],ant.path[-1])] - 1
                ant.total_surveillance += 1 # count senzor as surveilled

                if ant.energy <= 0:
                    ant.total_surveillance -= 1
                    continue

                # FIND HOW MUCH THE SENZORS HAVE SURVEILLED
                current_senzor = ant.path[-1]
                max_energy = self.find_max_senzor_energy(current_senzor)

                # give energy untill it runs out with energy
                out_of_energy = False
                for i in range(1, max_energy + 1):
                    if ant.energy <= 0:
                        out_of_energy = True
                        break
                    surveilled = self.__map.give_senzor_energy(self.__senzors_positions[current_senzor], 1)
                    ant.energy -= 1
                    ant.total_surveillance += surveilled

                # skip if
                if out_of_energy == True:
                    continue


        fitnesses = [[antSet[i].fitness(self.__distances_between_senzors), i] for i in range(len(antSet))]
        fitnesses = min(fitnesses)

        # degradare la terminarea drumului
        minim = 1
        for i in range(self.number_of_senzors):
            for j in range(i+1, self.number_of_senzors + 1):
                self.__pheromone_between_senzors[(i,j)] *= (1 - rho)
                if self.__pheromone_between_senzors[(i,j)] < minim and self.__pheromone_between_senzors[(i,j)] != 0:
                    minim = self.__pheromone_between_senzors[(i,j)]

        # for i in range(self.number_of_senzors):
        #     for j in range(i + 1, self.number_of_senzors + 1):
        #         self.__pheromone_between_senzors[(i,j)] /= minim
        #         self.__pheromone_between_senzors[(j,i)] /= minim

        best_path = antSet[fitnesses[1]].path
        for index in range(len(best_path) - 1):
            self.__pheromone_between_senzors[(best_path[index], best_path[index + 1])] += rho * (
                        1 / self.__distances_between_senzors[(best_path[index], best_path[index + 1])])
            self.__pheromone_between_senzors[(best_path[index + 1], best_path[index])] += rho * (
                    1 / self.__distances_between_senzors[(best_path[index],best_path[index + 1])])

        return best_path, fitnesses[0]

    def run_solver(self, energy = 1000000000, generations = 100,  q0=0.5, alpha=1.9, beta=0.9, rho=0.05):
        sol = []
        best_fitness = float('inf')  # lower is better
        print("running...")
        for i in range(generations):
            print("generation nr:", i)
            sol, fitness = self.generation(q0, alpha, beta, rho, energy)
            if fitness < best_fitness:
                best_sol = copy.deepcopy(sol)
                best_fitness = fitness

        return best_sol




