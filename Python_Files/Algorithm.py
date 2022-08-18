"""
Import Statements
"""
import Atom
import Axis
import Hydrogen
import Oxygen
import Site
import sys
import time

"""
Initial Input Pulling
Read information from data file
"""
if len(sys.argv) < 2:
    print("Usage: input the datafile containing the Oxygen Lattice")
    sys.exit(1)

print("This is the file: " + sys.argv[0])

print("The input file is: " + sys.argv[1])




"""
Axis Generation
Loop through the Oxygen Atoms list and find each neighbor
while generating the lists associated - the Axes and Sites
"""



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
