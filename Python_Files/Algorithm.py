"""
Import Statements
"""
from Atom import Atom
from Axis import Axis
from Hydrogen import Hydrogen
from Oxygen import Oxygen
from Site import Site
import sys
import time
import math

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
xLo = round(float(xlo), 5)
xHi = round(float(xhi), 5)
yLo = round(float(ylo), 5)
yHi = round(float(yhi), 5)
zLo = round(float(zlo), 5)
zHi = round(float(zhi), 5)



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
    oxygens.append(Oxygen([round(float(posX),5), round(float(posY), 5), round(float(posZ), 5)]))


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

print("lowests: " + str(lowestX) + ", " + str(lowestY) + ", " + str(lowestZ))

numUnitCellsX = round(xHi / (2.75 * math.sqrt(8.0/3.0)), 5)
numUnitCellsY = round(yHi / (2.75 * math.sqrt(8.0)), 5)
numUnitCellsZ = round(zHi / (2.75 * (8.0/3.0)), 5)

highX = round(xHi - lowestX, 5)
highY = round(yHi - lowestY, 5)
highZ = round(zHi - lowestZ, 5)

print("highests: " + str(highX) + ", " + str(highY) + ", " + str(highZ))

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
        if isXEdge(posX):
            if posX == lowestX:
                posX += xHi
            else:
                posX -= xHi
        if isYEdge(posY):
            if posY == lowestY:
                posY += yHi
            else:
                posY -= yHi
        if isZEdge(posZ):
            if posZ == lowestZ:
                posZ += zHi
            else:
                posZ -= zHi
        ghosts.append(Oxygen([posX, posY, posZ]))

#Loop through the oxygens
for i in range(len(oxygens)):
        
    #Loop through the real oxygens
    for j in range(len(oxygens)):
        if i != j:
            distance = math.dist(oxygens[i].getPosition(), oxygens[j].getPosition())
            print("Distance from oxy 0 to oxy " + str(j) + " is: " + str(distance))
            if round(distance, 5) == 2.75000:
                oxygens[i].addNeighbor(oxygens[j])
                if not axisExist(oxygens[i], oxygens[j]):
                    axes.append(Axis(oxygens[i], oxygens[j]))

    #Check if an oxygen is considered an edge
    if isEdge(oxygens[i]):
        #if oxygen is an edge, loop through the ghosts checking for the nearest ones
        for ghost in ghosts:
            distance = math.dist(oxygens[i].getPosition(), ghost.getPosition())
            print("distance from oxy 0 to ghost atom is " + str(distance))
            if round(distance, 5) == 2.75000:
                oxygens[i].addNeighbor(ghost)
                axes.append(Axis(oxygens[i], ghost))

print("the number of ghost atoms: " + str(len(ghosts)))
print("the number of Axes is: " + str(len(axes)))
for i in range(len(oxygens)):
    print("oxygen " + str(i) + " has " + str(oxygens[i].getNumNeighbors()) + " neighbor oxygens")

"""
Hydrogen Generation
Iterate through the Axis List for Hydrogen Generation
"""




"""
Monte Carlo Simulation 
to ensure the Coordination number of each Oxygen is exactly 2
"""



"""
Output
Write data output file
"""
