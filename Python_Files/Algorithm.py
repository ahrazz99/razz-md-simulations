"""
Import Statements
"""
from Atom import Atom
from Axis import Axis
from Hydrogen import Hydrogen
from Oxygen import Oxygen
from Site import Site
from GhostOxygen import GhostOxygen
import sys
import time
import math
import random

"""
Initial Input Pulling
Read information from data file
"""
if len(sys.argv) < 2:
    print("Usage: input the datafile containing the Oxygen Lattice")
    sys.exit(1)

#Open the file given
dataFile = open(sys.argv[1])

#before = time.time()

#Skip the Header
dataFile.readline()
dataFile.readline()

#Pull in the initial set-up values
numAtoms = int(dataFile.readline().removesuffix(" atoms\n"))
numAtomTypes = int(dataFile.readline().removesuffix(" atom types\n"))

dataFile.readline()

xlo, xhi = dataFile.readline().removesuffix(" xlo xhi\n").split(" ")
ylo, yhi = dataFile.readline().removesuffix(" ylo yhi\n").split(" ")
zlo, zhi = dataFile.readline().removesuffix(" zlo zhi\n").split(" ")
xLo = float(xlo)
xHi = float(xhi)
yLo = float(ylo)
yHi = float(yhi)
zLo = float(zlo)
zHi = float(zhi)



#Skip unneeded lines
dataFile.readline()
dataFile.readline()
dataFile.readline()
dataFile.readline()
dataFile.readline()
dataFile.readline()
dataFile.readline()

"""
Generate the Oxygen Atom List
"""
oxygens = []

for i in range(numAtoms):
    atomId, molId, atomType, q, posX, posY, posZ = dataFile.readline().removesuffix(" 0 0 0\n").split(" ")
    oxygens.append(Oxygen([round(float(posX),5), round(float(posY), 5), round(float(posZ), 5)], (i+1)))
dataFile.close()

"""
Axis Generation
Loop through the Oxygen Atoms list and find each neighbor
while generating the lists associated - the Axes and Sites
"""
axes = []

#Needed Values
lowestX = round((2.75 / 4.0) * math.sqrt(8.0/3.0), 5)
lowestY = round((1.0/6.0) * 2.75 * math.sqrt(8.0), 5)
lowestZ = round((3.0/16.0) * 2.75 * 8.0 / 3.0, 5)

numUnitCellsX = round(xHi / (2.75 * math.sqrt(8.0/3.0)), 5)
numUnitCellsY = round(yHi / (2.75 * math.sqrt(8.0)), 5)
numUnitCellsZ = round(zHi / (2.75 * (8.0/3.0)), 5)

highX = round(xHi - lowestX, 5)
highY = round(yHi - lowestY, 5)
highZ = round(zHi - lowestZ, 5)

'''Helpful Methods'''
def isXEdge(posX):
    return posX == lowestX or posX == highX

def isYEdge(posY):
    return posY == lowestY or posY == highY

def isZEdge(posZ):
    return posZ == lowestZ or posZ == highZ

def isEdge(oxygen):
    position = oxygen.getPosition()
    return isXEdge(position[0]) or isYEdge(position[1]) or isZEdge(position[2])

def axisExist(oxyA, oxyB):
    for axis in axes:
        oxys = axis.getOxygens()
        if (oxyA == oxys[0] and oxyB == oxys[1]) or (oxyA == oxys[1] and oxyB == oxys[0]):
            return True
    return False

'''
Generate the Ghost Atom list for PBC
'''
ghosts = []
for oxy in oxygens:
    if isEdge(oxy):
        oxyPos = oxy.getPosition()
        posX = oxyPos[0]
        posY = oxyPos[1]
        posZ = oxyPos[2]
        if isXEdge(posX) and isYEdge(posY) and isZEdge(posZ):
            temp1 = posX + xHi if posX == lowestX else posX - xHi
            temp2 = posY + yHi if posY == lowestY else posY - yHi
            temp3 = posZ + zHi if posZ == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, temp2, temp3], oxy.getId(), len(ghosts) + 1000))
        elif isXEdge(posX) and isYEdge(posY):
            temp1 = posX + xHi if posX == lowestX else posX - xHi
            temp2 = posY + yHi if posY == lowestY else posY - yHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
        elif isXEdge(posX) and isZEdge(posZ):
            temp1 = posX + xHi if posX == lowestX else posX - xHi
            temp3 = posZ + zHi if posZ == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, posY, temp3], oxy.getId(), len(ghosts) + 1000))
        elif isYEdge(posY) and isZEdge(posZ):
            temp2 = posY + yHi if posY == lowestY else posY - yHi
            temp3 = posZ + zHi if posZ == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, temp3], oxy.getId(), len(ghosts) + 1000))
        elif isXEdge(posX):
            temp1 = posX + xHi if posX == lowestX else posX - xHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
        elif isYEdge(posY):
            temp2 = posY + yHi if posY == lowestY else posY - yHi
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
        elif isZEdge(posZ):
            temp3 = posZ + zHi if posZ == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            

#Loop through the oxygens
for i in range(len(oxygens)):
        
    #Loop through the real oxygens
    for j in range(len(oxygens)):
        if i != j:
            distance = math.dist(oxygens[i].getPosition(), oxygens[j].getPosition())
            if round(distance, 2) == 2.75:
                oxygens[i].addNeighbor(oxygens[j])
                if not axisExist(oxygens[i], oxygens[j]):
                    axes.append(Axis(oxygens[i], oxygens[j]))

    #Check if an oxygen is considered an edge
    if isEdge(oxygens[i]):
        #if oxygen is an edge, loop through the ghosts checking for the nearest ones
        for ghost in ghosts: 
            distance = round(math.dist(oxygens[i].getPosition(), ghost.getPosition()), 2)
            if distance == 2.75:
                oxygens[i].addNeighbor(ghost)
                axes.append(Axis(oxygens[i], ghost))
"""
Hydrogen Generation
Iterate through the Axis List for Hydrogen Generation
"""

#idenGhostOxy method
#Determines which oxygen in an axis is the ghost oxygen
#   Input: Axis to check
#   Output: 0 or 1
def idenGhostOxy(axis):
    if isinstance(axis.getOxygens()[0], GhostOxygen):
        return 0
    elif isinstance(axis.getOxygens()[1], GhostOxygen):
        return 1
    return -1


#isGhostAxis method
#Checks if an axis contains a ghostOxygen
#   Input: The axis
#   Output: True or False
def isGhostAxis(axis):
    return idenGhostOxy(axis) == 0 or idenGhostOxy(axis) == 1


#findAxis Method
#Method to find an axis with the reference oxygen a ghost atom points to
#   To find the specific axis, input: reference ID of the ghost atom's reference from the first axis
#                                     reference Id of the Oyxgen from the first axis
#       Using both references should allow identification of the exact axis that is a representation 
#               of the same axis across the periodic boundary. 
def findAxis(refId1, refId2):
    for i in range(len(axes)):
        if isGhostAxis(axes[i]):
            oxy1 = axis.getOxygens()[0]
            oxy2 = axis.getOxygens()[1]
            if oxy1.getId() == refId1 and oxy2.getRefO() == refId2:
                return i
            elif oxy2.getId() == refId1 and oxy1.getRefO() == refId2:
                return i
            else:
                return -1
#Generate the list of hydrogens
hydrogens = []

#Begin looping through the Axes
for axis in axes:
    if not axis.hasHydrogen():
        site = random.randint(1,2)
        if isGhostAxis(axis):
            ghost = None
            oxy = None
            if idenGhostOxy(axis) == 0:
                ghost = axis.getOxygens()[0]
                oxy = axis.getOxygens()[1]
            else:
                ghost = axis.getOxygens()[1]
                oxy = axis.getOxygens()[0]
            axis2= axes[findAxis(ghost.getRefO(), oxy.getId())]
            realSite1 = axis.getSiteRealId()
            realSite2 = axis2.getSiteRealId()
            realSite1Pos = axis.getSiteRealPosition()
            realSite2Pos = axis2.getSiteRealPosition()
            if realSite1 == -1 or realSite2 == -1 or realSite1Pos == [] or realSite2Pos == []:
                break
            if site == 1:
                hyd = Hydrogen(realSite1Pos)
                axis.addHydrogen(hyd, realSite1)
                axis.getOxygens()[realSite1 - 1].addChemBond(hyd)
                hydrogens.append(hyd)
                axis2.addGhostHyd()
            else:
                hyd = Hydrogen(realSite2Pos)
                axis2.addHydrogen(hyd, realSite2)
                axis2.getOxygens()[realSite2 - 1].addChemBond(hyd)
                hydrogens.append(hyd)
                axis.addGhostHyd()
        else:
            position = axis.getSitePosition(site)
            hyd = Hydrogen(position)
            axis.addHydrogen(hyd, site)
            axis.getOxygens()[site-1].addChemBond(hyd)
            hydrogens.append(hyd)

print("Number of axes = " + str(len(axes)))
print("Number of Oxygens = " + str(len(oxygens)))
print("Number of Hydrogens = " + str(len(hydrogens)))

"""
Monte Carlo Simulation 
to ensure the Coordination number of each Oxygen is exactly 2
"""



"""
Output
Write data output file
"""

#Generate the new file
file = open("ice_lattice_data2.lammps", "w")

#Calculate needed values:
totNumAtoms = numAtoms + len(hydrogens)
numAtomTypes += 1

##Calculate number of bonds
numBonds = 0
for oxy in oxygens:
    numBonds += oxy.getNumBonds()

##Calculate number of angles
numAngles = numBonds/2

#Add the header
file.write("LAMMPS data file generated by Python Script, timestep = 0\n\n")

#Add the beginning total numbers
file.write(str(216 + len(ghosts) + len((hydrogens))) + " atoms\n")
file.write(str(2) + " atom types\n\n")
#file.write(str(numBonds) + " bonds\n")
#file.write("1 bond types\n")
#file.write(str(numAngles) + " angles\n")
#file.write("1 angle types\n\n")

#Add the box dimensions
file.write(xlo + " " + xhi + " xlo xhi\n")
file.write(ylo + " " + yhi + " ylo yhi\n")
file.write(zlo + " " + zhi + " zlo zhi\n\n")

#Add Masses Section
file.write("Masses\n\n")
file.write("1 15.9994\n")
file.write("2 1.008\n\n")

#Add Atoms Section
file.write("Atoms # full\n\n")
count = 1
molCount = 1
for oxy in oxygens:
    oxyPos = oxy.getPosition()
    file.write("\t" + str(count) + "\t" + str(molCount) + "\t1\t-1.1128\t" + str(oxyPos[0]) + "\t" + str(oxyPos[1]) + "\t" + str(oxyPos[2]) + "\n")
    count += 1
    #'''
    for i in range(oxy.getNumBonds()):
        hPos = oxy.getChemBond(i).getPosition()
        file.write("\t" + str(count) + "\t" + str(molCount) + "\t2\t0.5564\t" + str(hPos[0]) + "\t" + str(hPos[1]) + "\t" + str(hPos[2]) + "\n")
        count += 1
    molCount += 1
    #'''
for oxy in ghosts:
    oxyPos = oxy.getPosition()
    file.write("\t" + str(count) + "\t" + str(molCount) + "\t1\t-1.1128\t" + str(oxyPos[0]) + "\t" + str(oxyPos[1]) + "\t" + str(oxyPos[2]) + "\n")
    count += 1


#Add Velocities Section
file.write("\nVelocities\n\n")
for i in range(216 + len(ghosts)+len(hydrogens)):
    file.write("\t" + str(i + 1) + "\t0\t0\t0\n")
'''
#Add Bonds Section
file.write("\nBonds\n\n")
bondId = 1
oxyId = 1
hydId = 2
for oxy in oxygens:
    for i in range(oxy.getNumBonds()):
        file.write("\t" + str(bondId) + "\t" + str(oxyId) + "\t" + str(hydId) + "\n")
        hydId += 1
        bondId += 1
    oxyId += 1

#Add Angles Section - add after Monte Carlo Simulation
file.write("\nAngles\n")
for oxy in oxygens:
'''

file.close()
