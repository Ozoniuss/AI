from UI.gui import *
from  Service.service import Service

class Ui:
    def __init__(self, service : Service):
        self.__service = service


    def printMenu(self):
        print('a. create random map\nb. load a map\nc. save a map\nd. visualise map\ne. run the algorighm\nf. exit\n'
              'g. test shortest path\n')

    def run(self):
        self.printMenu()
        option = input('Pick your option.')
        while option not in 'abcdefg':
            option = input("Choose another option")
        while True:
            if option == "a":
                pass
            elif option == 'b':
                pass
            elif option == 'c':
                pass
            elif option == 'd':
                self.visualizeMap()

            elif option == 'e':
                self.run()

            elif option == 'f':
                break

            elif option == 'g':
                a = input("Enter destination coord: ")
                x, y = a.split(' ')
                coords = (int(x), int(y))
                path = self.__service.getMap().searchAStar(self.__service.starting_position[0],
                                                           self.__service.starting_position[1],
                                                           coords[0], coords[1])
                movingDrone(self.__service.getMap(), path)


            else:
                print('Invalid option.')

            option = input("Choose another option >>> ")

    def visualizeMap(self):
        print(self.__service.getMap())
        screen = initPyGame((20*self.__service.getMap().get_size()[0], 20*self.__service.getMap().get_size()[1]))
        img = image(self.__service.getMap())
        displayMapImage(screen, img, 5, 2)

    def saveMap(self):
        filename = input("Enter the name of the file to save the map:")
        try:
            self.__service.saveMap(filename)
            print('The map has been saved!')
        except Exception as e:
            print(str(e))

    def loadMap(self):
        filename = input("Enter the name of the file to load the map:")
        try:
            self.__service.loadMap(filename)
            print('The map has been loaded!')
        except Exception as e:
            print(str(e))

    def run(self):
        sol = self.__service.run_solver()
        print(sol)