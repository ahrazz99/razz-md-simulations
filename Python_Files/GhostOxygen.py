'''Imports'''
from Oxygen import Oxygen

"""Class Header"""
class GhostOxygen(Oxygen):
    """Constructor"""
    def __init__(self, position, refOId, Id):
        super().__init__(position, Id)
        self.__refOId = refOId
        
    """Methods"""
    
    #getReferenceOxygen method
    #   Input: None
    #   Output: returns the ID for the oxygen that the ghost is referenced from.
    def getRefO(self):
        return self.__refOId
