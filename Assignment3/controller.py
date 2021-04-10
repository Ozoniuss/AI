from repository import *


class Controller:
    def __init__(self, repository, statistics):
        self.__repository = repository
        self.__statistics = statistics

    def getMap(self):
        return self.__repository.cmap

    def randomMap(self, fill=0.2, n=20, m=20):
        self.__repository.randomMap(fill,n,m)

    def saveMap(self, file):
        self.__repository.saveMap(file)

    def loadMap(self, file):
        self.__repository.loadMap(file)

    def getStartingPosition(self):
        return self.__repository.getStartingPosition()

    def getChromozomeSize(self):
        return self.__repository.pop().get_chromozome_size()

    def getBestIndividual(self):
        return self.__repository.getBestIndividual()

    def iteration(self, selection_size=2):
        print('Starting iteration.')
        current_populatuon = self.__repository.pop()
        bst = current_populatuon.best
        avg = current_populatuon.average
        all = list(current_populatuon.individuals_with_scores.values())
        individuals = current_populatuon.individuals
        next_population = list()
        while(len(next_population) != len(individuals)):
            firstParent, secondParent = current_populatuon.selection(2)
            ofs1, ofs2 = firstParent.crossover(secondParent)
            ofs1.mutate()
            ofs2.mutate()
            next_population.append(choice([ofs1, ofs2]))
        newP = Population(chromozomeSize=current_populatuon.get_chromozome_size(),
                          initialX=current_populatuon.getStartingPosition()[0],
                          initialY=current_populatuon.getStartingPosition()[1],
                          map=self.getMap()
                          )

        newP.set_individuals(next_population)
        scores = current_populatuon.individuals_with_scores
        newP.add_individuals_scores(scores)
        newP.filter(len(individuals))
        self.__repository.addPopulation(newP)
        return avg, bst, all




        
    def run(self, generations):
        for i in range(generations):
            avg, bst, all = self.iteration()
            self.__statistics.add_generation_score(avg)
            self.__statistics.add_best_score(bst)
            self.__statistics.add_standard_deviation(np.array(all).std())

        bestIndividual = self.getBestIndividual()

        return self.__statistics, bestIndividual
    
