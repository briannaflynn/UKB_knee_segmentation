#!/bin/bash

#SBATCH -J right           # Job name
#SBATCH -o right.o%j       # Name of stdout output file
#SBATCH -e right.e%j       # Name of stderr error file
#SBATCH -p rtx          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes 
#SBATCH -n 1              # Total # of mpi tasks
#SBATCH -t 18:30:00        # Run time (hh:mm:ss)

mkdir -p $SCRATCH/CENTER_AXIS/
mkdir -p $SCRATCH/CENTER_AXIS/RIGHT/
python ../scripts/femur_tibia_angle_centered.py $WORK2/knee_segmentation_predictions/right_knee_preds/ angle.txt
cd $WORK2/knee_segmentation_predictions/right_knee_preds/
mv *_center_axis_angle.png $SCRATCH/CENTER_AXIS/RIGHT/
