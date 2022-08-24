"""Imports"""
from Atom import Atom

"""Class Header"""
class Hydrogen(Atom):
    """Constructor"""
    def __init__(self, position):
        super().__init__(position)

    """Methods"""
    #addChemBond overriden method
    #   input: the bond to add
    #   output: false if there is already a bonded Atom
    #           otherwise, returns true
    def addChemBond(self, atom):
        if len(self.__chemBonds) > 0:
            return false
        else:
            self.__chemBonds.append(atom)
            return true
    
    #getChemBond overridden method
    #   input: none
    #   output: the Atom bonded to this Hydrogen
    def getChemBond(self):
        if len(self.__chemBonds) == 0:
            return none
        else:
            return self.__chemBonds[0]

    #delChemBond overriden method
    #   input: none
    #   output: the deleted chemically bonded Atom; none if no bond exists
    def delChemBond(self):
        if len(self.getChemBonds()) == 0:
            return none
        else:
            return self.getChembonds().pop(0)


