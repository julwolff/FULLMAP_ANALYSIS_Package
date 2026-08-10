#!/bin/bash
#SBATCH --account=project_2006015
#SBATCH --partition=medium
#SBATCH --time=03:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128

module purge
module load gcc/10.4.0 openmpi/4.1.5-cuda fftw/3.3.10-mpi cuda/12.1.1

export PATH="/projappl/project_2006015/julewolf/lammps/build:$PATH"
export LAMMPS_POTENTIALS=/projappl/project_2006015/julewolf/GRACE_potentials


# Might need this to help LAMMPS find FFTW and CUDA
export LD_LIBRARY_PATH=$FFTW_INSTALL_ROOT/lib:$CUDA_INSTALL_ROOT/lib64:$LD_LIBRARY_PATH

export OMP_NUM_THREADS=1

srun lmp -in in.npt #-k on g 1 -sf kk -pk kokkos #-v x 8 -v y 8 -v z 8

