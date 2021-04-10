from random import *
import numpy as np
from heapq import nlargest
from utils import *
# Initialize dictionary
test_dict = {'gfg': 1, 'is': 4, 'best': 6, 'for': 7, 'geeks': 3}

# Initialize N
N = 3

# printing original dictionary
print("The original dictionary is : " + str(test_dict))

# N largest values in dictionary
# Using nlargest
res = nlargest(N, test_dict, key=test_dict.get)

# printing result
print("The top N value pairs are  " + str(res))
print(test_dict)

d = {1:'1', 2:'c', 3:'d'}
for a in d:
    print(d[a])

b= [1,2,3]
a = np.random.choice(b)
print(a)
print(b)

print(np.array(b).std())


import itertools


a = [LEFT, RIGHT, UP, DOWN]
x = itertools.product(a, repeat=10)
i = 0
for e in x:
    print(e)
    i += 1
print(i)