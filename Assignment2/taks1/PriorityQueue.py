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