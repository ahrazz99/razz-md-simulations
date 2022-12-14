# razz-md-simulations
LAMMPS Input Files and Python Code For Generation of a full System for Ion Rejection Testing. 

### Acknowledgements:
We greatly appreciate the assistance of Luo et al for providing their code for review and the advice they provided regarding setting up a Molecular Dynamic Simulation. 

# Description:
This repository is designed to provide all the necessary files and algorithms to generate a system of proton-disorder hexagonal ice in direct co-existance with a solution of H2O and NaCl to simulate the Ion Rejection phenomenon at the molecular level using the TIP4P/2005 Water Model. 

The system generation process follows first the algorithm provided by V. Buch et al for the generation of proton disordered hexagonal ice - the phase of ice found throughout nature on earth. Following the ice generation, the ice is then relaxed and melted to generate a system of liquid water with an  equivalent number of H2O molecules. The melted ice is then stacked next to each other to generate the desired size of the water system. Following the stacking and another equilibration, NaCl atoms are then added to the desired molarity and again equilibrated. Finally, the previously generated ice is stacked on the left end of the water system and the whole system is again equilibrated for the final system set-up. 

# The Procedure:
### Step 1: Oxygen Initialization
Input Files: Oxygen_lattice_generation.in

Description: 

This lammps input script designates the unit cell and then repeats that unit cell in the desired directions to generate a system of the desired size. The unit cell used in this case is a orthohombic unit cell of 8 Oxygens 2.75 angstroms apart

Output: Single Data File representing the Oxygen lattice with a .lammps format for visualization in OVITO 

### Step 2: V. Buch Algorithm

Input Files: prevDataFile.lammps, Algorithm.py, Atom.py, Axis.py, GhostOxygen.py, Hydrogen.py, Oxygen.py, Site.py
	
Description: 

This is a custom python program that uses the principles of Objected-Oriented Programming to add the Hydrogens to each Oxygen in a disordered manner using a Monte Carlo Simulation procedue.

Output: Single ice lattice with perfect angles and distances in a .lammps format.

### Step 3: Ice Equilibration

Input Files: ice_equilibration_1.in, ice_equilibration_2.in, ice_equilibration_3.in, python code output file
	
Description: 

This step equilibrates the ice to get to a energy equilibrium. This can be done in a single step or in multiple steps of various temperatures beginning at 0 K to the desired Temp (in K)

Output: equilibrated ice data files. 

### Step 4: Ice Melting

Input Files: ice_melting.in, previous equilibrated data file

Description: 

This lammps script performs a NVT simulation on the ice at 400 K to completely melt the system.

Output: Melted Ice data file

### Step 5: Simulation Box Expansion

Input Files: simulation_box_expansion.in

Description: 

This LAMMPS script expands the simulation box and equilibrates the new system in the center of the box. This step was found to be necessary before stacking to prevent loss of Hydrogen Atoms when the system was repeated. 

Output: expanded water box data file

### Step 6: Water System Stacking
	
Input Files: water_box_stacking.in

Description: 

This LAMMPS script expands the system by repeating the initial water box a desired number of times in the desired direction. 

Output: Larger water system

### Step 7: Water Equilibration

Input Files: water_equilibration.in

Description: 

This equilibrates the water system at 273 K to condense the whole system to the center of the simulation box. 273 K was chosen due to the melting point of the TIP4P/2005 model being found to be around 250 K, so 273 K is still in the liquid H2O phase region. 

Output: equilibrated water system

### Step 8: Salt Addition

Input Files: salt_addition.in

Description: 

This LAMMPS script adds the desired amount of Na and Cl atoms into the system, assigns thema charge, and equilibrates the system again to prevent any overlapping atomic interactions with the addition of the ions.

Output: NaCl System

### Step 9: Final System Set Up
Input Files: final_system_setup.in

Description: 

This LAMMPS script adds the Ice from step 3 to the NaCl solution from step 8 and does a final equilibration for the entire system. This is the final step, after this, further MD simulations may be performed and the results analyzed. 

Output: the final equilibrated system.


# References:

