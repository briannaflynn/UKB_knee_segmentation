#!/usr/bin/python

import pandas as pd
import sys

right = pd.read_csv(sys.argv[1])
left = pd.read_csv(sys.argv[2])

rif = pd.read_csv('../data/right_file_instance.csv')
lif = pd.read_csv('../data/left_file_instance.csv')

rif['file'] = rif['file'].str.replace('.jpg', '_prediction.png')
lif['file'] = lif['file'].str.replace('.jpg', '_prediction.png')

cols = [col for col in left.columns if '_av_norm' in col]
cols.append('file')

right = right[cols]
left = left[cols]

right = right.merge(rif, on = 'file')
print(right)
left = left.merge(lif, on = 'file')
print(left)

outpath = '../data/'
# p = outpath.split("/")
# outfile = p[-1]
outfile = "gwas_formatted.csv"
print(outfile)
outpath = outpath.replace(outfile, "")
right_name = outpath + "right_" + outfile
left_name = outpath + "left_" + outfile

right.to_csv(right_name, index = False)
left.to_csv(left_name, index = False)