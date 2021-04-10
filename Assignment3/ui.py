# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *
from matplotlib import pyplot as plt

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class Ui:
    def __init__(self, controller):
        self.__controller = controller
        self.__statistics = None
        self.__bestIndividual = None
        # self.chromozomeSize = 20
        # self.populationSize= 50

    def printMenu(self):
        print('1. Map options:\n2. EA options:\n3. Quit')

    def run(self):
        self.printMenu()
        option = None
        while option != '3':
            option = input("Choose your menu option")
            if option == '1':
                self.map_options()
            if option == '2':
                self.EA_options()

    def printMapMenu(self):
        print('a. create random map\nb. load a map\nc. save a map\nd. visualise map\ne. back\n')

    def printEAMenu(self):
        print('a. parameters setup\nb. run the solver\nc. visualize statistics\nd. view the drone moving on a path\ne. free roam\nf. Find optimal solution. \n g. back')

    def map_options(self):
        self.printMapMenu()
        letter = input('Pick your option.')
        while letter not in 'abcde':
             letter = input('Invalid option. Pick your option.')
        if letter == "a":
            self.randomMap()
        if letter == 'b':
            self.loadMap()
        if letter == 'c':
            self.saveMap()
        if letter == 'd':
            self.visualizeMap()
        if letter == 'e':
            print('Going back.')

    def EA_options(self):
        self.printEAMenu()
        letter = input('Pick your option.')
        while letter not in 'abcdefg':
             letter = input('Invalid option. Pick your option.')
        if letter == "a":
            self.parametersSetup()
        if letter == 'b':
            self.runSolver()
        if letter == 'c':
            self.visualizeStatistics()
        if letter == 'd':
            self.viewDrone()

        # testing
        if letter == 'e':
            self.freeRoam()

        if letter == 'f':
            self.findOptimalSolution()

        if letter == 'g':
            pass


    def randomMap(self):
        n = int(input('Enter the number of rows >>> '))
        m = int(input('Enter the number of colums >>>'))
        fill = float(input('Enter a fill between 0 and 1 >>> '))
        self.__controller.randomMap(fill,n,m)
        print('A random map has been generated!')

    def saveMap(self):
        filename = input("Enter the name of the file to save the map:")
        try:
            self.__controller.saveMap(filename)
            print('The map has been saved!')
        except Exception as e:
            print(str(e))

    def loadMap(self):
        filename = input("Enter the name of the file to load the map:")
        try:
            self.__controller.loadMap(filename)
            print('The map has been loaded!')
        except Exception as e:
            print(str(e))

    def visualizeMap(self):
        print(self.__controller.getMap())
        screen = initPyGame((20*self.__controller.getMap().get_size()[0], 20*self.__controller.getMap().get_size()[1]))
        img = image(self.__controller.getMap())
        displayMapImage(screen, img, self.__controller.getStartingPosition()[0], self.__controller.getStartingPosition()[1])

    def parametersSetup(self):
        self.__chromozomeSize = int(input('Enter chromozome size >>> '))
        self.__populationSize = int(input('Enter population size >>> '))

    def runSolver(self):
        seed(randint(1, 1000))
        generations = int(input("For how many generations should we run? >>> "))
        self.__statistics, self.__bestIndividual = self.__controller.run(generations)
        avg =  self.__statistics.get_scores()[0]
        best =  self.__statistics.get_scores()[1]
        all = self.__statistics.get_scores()[2]
        for i in range(generations):
            print(str(avg[i]) + ', ' + str(best[i]) + ', '+ str(all[i]))

    def visualizeStatistics(self):
        averages = self.__statistics.get_scores()[0]
        best = self.__statistics.get_scores()[1]
        std = self.__statistics.get_scores()[2]
        print(std)
        plot1 = plt.figure(1)
        plt.plot(averages, color='k', label='Population Average')
        plt.plot(best, color='b', label='Population Best')
        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Genetic algorithm evaluation')

        plot2=plt.figure(2)
        plt.errorbar(np.arange(1, len(averages) + 1), averages, yerr=std, fmt='o')
        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Genetic algorithm standard deviation')

        plt.show()


    def viewDrone(self):
        chromozome = self.__bestIndividual.get_chromosome()
        print(len(chromozome))
        path = self.__controller.getMap().convertChromozomeToPath(chromozome, self.__controller.getStartingPosition()[0],
                                                                  self.__controller.getStartingPosition()[1])

        print(len(path))
        movingDrone(self.__controller.getMap(), path)

    def freeRoam(self):
        a = Individual(2)
        path = [[2,3], [2,2], [1,2], [1,1]]
        chromosome = [gene(), gene(), gene(), gene()]
        chromosome[0].set_direction(UP)
        chromosome[1].set_direction(LEFT)
        chromosome[2].set_direction(UP)
        chromosome[3].set_direction(LEFT)
        a.set_chromosome(chromosome)
        print(a.fitness(self.__controller.getMap(),2,3))

        movingDrone(self.__controller.getMap(),path)

    def findOptimalSolution(self):
        p = Population(self.__controller.getChromozomeSize(), self.__controller.getStartingPosition()[0],
                       self.__controller.getStartingPosition()[1], self.__controller.getMap())
        optimal, score = p.find_optimal_solution()
        # directions = []
        # for gene in optimal:
        #     directions.append(gene.get_direction())
        # movingDrone(self.__controller.getMap(), directions)
        print(score)

print(np.arange(1,len([1,2,3])))

