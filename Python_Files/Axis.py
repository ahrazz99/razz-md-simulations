"""Imports"""
from Site import Site
import math
from Oxygen import Oxygen

"""Class Header"""
class Axis():
    """Constructor"""
    def __init__(self, oxyA, oxyB):
        self.__oxy1 = oxyA
        self.__length = self.__calcLength(oxyA.getPosition(), oxyB.getPosition())
        self.__oxy2= oxyB
        self.__site1 = self.__calcSitePos(oxyA, oxyB)
        self.__site2 = self.__calcSitePos(oxyB, oxyA)

    """Methods"""
    #getOxygens
    #   Input: none
    #   output: a list representation of the 2 oxygens
    def getOxygens(self):
        return [self.__oxy1, self.__oxy2]
    
    #addHydrogen method
    #   Input: Hydrogen to add to a Site, the Site to add to (1 or 2)
    #   output: True or False depending on if it was successful
    def addHydrogen(self, hyd, site):
        if site == 1:
            return self.__site1.addHydrogen(hyd)
        elif site == 2:
            return self.__site2.addHydrogen(hyd)
        else:
            return False
    
    #getHydrogen method
    #   Input: the site from which to get a hydrogen
    #   Output: None if there isn't a hydrogen, otherwise, the Hydrogen
    def getHydrogen(self, site):
        if site == 1:
            return self.__site1.getHydrogen()
        elif site == 2:
            return self.__site2.getHydrogen()
        else:
            return None

    #getSitePosition method
    #   Input: the site to get the position of
    #   Output: a list representation of the Site's position, or an empty list
    def getSitePosition(self, site):
        if site == 1:
            return self.__site1.getPosition()
        elif site == 2:
            return self.__site2.getPosition()
        else:
            return []

    #__calcLength method: calculate the length between positions loc1 and loc2 that are arrays [x,y,z]
    #   input: the 2 locations to calculate the distance between
    #   output: the distance
    def __calcLength(self, loc1, loc2):
        return math.dist(loc1, loc2)
    
    #__genSite: Calculate the position of the Site closer to oxy1 and return it.
    #   input: the 2 oxygens between which to generate the site
    #   output: the Site generated closer to oxy1
    def __calcSitePos(self, oxy1, oxy2):
        oxy1Pos = oxy1.getPosition()
        oxy2Pos = oxy2.getPosition()
        length = self.__calcLength(oxy1Pos, oxy2Pos)
        vec = [oxy2Pos[0] - oxy1Pos[0], oxy2Pos[1]-oxy1Pos[1], oxy2Pos[2]-oxy1Pos[2]]
        
        #Divide vec by its length so it is a unit vector pointing down the axis
        for i in range(3):
            vec[i] = vec[i]/length
        #Add the unit vector to the first vector to get the position of the site
        posX = oxy1Pos[0] + vec[0]
        posY = oxy1Pos[1] + vec[1]
        posZ = oxy1Pos[2] + vec[2]
        
        #Generate and return the new Site 
        site = Site([posX, posY, posZ])
        return site
