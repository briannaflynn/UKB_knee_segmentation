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

#SBATCH -J knee_seg           # Job name
#SBATCH -o knee_seg.o%j       # Name of stdout output file
#SBATCH -e knee_seg.e%j       # Name of stderr error file
#SBATCH -p rtx          # Queue (partition) name
#SBATCH -N 2               # Total # of nodes 
#SBATCH -n 8              # Total # of mpi tasks
#SBATCH -t 12:30:00        # Run time (hh:mm:ss)

python /scratch1/05515/bflynn/seg_utils/deploy_segmentation.py /scratch1/05515/bflynn/knee/left_knee/padded_left_knee/ /scratch1/05515/bflynn/knee/left_knee/predictions_left_knee/ knee_segmentation.pkl 
