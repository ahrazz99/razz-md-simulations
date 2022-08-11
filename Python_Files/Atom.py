from abc import ABC, abstractmethod
import Axis


class Atom(ABC):
    """Class Atom to be used as the parent class to the Oxygen and Hydrogen 
        classes to allow for polymorphism"""
    def __init__(self, posX, posY, posZ):
        """Atom Constructor"""
        self.__posX = 0
        self.__posY = 0
        self.__posZ = 0
        self.__chemBonds = []
        self.__axes = []

    def getPosition(self):
        return [self.__posX, self.__posY, self.__posZ]

    def getChemBonds(self):
        return self.__chemBonds
    
    def getAxes(self):
        return self.__axes

    @abstractmethod
    def addChemBond(self, Atom=atom):
        pass

    @abstractmethod
    def addAxis(self, Axis=axis):
        pass
