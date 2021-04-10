# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np
from heapq import nlargest
import itertools

# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

class gene:
    def __init__(self):
        # random initialise the gene according to the representation
        self.__gene = choice([UP, DOWN, LEFT, RIGHT])

    def get_direction(self):
        return self.__gene

    def set_direction(self, otherDirection):

        if otherDirection not in [UP, DOWN, LEFT, RIGHT]:
            raise Exception("Invalid direction!")
        self.__gene= otherDirection

class Individual:
    def __init__(self, size = 0):
        self.__size = size

        #chromosome
        self.__chromozome = [gene() for i in range(self.__size)]
        self.__fitness = None

    def get_size(self):
        return self.__size

    def get_gene(self, genePosition):
        if genePosition >= self.__size:
            raise Exception("No gene!")
        return self.__chromozome[genePosition]

    def set_gene(self, genePosition, newGene):
        if genePosition >= self.__size:
            raise Exception("No gene!")
        self.__chromozome[genePosition] = newGene


    def get_chromosome(self):
        return self.__chromozome

    def set_chromosome(self, chromosome):
        self.__chromozome = chromosome

        
    def fitness(self, map, x, y):
        # x, y represents the starting position of the drone.
        posx, posy = x, y
        copy_map = map.copy()
        score = 0
        score += copy_map.markVisible(x, y)
        for gene in self.__chromozome:
            direction = gene.get_direction()
            if direction == UP:
                posx = posx - 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (copy_map[posx][posy] == 1):
                    posx = posx + 1
                    continue
                #score += copy_map.markVisible(posx, posy)

            if direction == DOWN:
                posx = posx + 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (copy_map[posx][posy] == 1):
                    posx = posx - 1
                    continue
                #score += copy_map.markVisible(posx, posy)

            if direction == LEFT:
                posy = posy - 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (copy_map[posx][posy] == 1):
                    posy = posy + 1
                    continue
                #score += copy_map.markVisible(posx, posy)

            if direction == RIGHT:
                posy = posy + 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (copy_map[posx][posy] == 1):
                    posy = posy - 1
                    continue
                #score += copy_map.markVisible(posx, posy)


            score += copy_map.markVisible(posx, posy)

        self.__fitness = score
        return self.__fitness

    
    def mutate(self, mutateProbability = 0.04):
        if random() < mutateProbability:
            mutated_gene = randrange(self.__size)
            self.__chromozome[mutated_gene].set_direction(choice([UP, DOWN, LEFT, RIGHT]))
            # perform a mutation with respect to the representation
        
    
    def crossover(self, otherParent, crossoverProbability = 0.7):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossoverProbability:
            border = randrange(0, self.__size)
            for i in range(border):
                offspring1.set_gene(i, self.get_gene(i))
                offspring2.set_gene(i, otherParent.get_gene(i))
            for j in range(border, self.__size):
                offspring1.set_gene(j, otherParent.get_gene(j))
                offspring2.set_gene(j, self.get_gene(j))
        else:
            offspring1.set_chromosome(self.get_chromosome())
            offspring2.set_chromosome(otherParent.get_chromosome())
        
        return offspring1, offspring2
    
class Population():
    def __init__(self, chromozomeSize = 0, initialX=0, initialY=0, map = None):
        self.__chromozomeSize = chromozomeSize # chromozome size
        self.__individuals = []
        self.__x = initialX
        self.__y = initialY
        self.map = map

        self.__individuals_scores = {}
        # for ind in self.__individuals:
        #     self.__individuals_scores[ind] = 0

        self.__total = 0
        self.__best = 0
        self.__bestIndividual = None

    def clear_individuals(self):
        self.__individuals.clear()
        self.__individuals_scores = {}

    def evaluate(self):
        # evaluates the population

        self.__total = 0
        self.__best = 0
        self.__bestIndividual = None

        for x in self.__individuals:
            individual_score = x.fitness(self.map, self.__x, self.__y)
            self.__individuals_scores[x] = individual_score
            self.__total += individual_score
            if individual_score > self.__best:
                self.__best = individual_score
                self.__bestIndividual = x
        return self.__total, self.__best

    def add_individuals_scores(self, individuals_scores):
        # individuals_scores - dict with individuals and scores
        for i in individuals_scores:
            self.__individuals.append(i)
            self.__individuals_scores[i] = individuals_scores[i]
            if individuals_scores[i] >= self.__best:
                self.__best = individuals_scores[i]
                self.__bestIndividual = i
            self.__total += individuals_scores[i]

    def __len__(self):
        return len(self.__individuals)

    @property
    def populationSize(self):
        return len(self.__individuals)

    @property
    def average(self):
        return self.__total / len(self.__individuals)

    @property
    def total(self):
        return self.__total

    @property
    def best(self):
        return self.__best

    @property
    def individuals(self):
        return self.__individuals

    @property
    def individuals_with_scores(self):
        return self.__individuals_scores

    @property
    def bestIndividual(self):
        return self.__bestIndividual

    def getStartingPosition(self):
        return self.__x, self.__y

    def get_chromozome_size(self):
        return self.__chromozomeSize

    def random_individuals(self, size):
        # generate a population with given size
        self.__individuals_scores = {}
        self.__individuals = [Individual(self.__chromozomeSize) for i in range(size)]
        self.evaluate()

    def set_individuals(self, individuals):
        # generate a population from list of individuals
        self.__individuals_scores = {}
        self.__individuals.clear()
        for i in individuals:
            if len(i.get_chromosome()) != self.__chromozomeSize:
                raise Exception('Incompatible individuals!')
            self.__individuals.append(i)
        self.evaluate()


    def selection(self, k = 0):
        selected = set()
        while(len(selected) != k):
            individual = np.random.choice(self.__individuals, 1, False,
                                          [(self.__individuals_scores[y] / self.__total) for y in self.__individuals])
            selected.add(individual[0])
        return selected
            
    def bestK(self, k = 2):
        a = nlargest(k, self.__individuals_scores, key=self.__individuals_scores.get)
        x1 = []
        x2 = []
        for i in self.__individuals:
            x1.append(self.__individuals_scores[i])
        for i in a:
            x2.append(self.__individuals_scores[i])
        x1.sort(reverse=True)
        print(x1)
        print(x2)
        print(len(self.__individuals))
        print(len(self.__individuals_scores))
        print('---------------')
        return a

    def filter(self, k):
        # filter , keep the best individuals
        filtered = self.bestK(k)
        survivors = {}
        for ind in filtered:
            survivors[ind] = self.__individuals_scores[ind]
        self.clear_individuals()
        self.__best = 0
        self.__total = 0
        self.__bestIndividual = None
        self.add_individuals_scores(survivors)

    def find_optimal_solution(self):
        genes = [gene(), gene(), gene(), gene()]
        genes[0].set_direction(UP)
        genes[1].set_direction(DOWN)
        genes[2].set_direction(LEFT)
        genes[3].set_direction(RIGHT)

        ALL_CHROMOSOMES = itertools.product(genes, repeat=self.__chromozomeSize)
        best_score = 0
        best_individual = None

        i = 0

        for c in ALL_CHROMOSOMES:
            i += 1
            print(i)
            chromosome = list(c)
            print(chromosome)
            ind = Individual(self.__chromozomeSize)
            ind.set_chromosome(chromosome)
            score = ind.fitness(self.map, self.__x, self.__y)
            if score > best_score:
                best_individual = ind
                best_score = score

        return best_individual.get_chromosome(), best_score

        # a = [LEFT, RIGHT, UP, DOWN]
        # x = itertools.product(a, repeat=10)
        # i = 0
        # for e in x:
        #     print(e)
        #     i += 1
        # print(i)

    
class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))


    # creates a random map of given size
    def randomMap(self, fill = 0.2, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1
                else:
                    self.surface[i][j] = 0

    def __getitem__(self, key):
        return self.surface[key]

    def get_size(self):
        return self.n, self.m
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def copy(self):
        copy = Map(self.n, self.m)
        copy.surface = np.array(self.surface, copy=True)
        return copy

    def readUDMSensors(self, x,y):
        readings=[0,0,0,0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.n) and (self.surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.m) and (self.surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1
        return readings

    def markVisible(self, x, y):

        marked = 0

        if self.surface[x][y] == 0:
            marked += 1

        self.surface[x][y] = 2
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.surface[xf][y] != 1)):

            # add to the count if it wasn't marked previously
            if self.surface[xf][y] == 0:
                marked += 1

            self.surface[xf][y] = 2
            xf = xf - 1

        # DOWN
        xf = x + 1
        while ((xf < self.n) and (self.surface[xf][y] != 1)):

            # add to the count if it wasn't marked previously
            if self.surface[xf][y] == 0:
                marked += 1

            self.surface[xf][y] = 2
            xf = xf + 1

        # LEFT
        yf = y + 1
        while ((yf < self.m) and (self.surface[x][yf] != 1)):

            # add to the count if it wasn't marked previously
            if self.surface[x][yf] == 0:
                marked += 1

            self.surface[x][yf] = 2
            yf = yf + 1

        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.surface[x][yf] != 1)):

            # add to the count if it wasn't marked previously
            if self.surface[x][yf] == 0:
                marked += 1

            self.surface[x][yf] = 2
            yf = yf - 1

        return marked

    # def image(self, colour=BLUE, background=WHITE):
    #     imagine = pygame.Surface((400, 400))
    #     brick = pygame.Surface((20, 20))
    #     destination = pygame.Surface((20, 20))
    #     roadGreedy = pygame.Surface((20, 20))
    #     roadAStar = pygame.Surface((20, 20))
    #     common_road = pygame.Surface((20, 20))
    #     brick.fill(BLUE)
    #     imagine.fill(WHITE)
    #     destination.fill(RED)
    #
    #     for i in range(self.n):
    #         for j in range(self.m):
    #             if (self.surface[i][j] == 1):
    #                 imagine.blit(brick, (j * 20, i * 20))
    #             if (self.surface[i][j] == 2):
    #                 imagine.blit(destination, (j * 20, i * 20))
    #             if (self.surface[i][j] == 3):
    #                 imagine.blit(roadGreedy, (j * 20, i * 20))
    #             if (self.surface[i][j] == 4):
    #                 imagine.blit(roadAStar, (j * 20, i * 20))
    #             if (self.surface[i][j] == 5):
    #                 imagine.blit(common_road, (j * 20, i * 20))
    #
    #     return imagine

    def get_neighbours(self, xi, yi):
        possibilities = [(xi + 1, yi), (xi - 1, yi), (xi, yi + 1), (xi, yi - 1)]

        # squares have coordinates between 0 and 19
        first_cut = list(filter(lambda t: (0 <= t[0] <= 19 and 0 <= t[1] <= 19), possibilities))

        return list(filter(lambda t: (self.surface[t[0]][t[1]] == 0 or self.surface[t[0]][t[1]] >= 2), first_cut))

    def convertChromozomeToPath(self, chromozome, x, y):
        path = []
        path.append([x,y])
        posx = x
        posy = y
        for gene in chromozome:
            direction = gene.get_direction()
            if direction == UP:
                posx = posx - 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (self.surface[posx][posy] == 1):
                    posx = posx + 1
                    continue
                # score += copy_map.markVisible(posx, posy)

            elif direction == DOWN:
                posx = posx + 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (self.surface[posx][posy] == 1):
                    posx = posx - 1
                    continue
                # score += copy_map.markVisible(posx, posy)

            elif direction == LEFT:
                posy = posy - 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (self.surface[posx][posy] == 1):
                    posy = posy + 1
                    continue
                # score += copy_map.markVisible(posx, posy)

            elif direction == RIGHT:
                posy = posy + 1
                if not (0 <= posx <= 19) or not (0 <= posy <= 19) or (self.surface[posx][posy] == 1):
                    posy = posy - 1
                    continue
                # score += copy_map.markVisible(posx, posy)
            print('added')
            path.append([posx, posy])
        return path



class Statistics:
    def __init__(self):
        self.runs = []
        self.best = []
        self.std = []

    def add_generation_score(self, score):
        self.runs.append(score)

    def add_best_score(self, score):
        self.best.append(score)

    def add_standard_deviation(self, std):
        self.std.append(std)

    def get_scores(self):
        return self.runs, self.best, self.std

