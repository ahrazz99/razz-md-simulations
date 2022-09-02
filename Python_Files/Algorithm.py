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
print(" ... reading oxygen lattice input file... ")

initTime = round(time.time(), 3) * 1000

if len(sys.argv) < 2:
    print("Usage: input the datafile containing the Oxygen Lattice")
    sys.exit(1)

#Pull output file name if given. If not, follow default
outputFileName = "ice_lattice_1.lammps"
if len(sys.argv) == 3:
    outputFileName = sys.argv[2]

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
    oxygens.append(Oxygen([float(posX), float(posY), float(posZ)], i))
dataFile.close()

timeFileRead = round(time.time(), 3) * 1000
tFileReadReq = timeFileRead - initTime
print("*** Complete ***")
print("... time required: " + str(tFileReadReq) + " milliseconds\n\n\n")

"""
Axis Generation
Loop through the Oxygen Atoms list and find each neighbor
while generating the lists associated - the Axes and Sites
"""
print("... axis generation process begins ... ")

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
    return round(posX, 5) == lowestX or round(posX, 5) == highX

def isYEdge(posY):
    return round(posY, 5) == lowestY or round(posY, 5) == highY

def isZEdge(posZ):
    return round(posZ, 5) == lowestZ or round(posZ ,5) == highZ

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

print("\t... Ghost Atom  generation ...")
ghosts = []
for oxy in oxygens:
    if isEdge(oxy):
        oxyPos = oxy.getPosition()
        posX = oxyPos[0]
        posY = oxyPos[1]
        posZ = oxyPos[2]
        if isXEdge(posX) and isYEdge(posY) and isZEdge(posZ):
            temp1 = posX + xHi if round(posX, 5) == lowestX else posX - xHi
            temp2 = posY + yHi if round(posY, 5) == lowestY else posY - yHi
            temp3 = posZ + zHi if round(posZ, 5) == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, temp2, temp3], oxy.getId(), len(ghosts) + 1000))
        elif isXEdge(posX) and isYEdge(posY):
            temp1 = posX + xHi if round(posX, 5) == lowestX else posX - xHi
            temp2 = posY + yHi if round(posY, 5) == lowestY else posY - yHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
        elif isXEdge(posX) and isZEdge(posZ):
            temp1 = posX + xHi if round(posX, 5) == lowestX else posX - xHi
            temp3 = posZ + zHi if round(posZ, 5) == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([temp1, posY, temp3], oxy.getId(), len(ghosts) + 1000))
        elif isYEdge(posY) and isZEdge(posZ):
            temp2 = posY + yHi if round(posY, 5) == lowestY else posY - yHi
            temp3 = posZ + zHi if round(posZ, 5) == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))
            ghosts.append(GhostOxygen([posX, temp2, temp3], oxy.getId(), len(ghosts) + 1000))
        elif isXEdge(posX):
            temp1 = posX + xHi if round(posX, 5) == lowestX else posX - xHi
            ghosts.append(GhostOxygen([temp1, posY, posZ], oxy.getId(), len(ghosts) + 1000))
        elif isYEdge(posY):
            temp2 = posY + yHi if round(posY, 5) == lowestY else posY - yHi
            ghosts.append(GhostOxygen([posX, temp2, posZ], oxy.getId(), len(ghosts) + 1000))
        elif isZEdge(posZ):
            temp3 = posZ + zHi if round(posZ, 5) == lowestZ else posZ - zHi
            ghosts.append(GhostOxygen([posX, posY, temp3], oxy.getId(), len(ghosts) + 1000))


print("\t*** Ghost Atom Generation Complete***")
comGhostTime = 1000 * round(time.time(), 3)
ghostTime = comGhostTime - timeFileRead
print("\t\t time required: " + str(ghostTime) + " milliseconds\n")

print("\t...Axis Generation via List Iterations...")


#Loop through the oxygens
for i in range(len(oxygens)):
        
    #Loop through the real oxygens
    for j in range(len(oxygens)):
        if i != j:
            distance = math.dist(oxygens[i].getPosition(), oxygens[j].getPosition())
            if round(distance, 2) == 2.75:
                oxygens[i].addNeighbor(oxygens[j])
                if not axisExist(oxygens[i], oxygens[j]):
                    axes.append(Axis(oxygens[i], oxygens[j], False))
    #Check if an oxygen is considered an edge
    if isEdge(oxygens[i]):
        #if oxygen is an edge, loop through the ghosts checking for the nearest ones
        for ghost in ghosts: 
            distance = round(math.dist(oxygens[i].getPosition(), ghost.getPosition()), 2)
            if distance == 2.75:
                oxygens[i].addNeighbor(ghost)
                axes.append(Axis(oxygens[i], ghost, True))


print("\t***Axis Generation via List Iteration Complete***")
axisGenFin = 1000*round(time.time(), 3)
axisGenItTime = axisGenFin - comGhostTime
print("\t\t time required: " + str(axisGenItTime) + " milliseconds\n")
totAxisGenTime = axisGenFin - timeFileRead
print("***Axis Generation Complete***")
print("\ttime required: " + str(totAxisGenTime) + " milliseconds\n\n")


"""
Hydrogen Generation
Iterate through the Axis List for Hydrogen Generation
"""

#findAxis Method
#Method to find an axis with the reference oxygen a ghost atom points to
#   To find the specific axis, input: reference ID of the ghost atom's reference from the first axis
#                                     reference Id of the Oyxgen from the first axis
#       Using both references should allow identification of the exact axis that is a representation 
#               of the same axis across the periodic boundary. 
def findAxis(ghostParent, otherParent):
    #find the axes with GhostParent
    for i in range(len(axes)):
        if axes[i].isGhostAxis() and axes[i].getOxygens()[0] == ghostParent and oxygens[axes[i].getOxygens()[1].getRefO()] == otherParent:
            return i
    return -1


print("...Hydrogen Generation Algorithm Begins...")


#Generate the list of hydrogens
hydrogens = []

#Modified Axis list
modAxes = []

for i in range(len(axes)):
    #Check that if there is a Hydrogen in this axis. If there is, skip it. 
    if axes[i].hasHydrogen():
        continue
    else:
        #If the axis has no Ghost atom:
        if not axes[i].isGhostAxis():
            #Generate the random number for the site
            site = random.randint(1,2)

            #Pull the position of that site
            position = axes[i].getSitePosition(site)

            #Generate the hydrogen
            hyd = Hydrogen(position)

            #Add the hydrogen to the axis and as a bond
            axes[i].addHydrogen(hyd, site)
            axes[i].getOxygens()[site-1].addChemBond(hyd)

            #Add Hydrogen to the list of hydrogens
            hydrogens.append(hyd)

            #Add the now modified axis to the modAxes list
            modAxes.append(axes[i])

        #If the axis is a ghost axis
        else:
            #Find the corresponding axis across the periodic boundary
            index = findAxis(oxygens[axes[i].getOxygens()[1].getRefO()], axes[i].getOxygens()[0]) 
            if index == -1:
                break

            #Generate a random site number
            site = random.randint(1,2)
            
            #Find the position based on the site
            position = [0,0,0]
            if site == 1:
                position = axes[i].getSiteRealPosition()
            else:
                position = axes[index].getSiteRealPosition()

            #Generate the new hydrogen
            hyd = Hydrogen(position)

            #Add the hydrogen into the site corresponding to the nearest real atom on either axis
            if site == 1:
                axes[i].addHydrogen(hyd, 1)
                
                #Add the hydrogen as a chembond
                axes[i].getOxygens()[0].addChemBond(hyd)

                #Mark the site that didn't get the H as containing a ghost
                axes[index].addGhostHyd()
            else:
                #Repeat for if the site 2 is chosen
                axes[index].addHydrogen(hyd, 1)
                axes[index].getOxygens()[0].addChemBond(hyd)
                axes[i].addGhostHyd()

            #Add the hydrogen to the list
            hydrogens.append(hyd)
            
            #Modify the axis list by randomly removing one of the axis after connecting them

            ##connect the axes
            axes[i].addConnectedAxis(axes[index])
            axes[index].addConnectedAxis(axes[i])

            ##Generate number 1 or 2
            num = random.randint(1,2)

            ##If 1 add the first axis to modAxes, if 2 add the 2nd axis
            if num == 1:
                modAxes.append(axes[i])
            else:
                modAxes.append(axes[index])

hydGenTime = 1000 * round(time.time(), 3)
tothydGen = hydGenTime - axisGenFin
print("***Hydrogen Generation Complete***")
print("\ttime required: " + str(tothydGen) + " milliseconds\n")


"""
Monte Carlo Simulation 
to ensure the Coordination number of each Oxygen is exactly 2
"""

print("...Monte Carlo Simulation for Coordination Numbers Begin...")

#checkCoordNums method
#   Input: oxygens list
#   Output: True or False
# Checks every oxygen in the system to make sure their coordination numbers == 2
#   if any do not, return False. If all == 2, return true
def checkCoordNums(oxys):
    for oxy in oxys: 
        if oxy.getNumBonds() != 2:
            return False
    return True

def checkCoordNums(oxys):
    count = 0
    for oxy in oxys:
        if oxy.getNumBonds() == 2:
            count += 1
    if count == len(oxys):
        return True
    else:
        return False

#switchHydPos method
#   Input: the axis, the position of the hydrogen
#   Output: none
# switches the position of the hydrogen in the axis
def switchHydPos(axis, site):
    if not axis.isGhostAxis():
        #Pull the hydrogen out
        hyd = axis.getHydrogen(site)

        #Remove the hydrogen from the axis
        axis.delHydrogen(site)

        if site == 1:
            #Change the position of the hydrogen to its new position
            hyd.changePosition(axis.getSitePosition(2))

            #Add the hydrogen to the other site
            axis.addHydrogen(hyd, 2)

            #remove the hydrogen from the old oxygen's bond list
            axis.getOxygens()[0].delAtom(hyd)

            #add the hydrogen to the new oxygen's bond list
            axis.getOxygens()[1].addChemBond(hyd)
        else:
            hyd.changePosition(axis.getSitePosition(1))
            axis.addHydrogen(hyd, 1)
            axis.getOxygens()[1].delAtom(hyd)
            axis.getOxygens()[0].addChemBond(hyd)
    else:
        if site == 1:
            #pull the hydrogen out
            hyd = axis.getHydrogen(1)

            #change the position of the hydrogen to its new position
            hyd.changePosition(axis.getConnectedAxis().getSitePosition(1))
            
            #REmove the hydrogen from the axis
            axis.delHydrogens()

            #Remove the hydrogen from the old oxygen's bond list
            axis.getOxygens()[0].delAtom(hyd)

            #Remove the hydrogen from the other axis (the ghost hydrogen)
            axis.getConnectedAxis().delHydrogens()

            #add the hydrogen to the new site
            axis.getConnectedAxis().addHydrogen(hyd, 1)

            #Add the hydrogen to the new oxygen's bond list
            axis.getConnectedAxis().getOxygens()[0].addChemBond(hyd)

            #Add a ghost hydrogen to the other axis
            axis.addGhostHyd()
        else:
            hyd = axis.getConnectedAxis().getHydrogen(1)
            hyd.changePosition(axis.getSitePosition(1))
            axis.getConnectedAxis().delHydrogens()
            axis.getConnectedAxis().getOxygens()[0].delAtom(hyd)
            axis.delHydrogens()
            axis.addHydrogen(hyd, 1)
            axis.getOxygens()[0].addChemBond(hyd)
            axis.getConnectedAxis().addGhostHyd()

#Enter Loop while coord nums of any oxygen != 2
count = 0
while not checkCoordNums(oxygens):
    #Randomly choose an axis
    index = random.randint(0, len(modAxes) - 1)
    
    #Count the number of loop iterations for the Monte Carlo Algorithm
    count += 1
    if count % 100000 == 0:
        print("\tMonte Carlo Iterations: " + str(count))


    #if it is a not a ghost axis:
    if not modAxes[index].isGhostAxis():
        #pull the coordination numbers of the oxygens
        ci = modAxes[index].getOxygens()[0].getNumBonds()
        cj = modAxes[index].getOxygens()[1].getNumBonds()

        #pull the location of the hydrogen from the axis
        site = modAxes[index].getOccupiedSite()

        #calculate changes in coordination numbers should the hydrogen change positions
        ciMod = ci - 1 if site == 1 else ci + 1
        cjMod = cj + 1 if site == 1 else cj - 1

        #Attempt the change of the hydrogen if there is a position change of coordination numbers
        if abs(ciMod - cjMod) < abs(ci - cj):
            switchHydPos(modAxes[index], site)

        elif abs(ciMod - cjMod) == abs(ci - cj):
            swap = random.randint(1,2)
            if swap == 1:
                switchHydPos(modAxes[index], site)
    else:
        #If it is a ghost axis:
        #Pull the coordination numbers of the oxygens
        ci = modAxes[index].getOxygens()[0].getNumBonds()
        cj = modAxes[index].getConnectedAxis().getOxygens()[0].getNumBonds()
        
        #Determine which axis has the hydrogen axis 1 is the first axis, axis 2 is the connected axis
        site = 1 if modAxes[index].getOccupiedSite() != -1 else 2

        #calculate changes in coordination numbers should the hydrogen change positions
        ciMod = ci - 1 if site == 1 else ci + 1
        cjMod = cj + 1 if site == 1 else cj - 1

        #Attempt the change of the hdyrogen if there is a position change of coordinations numbers
        if abs(ciMod - cjMod) < abs(ci - cj):
            switchHydPos(modAxes[index], site)
        elif abs(ciMod - cjMod) == abs(ci - cj):
            swap = random.randint(1,2)
            if swap == 1:
                switchHydPos(modAxes[index], site)
print("Total Monte Carlo Iterations: " + str(count) + "\n")
print("***Monte Carlo Simulation Complete***")
mcSimTime = 1000*round(time.time(), 3)
mcSimTotal = mcSimTime - hydGenTime
numHours = mcSimTotal // 3600000
remainder = mcSimTotal % 3600000
numMin = remainder // 60000
remainder = remainder % 60000
numSec = remainder // 1000
numMSec = remainder % 1000
print("\ttime required: " + str(numHours) + " hours, " + str(numMin) + " min, " + str(numSec) + " sec, " + str(numMSec) + " ms\n")


"""
========================================================
Output
Write data output file
========================================================
"""

print("... Output File Generation Begins ... ")


#Generate the new file
file = open(outputFileName, "w")

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
file.write("LAMMPS data file generated by Python Script, timestep = 0, following V. Buch Algorithm\n\n")

#Add the beginning total numbers
file.write(str(len(oxygens) + len((hydrogens))) + " atoms\n")
file.write("2 atom types\n")
file.write(str(numBonds) + " bonds\n")
file.write("1 bond types\n")
file.write(str(numAngles) + " angles\n")
file.write("1 angle types\n\n")

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


#Add Velocities Section
file.write("\nVelocities\n\n")
for i in range(len(oxygens) + len(hydrogens)):
    file.write("\t" + str(i + 1) + "\t0\t0\t0\n")

#Add Bonds Section
file.write("\nBonds\n\n")
bondId = 1
oxyId = 1
hydId = 2
for oxy in oxygens:
    for i in range(oxy.getNumBonds()):
        file.write("\t" + str(bondId) + "\t1\t" + str(oxyId) + "\t" + str(hydId) + "\n")
        hydId += 1
        bondId += 1
    oxyId += 3
    hydId += 1

#Add Angles Section - add after Monte Carlo Simulation
file.write("\nAngles\n\n")
angleId = 1
oxyId = 1
hydId1 = 2
hydId2 = 3
for oxy in oxygens:
    file.write("\t" + str(angleId) + "\t1\t" + str(hydId1) + "\t" + str(oxyId) + "\t" + str(hydId2) + "\n")
    oxyId += 3
    hydId1 += 3
    hydId2 += 3
    angleId += 1

file.close()


fileGenTime = 1000 * round(time.time(), 3)
totGenTime = fileGenTime - mcSimTime
print("***Output File Generation Complete***")
print("\ttime required: " + str(totGenTime) + " milliseconds\n")

totalTime = fileGenTime - initTime
numHours = totalTime // 3600000
remainder = mcSimTotal % 3600000
numMin = remainder // 60000
remainder = remainder % 60000
numSec = remainder // 1000
numMSec = remainder % 1000
print("Algorithm Complete. Ice lattice output to " + outputFileName)
print("---Total Time Required: " + str(numHours) + " hours, " + str(numMin) + " min, " + str(numSec) + " sec, " + str(numMSec) + " ms\n")

