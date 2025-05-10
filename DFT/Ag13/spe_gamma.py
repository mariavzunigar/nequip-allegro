from ase.build import bulk
from ase.io import read
from ase.calculators.vasp.vasp2 import Vasp2
import os
from shutil import copyfile

cwd = os.getcwd()

bootstrap = {'ediff': [1e-4, 1e-6],
             'ediffg': [-0.08, -0.04]}

atoms = read('POSCAR')

for i in range(2):
    vasp_directory = str(bootstrap['ediff'][i]) + '_' + str(bootstrap['ediffg'][i])
    
    # Create a directory for this set of calculations
    if not os.path.exists(cwd + '/' + vasp_directory):
        os.mkdir(cwd + '/' + vasp_directory)
    
    # Change to the directory where this VASP calculation will be performed
    os.chdir(cwd + '/' + vasp_directory)
    
    # Setup and run VASP calculation in the specific directory
    calc = Vasp2(xc='pbe',
                 kpts=[1, 1, 1],
                 encut=400,  # enmax=230
                 ediff=bootstrap['ediff'][i],
                 ediffg=bootstrap['ediffg'][i],
                 lreal='Auto',
                 prec='Accurate',
                 ismear=0,
                 sigma=0.2,  # default
                 # isif = 2,
                 # idipol = 4,
                 ibrion=-1,  # ions are not moved
                 nsw=0,  # nmax number of ionic steps
                 lwave=False,  # Don't write WAVECAR
                 lcharg=False,  # Don't write CHGCAR
                 lscalapack=False,
                 )

    atoms.set_calculator(calc)
    print(atoms.get_potential_energy())
    
    # After the first iteration, copy relevant files to the next folder
    if i == 1:
        previous_vasp_directory = cwd + '/' + str(bootstrap['ediff'][i - 1]) + '_' + str(bootstrap['ediffg'][i - 1])
        current_vasp_directory = cwd + '/' + vasp_directory
        
        # Copy CONTCAR from the previous calculation as the starting POSCAR for the next
        if os.path.exists(previous_vasp_directory + '/CONTCAR'):
            copyfile(previous_vasp_directory + '/CONTCAR', current_vasp_directory + '/POSCAR')
        else:
            print(f"Warning: {previous_vasp_directory}/CONTCAR not found, skipping copy operation.")

    # Return to the original working directory
    os.chdir(cwd)

