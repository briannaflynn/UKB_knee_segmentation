#!/usr/bin/python
import os
import re
import subprocess
import sys
import argparse
import time
import logging
import logging.config
#logging.config.fileConfig('logging.conf')
#logger = logging.getLogger('main')

def js(*args):
    b = os.path.abspath('joint_space.py')
    trun = 'python ' + b
    cmd = [trun] + [*args]

    try:
        process = run(cmd)
    except subprocess.CalledProcessError:
        logger.error(f"Joint space crashed, here is stderr: {process.stderr}")
        raise
    return process.stdout

##############################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repository for generating measurements from DXA image segmentation: AP knee")
    parser.add_argument('--path', action='store', type=str, required = True,
                        help='Path to directory with input files')
    parser.add_argument('--input_filename', action='store', type=str, required = True,
                        help='Path to text file containing list of files from the input directory for processing')

    args = parser.parse_args()
    
    path = args.path
    input_filename = args.input
    choice = args.measure
    
    if choice == "jointspace":
    	js(path, input_filename)
    elif choice == "displacement":
    	ds(path, input_filename)
    elif choice == "tibiofemoral":
    	tf(path, input_filename)
