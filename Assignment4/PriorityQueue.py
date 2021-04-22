class PriorityQueue:
    def __init__(self):
        self.__values = {}

    def __str__(self):
        out = ''
        for el in self.__values:
            out += str(el)
            out += ':'
            out += str(self.__values[el])
            out += '\n'
        return out[:-1]

    def isEmpty(self):
        return len(self.__values) == 0

    def pop(self):
        topPriority = None
        topObject = None
        for obj in self.__values:
            objPriority = self.__values[obj]
            if topPriority is None or topPriority > objPriority:
                topPriority = objPriority
                topObject = obj
        del self.__values[topObject]
        return topObject, topPriority

    def add(self, obj, priority):
        self.__values[obj] = priority

    def contains(self, val):
        return val in self.__values

    def getObjPriority(self, obj):
        return self.__values[obj]

    def update(self, key, value):
        if key not in self.__values:
            raise Exception("Not in dict.")
        self.__values[key] = value


# a = PriorityQueue()
# a.add(2,4)
# a.add(3,9)
#
# print(a)
# print(a.contains(4))
#
#
# #
# # a = [(2,3),(3,4), (2,7),(3,9), (4,1), (5,2)]
# # print(list(filter(lambda t: t[0] == 2 or 1 <= t[1] <= 2, a)))
# print(-13 > -16)

a = set()
a.add(12)
print(12 in a)

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

        return list(reversed(route))

    return []