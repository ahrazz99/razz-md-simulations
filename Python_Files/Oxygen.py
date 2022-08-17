import Atom
import Hydrogen
import Axis


class Oxygen(Atom):
    #Initialization of Oxygen Object using superclass as well
    def __init__(self, posX, posY, posZ):
        super()__init__(posX, posY, posZ)
        self.__neighbors = []
    
    #addChemBonds method
    #Input:
    #Output:
    def addChemBond(self, atom):
        if isinstance(atom, Hydrogen):
            self.getChemBonds().append(atom)
        else:
            print("That is not a Hydrogen Atom")
            return
        return
    
    #removeChemBonds method - removes the hydrogen from the given index if there is one. 
    #Input
    def removeBond(self, index):
        if len(self.getChemBonds()) == 0:
            print("Nothing to remove")
            return none

        elif len(self.getChemBonds()) < (index + 1):
            print("There is no bond there to remove")
            return none

        else:
            return self.getChemBonds().pop(index)
    
    def removeAllBonds(self):
        bonds = self.getChemBonds()
        self.getChemBonds().clear()
        return bonds

    def getChemBond(self, index):
        if len(self.getChemBonds()) < (index + 1):
            print("There is no atom bonded in that position")
            return
        else:
            return self.getChemBonds()[index]

    def addNeighbor(self, neighOxy):
        self.__neighbors.append(neighOxy)

    def getNumNeighbors(self):
        return len(self.__neighbors)

    def getNeighbor(self, index):
        if len(self.__neighbors) < index + 1:
            return none
        else:
            return self.__neighbors[index]


    


