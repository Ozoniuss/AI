from ui import *

r = Repository(x=2, y=2)
r.loadMap("test1.map")
p = r.createRandomPopulation(20, 200)
r.addPopulation(p)
s = Statistics()
c = Controller(r, s)
u = Ui(c)

if __name__ == '__main__':
    u.run()