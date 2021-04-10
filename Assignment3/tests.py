import unittest
from repository import Repository
from domain import Map

# repository = Repository()
# repository.cmap = Map()
# repository.cmap.randomMap()
# repository.saveMap("test1.map")

# repository.loadMap("test1.map")
# print(repository.cmap)



class Tests(unittest.TestCase):


    def setUp(self) -> None:
        self.repository = Repository()
        self.repository.loadMap("test1.map")
        print(self.repository.cmap)

    def tearDown(self) -> None:
        pass

    def test_mark_visible(self):
        n1 = self.repository.cmap.mark_vizible(18,7)
        self.assertEqual(n1, 2)
        print(self.repository.cmap)
        n2 = self.repository.cmap.mark_vizible(17,4)
        self.assertEqual(n2, 7)
        print(self.repository.cmap)
        n3 = self.repository.cmap.mark_vizible(0, 19)
        self.assertEqual(n3, 10)
        print(self.repository.cmap)