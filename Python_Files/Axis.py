import Site
import math

class Axis():

    def __init__(self, oxyA, oxyB):
        self.__oxyA = oxyA
        self.__length = self.__calcLength(oxyA.getPosition(), oxyB.getPosition())
        self.__oxyB= oxyB
        self.__site1 = self.__calcSitePos(oxyA, oxyB)
        self.__site2 = self.__calcSitePos(oxyB, oxyA)




    #calculate the length between positions loc1 and loc2 that are arrays [x,y,z]
    def __calcLength(self, loc1, loc2):
        return math.dist(loc1, loc2)
    
    #Calculate the position of the Site closer to oxy1 and return it.
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
        Site site = Site(oxy1, posX, posY, posZ)
        return site
