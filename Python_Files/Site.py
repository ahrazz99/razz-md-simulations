import Oxygen

class Site():

    def __init__(self, oxygen, posX, posY, posZ):
        self.__oxygen = oxygen
        self.__posX = posX
        self.__posY = posY
        self.__posZ = posZ
        self.__occupied = false
        self.__hydrogen = none

    def getPosX(self):
        return self.__posX

    def getPosY(self):
        return self.__posY

    def getPosZ(self):
        return self.__posZ

    def getOxygen(self):
        return self.__oxygen

    def addHydrogen(self, hyd):
        self.__hydrogen = hyd

    def getHydrogen(self):
        return self.__hydrogen

    def deleteHydrogen(self):
        self.__hydrogen = none

    def removeHydrogen(self):
        hyd = self.__hydrogen
        self.__hydrogen = none
        return hyd





