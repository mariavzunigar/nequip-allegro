#!/bin/bash
#SBATCH --account paolucci_standard
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=48
#SBATCH --time=3-00:00:00
#SBATCH --partition=parallel
#SBATCH --mail-type=END
#SBATCH --mail-user=gdg4fh@virginia.edu

module purge
export MODULEPATH=/project/paolucci/apps/modulefiles:$MODULEPATH

module load ase
module load intel/18.0
module load intelmpi/18.0

module load vasp/6.3.0
unset VASP_SCRIPT
export VASP_COMMAND=/home/gdg4fh/important_files/setup_vasp6_gamma.sh

python spe_gamma.py 

echo "finish!"
