"""Imports"""
from Site import Site
import math
from Oxygen import Oxygen
from GhostOxygen import GhostOxygen

"""Class Header"""
class Axis():
    """Constructor"""
    def __init__(self, oxyA, oxyB, ghost):
        self.__oxy1 = oxyA
        self.__length = self.__calcLength(oxyA.getPosition(), oxyB.getPosition())
        self.__oxy2= oxyB
        self.__site1 = self.__calcSitePos(oxyA, oxyB)
        self.__site2 = self.__calcSitePos(oxyB, oxyA)
        self.__hasHydrogen = False
        self.__isGhostAxis = ghost
        self.__connectedAxis = None

    """Methods"""
    #hasHydrogen method
    #   input; none
    #   output: True or False
    def hasHydrogen(self):
        return self.__hasHydrogen

    def isGhostAxis(self):
        return self.__isGhostAxis

    #addGhostHyd method:
    #   input: none
    #   output: none
    def addGhostHyd(self):
        self.__hasHydrogen = True

    #getOccupiedSite method
    #   Input: none
    #   output: the number of site where the hydrogen is or -1 if there is not one.
    def getOccupiedSite(self):
        if self.__site1.isOccupied():
            return 1
        elif self.__site2.isOccupied():
            return 2
        else:
            return -1

    #addConnectedAxis method
    #   Input: the axis that is connected to this one 
    #   output: none
    #   Why: This is to prevent increased probabilty of choosing and modifying a hydrogen
    #       on a ghost axis
    def addConnectedAxis(self, axis):
        self.__connectedAxis = axis

    #getConnectedAxis method
    #   Input: none
    #   Output: the axis that is connected to this axis
    def getConnectedAxis(self):
        return self.__connectedAxis

    #getOxygens
    #   Input: none
    #   output: a list representation of the 2 oxygens
    def getOxygens(self):
        return [self.__oxy1, self.__oxy2]
    
    #addHydrogen method
    #   Input: Hydrogen to add to a Site, the Site to add to (1 or 2)
    #   output: True or False depending on if it was successful
    def addHydrogen(self, hyd, site):
        if not self.__hasHydrogen:
            if site == 1:
                self.__hasHydrogen = self.__site1.addHydrogen(hyd)
                return self.__hasHydrogen
            elif site == 2:
                self.__hasHydrogen = self.__site2.addHydrogen(hyd)
                return self.__hasHydrogen
            else:
                return False
        return False
    
    #getHydrogen method
    #   Input: the site from which to get a hydrogen
    #   Output: None if there isn't a hydrogen, otherwise, the Hydrogen
    def getHydrogen(self, site):
        if self.__hasHydrogen:
            if site == 1:
                return self.__site1.getHydrogen()
            elif site == 2:
                return self.__site2.getHydrogen()
            else:
                return None
        else:
            return None
    
    def pullHyd(self):
        if self.__isGhostAxis:
            if self.__site1.isOccupied():
                return self.__site1.getHydrogen()
            else:
                return self.__connectedAxis.__site1.getHydrogen()
        else:
            if self.__site1.isOccupied():
                return self.__site1.getHydrogen()
            else:
                return self.__site2.getHydrogen()

    #delHydrogens method
    #   Input; none
    #   Output; none, but there will be no hydrogen on the axis
    def delHydrogens(self):
        if self.__site1.isOccupied():
            self.__site1.delHydrogen()
        elif self.__site2.isOccupied():
            self.__site2.delHydrogen()
        self.__hasHydrogen = False

    #delHydrogen method
    def delHydrogen(self, site):
        hyd = None
        if site == 1 and self.__site1.isOccupied():
            hyd = self.__site1.delHydrogen()
            self.__hasHydrogen = False
            return hyd
        elif site == 2 and self.__site2.isOccupied():
            hyd = self.__site2.delHydrogen()
            self.__hasHydrogen = False
            return hyd

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

    #getSiteRealId method
    #   Returns the site number of the site next to the real Oxygen Atom
    #   Input: None
    #   Output: 1 or 2 or -1
    def getSiteRealId(self):
        if isinstance(self.__oxy1, GhostOxygen):
            return 2
        elif isinstance(self.__oxy2, GhostOxygen):
            return 1
        return -1

    #getSiteRealPosition method
    #   Returns the site position of the site next to a real Oxygen Atom
    #   Input: None
    #   Output: the site position of the site next to the real oxygen
    def getSiteRealPosition(self):
        if isinstance(self.__oxy1, GhostOxygen):
            return self.__site2.getPosition()
        elif isinstance(self.__oxy2, GhostOxygen):
            return self.__site1.getPosition()
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
