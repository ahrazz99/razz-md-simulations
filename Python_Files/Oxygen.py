"""imports"""
from Atom import Atom

"""Class Header"""
class Oxygen(Atom):
    """Constructor"""
    def __init__(self, position, Id):
        super().__init__(position)
        self.__neighbors = []
        self.__Id = Id
    
    
    """Methods"""
    #addNeighbor method
    #   input: the neighbor Oxygen to add
    #   output: none
    def addNeighbor(self, neighOxy):
        self.__neighbors.append(neighOxy)
    
    #getNumNeighbors method
    #   input: none
    #   output: the number of neighboring Oxygens
    def getNumNeighbors(self):
        return len(self.__neighbors)

    #getNeighbor method
    #   input: the index of the neighbor to pull
    #   output: none if the index does not work, 
    #           the neighbor at the index
    def getNeighbor(self, index):
        if len(self.__neighbors) < index + 1:
            return None
        else:
            return self.__neighbors[index]
    
    #getId
    def getId(self):
        return self.__Id

    


