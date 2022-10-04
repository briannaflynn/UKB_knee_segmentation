#!/bin/bash

#SBATCH -J left           # Job name
#SBATCH -o left.o%j       # Name of stdout output file
#SBATCH -e left.e%j       # Name of stderr error file
#SBATCH -p rtx          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes 
#SBATCH -n 1              # Total # of mpi tasks
#SBATCH -t 18:30:00        # Run time (hh:mm:ss)

mkdir -p $SCRATCH/CENTER_AXIS/
mkdir -p $SCRATCH/CENTER_AXIS/LEFT/
python ../scripts/femur_tibia_angle_centered.py $WORK2/knee_segmentation_predictions/left_knee_preds/ angle.txt
cd $WORK2/knee_segmentation_predictions/left_knee_preds/
mv *_center_axis_angle.png $SCRATCH/CENTER_AXIS/LEFT/
