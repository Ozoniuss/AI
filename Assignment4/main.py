from UI.ui import *

# Starting position is 2, 3
s = Service(Map(), (5,2))
s.loadMap("test1.map")
s.getMap().place_senzors([(7,8), (1,15), (6,9), (9,6), (4, 2), (0,18), (0,12), (19,19), (15,12)])
s.initialize_all_parameters()

# service senzors setup
s.find_senzors_positions()
s.find_distances_between_all_senzors()


u = Ui(s)

if __name__ == '__main__':
    u.run()