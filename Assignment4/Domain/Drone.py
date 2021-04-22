import copy
from random import randint, random, choice
from typing import List, Tuple, Dict
import numpy as np
from Domain.Map import Map


class Ant:
    def __init__(self, mapM: Map,
                 initial_position: Tuple,
                 energy: int,
                 path=None):

        if path is None:
            self.path = []

        # add the initial posititon of the ant to the path
        self.path.append(0)

        self.energy = energy
        self.mapM = copy.deepcopy(mapM)

        #list of senzors that need to be visited
        self.toVisit = [id for id in range(1, mapM.number_of_senzors + 1)]

        # total area surveilled (MOVED IN MAP)
        self.total_surveillance = 0

        self.energy_for_sensors = 0

        # initial position is labeled as senzor 0 in the service
        self.current_sensor_id = 0




    def addMove(self, q0, alpha, beta,
                distances_between_senzors: Dict[Tuple[int, int], int],
                pheromone_between_senzors: Dict[Tuple[int, int], int]):

        if len(self.toVisit) == 0:
            return False

        probablilities = []
        total = 0

        max = -1
        max_neXt = None

        for index in range(len(self.toVisit)):
            prob = ((pheromone_between_senzors[(self.current_sensor_id,self.toVisit[index])]) ** alpha) *\
                   (distances_between_senzors[(self.current_sensor_id, self.toVisit[index])] ** (-beta))
            probablilities.append(prob)
            total += prob

            if prob > max:
                max = prob
                max_neXt = self.toVisit[index]

        if (random() < q0):
            # adaugam cea mai buna dintre mutarile posibile
            next = max_neXt


        else:
            next = np.random.choice(self.toVisit, 1, False, [prob / total for prob in probablilities])
        next = int(next)
        self.toVisit.remove(next)
        self.path.append(next)
        self.current_sensor_id = next

        return True

    def fitness(self, distances_between_senzors: Dict[Tuple[int, int], int]):
        path_length = 0
        for index in range(len(self.path) - 1):
            path_length += distances_between_senzors[(self.path[index], self.path[index + 1])] - 1

        return path_length

