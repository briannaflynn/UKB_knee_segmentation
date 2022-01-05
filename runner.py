#!/usr/bin/python
import os
import re
import subprocess
import sys
import argparse
import time
import logging
import logging.config
logger = logging.getLogger('main')
import datetime

#get current date and time
dateTime = datetime.datetime.now()
dateTimeStr = str(dateTime)
date = dateTimeStr[:10]
time = dateTimeStr[11:-7]
dt = date + "_" + time + ".log"

def run(a: list):
    args = None
    for j in a:
        args = ' '.join(a)

    return subprocess.run(args, shell=True, stdout=subprocess.PIPE)
    
def js(*args):
    b = os.path.abspath('./scripts/joint_space.py')
    trun = 'python ' + b
    cmd = [trun] + [*args] + ['> ./logfiles/js_' + dt]

    try:
        process = run(cmd)
    except subprocess.CalledProcessError:
        logger.error(f"Joint space crashed, here is stderr: {process.stderr}")
        raise
    return process.stdout
    
def ds(*args):
    b = os.path.abspath('./scripts/displacement.py')
    trun = 'python ' + b
    cmd = [trun] + [*args] + ['> ./logfiles/displacement_' + dt]

    try:
        process = run(cmd)
    except subprocess.CalledProcessError:
        logger.error(f"Displacement crashed, here is stderr: {process.stderr}")
        raise
    return process.stdout




##############################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repository for generating measurements from DXA image segmentation: AP knee")
    parser.add_argument('--path', action='store', type=str, required = True,
                        help='Path to directory with input files')
    parser.add_argument('--input_filename', action='store', type=str, required = True,
                        help='Path to text file containing list of files from the input directory for processing')
    parser.add_argument('--measure', action = 'store', type = str, required = True, 
    					help = 'What measurement to run - choices include: jointspace, displacement, or tibiofemoral. See README for details.')

    args = parser.parse_args()
    
    path = args.path
    input_filename = args.input_filename
    choice = args.measure
    
    if choice == "jointspace":
    	js(path, input_filename)
    elif choice == "displacement":
    	ds(path, input_filename)
    elif choice == "tibiofemoral":
    	tf(path, input_filename)
