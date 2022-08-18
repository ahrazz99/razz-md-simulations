"""imports"""
import Hydrogen

"""Class Header"""
class Site():
    """Constructor"""
    def __init__(self, position):
        self.__position = position
        self.__occupied = False
        self.__hydrogen = None
    """Methods"""

    #getPosition method
    #   input: none
    #   output: the position of the Site
    def getPosition(self):
        return self.__position
    
    #addHydrogen method
    #   input: the hydrogen to add to the site
    #   output: true if sucessful, false if not
    def addHydrogen(self, hyd):
        if self.__occupied:
            return False
        else:
            self.__hydrogen = hyd
            self.__occupied = True
            return True
    
    #isOccupied method
    #   input: none
    #   output: True or False depending on if the Site is occupied
    def isOccupied(self):
        return self.__occupied

    #getHydrogen method
    #   input: none
    #   output: the hydrogen or none
    def getHydrogen(self):
        return self.__hydrogen
    
    #delHydrogen
    #   input: none
    #   output: the deleted hydrogen (none if there isn't one)
    def delHydrogen(self):
        hyd = self.__hydrogen
        self.__hydrogen = None
        return hyd





