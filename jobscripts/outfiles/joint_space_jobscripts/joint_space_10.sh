#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Frontera CLX nodes
#
#   *** MPI Job in Normal Queue ***
# 
# Last revised: 20 May 2019
#
# Notes:
#
#   -- Launch this script by executing
#      "sbatch clx.mpi.slurm" on a Frontera login node.
#
#   -- Use ibrun to launch MPI codes on TACC systems.
#      Do NOT use mpirun or mpiexec.
#
#   -- Max recommended MPI ranks per CLX node: 56
#      (start small, increase gradually).
#
#   -- If you're running out of memory, try running
#      fewer tasks per node to give each task more memory.
#
#----------------------------------------------------

#SBATCH -J js           # Job name
#SBATCH -o js.o%j       # Name of stdout output file
#SBATCH -e js.e%j       # Name of stderr error file
#SBATCH -p rtx          # Queue (partition) name
#SBATCH -N 2               # Total # of nodes 
#SBATCH -n 8              # Total # of mpi tasks
#SBATCH -t 12:30:00        # Run time (hh:mm:ss)

python /scratch1/05515/bflynn/UKB_knee_segmentation/joint_space_1.py /scratch1/05515/bflynn/knee/right_knee/predictions_right_knee/ 