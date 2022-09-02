
class Atom(object):
    """Class Atom to be used as the parent class to the Oxygen and Hydrogen 
        classes to allow for polymorphism
    """

    """Constructor"""
    def __init__(self, position):
        self.__position = position
        self.__chemBonds = []

    """Methods"""

    #getPosition method
    #   input: none
    #   output: the position of the Atom
    def getPosition(self):
        return self.__position
    
    #addChemBond method
    #   input: the Atom to add to the list
    #   output: none
    def addChemBond(self, atom):
        self.__chemBonds.append(atom)

    #getChemBond method
    #   input: the index of the bond desired
    #   output: the bond at the index if present, none if not
    def getChemBond(self, index):
        if len(self.__chemBonds) < (index + 1):
            return None
        else:
            return self.__chemBonds[index]
    def getBonds(self):
        return self.__chemBonds
    
    #getNumBonds method
    #   input: none
    #   output: the number of chemical bonds the atom currently has
    def getNumBonds(self):
        return len(self.__chemBonds)
   
    def changePosition(self, position):
        self.__position = position

    #delChemBond method
    #   input: the atom to remove
    #   output: none
    def delAtom(self, atom):
        if atom is None:
            return
        for i in range(len(self.__chemBonds)):
            if self.__chemBonds[i] == atom:
                self.__chemBonds.pop(i)
                return
        return

    #OVerriding Equals function
    #   Input: self and object to compare to
    #   Output: true if the 2 atoms' positions are the same
    def __eq__(self, other):
        posXCheck = self.__position[0] == other.__position[0]
        posYCheck = self.__position[1] == other.__position[1]
        posZCheck = self.__position[2] == other.__position[2]
        return posXCheck and posYCheck and posZCheck
        
