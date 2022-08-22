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
    oxygens.append(Oxygen([float(posX), float(posY), float(posZ)]))


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

#Loop through the oxygens
for i in range(20):
    
    #Loop through the oxygens
    for j in range(len(oxygens)):
        if i != j:
            #Pull the oxygen's position
            position = oxygens[i].getPosition()
            posX = round(position[0], 5)
            posY = round(position[1], 5)
            posZ = round(position[2], 5)

            #If the oxygen is in an edge, wrap around because of PBCs
            isEdgeX = posX == lowestX or posX == highX
            isEdgeY = posY == lowestY or posY == highY
            isEdgeZ = posZ == lowestZ or posZ == highZ

            isEdge = isEdgeX or isEdgeY or isEdgeZ
            
            #Calculate distance from i oxygen to j oxygen
            distance = math.dist(position, oxygens[j].getPosition())
            
            #Add the oxygen as a neighbor if close enough and generate the axis
            if round(distance, 5) == 2.75000:
                oxygens[i].addNeighbor(oxygens[j])
                axes.append(Axis(oxygens[i], oxygens[j]))
                continue

            #Check if the oxygen is an edge and treat it accordingly
            if isEdge:
                #generate a ghost oxygen for axis/hydrogen generation around the oxygen being studied
                print("Oxy " + str(i) + " is an edge")     
                ##Check if j oxygen is an edge
                positionJ = oxygens[j].getPosition()
                posX = round(positionJ[0], 5)
                posY = round(positionJ[1], 5)
                posZ = round(positionJ[2], 5)

                ##If the oxygen is in an edge, wrap around because of PBCs
                isJEdgeX = posX == lowestX or posX == highX
                isJEdgeY = posY == lowestY or posY == highY
                isJEdgeZ = posZ == lowestZ or posZ == highZ

                isJEdge = isJEdgeX or isJEdgeY or isJEdgeZ

                ##check which edges it is on and modify the position according
                if isJEdge:
                    print("oxy " + str(j) + " is an edge at ", end="")
                    if isEdgeX:
                        if posX == lowestX:
                            posX += xHi
                        else:
                            posX -= xHi
                        print("x, ", end="")

                    if isEdgeY:
                        if posY == lowestY:
                            posY += yHi
                        else:
                            posY -= yHi
                        print("y, ", end="")
                
                    if isEdgeZ: 
                        if posZ == lowestZ:
                            posZ += zHi
                        else:
                            posZ -= zHi
                        print("z, ")
                
                    ##Generate the ghost oxygen with the new coordinates
                    ghost = Oxygen([posX, posY, posZ])

                    ##Calculate distance between new ghost and the neighbors
                    distance = math.dist(ghost.getPosition(), oxygens[i].getPosition())
                    print("distance from oxy " + str(i) + " to oxy " + str(j) + " ghost = " + str(distance))
                    
                    ##If the distance between them is the correct value, add the 
                    if round(distance) == 2.75000:
                        oxygens[i].addNeighbor(ghost)
                        axes.append(Axis(oxygens[i], ghost))
                        

#for i in range(len(oxygens)):
 #   print("Oxygen " + str(i) + " has " + str(oxygens[i].getNumNeighbors()) + " neighbors")

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
