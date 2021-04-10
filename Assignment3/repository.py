# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository():
    def __init__(self, x = 2, y = 3):
         
        self.__populations = []
        self.cmap = Map()
        self.__x = x
        self.__y = y
        
    def createRandomPopulation(self, chromozome_size, population_size):
        p = Population(chromozome_size, self.__x, self.__y, self.cmap)
        p.random_individuals(population_size)
        return p

    def createPopulation(self, individuals):
        p = Population(len(individuals[0].get_chromosome()),self.__x, self.__y,self.cmap)
        p.set_individuals(individuals)
        return p

    def addPopulation(self, population):
        self.__populations.append(population)

    def pop(self):
        return self.__populations[-1]

    def saveMap(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.cmap, f)
            f.close()

    def loadMap(self, file):
        with open(file, "rb") as f:
            dummy  = None
            try:
                dummy = pickle.load(f)
            except Exception as e:
                print(str(e))
                print('a')
            self.cmap.n = dummy.n
            self.cmap.m = dummy.m
            self.cmap.surface = dummy.surface
            f.close()

    def randomMap(self, fill = 0.2, n = 20, m = 20):
        self.cmap.randomMap(fill=fill, n=n,m=m)

    def getStartingPosition(self):
        return self.__x, self.__y

    def getBestIndividual(self):
        return self.pop().bestIndividual
