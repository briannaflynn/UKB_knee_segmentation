#!/usr/bin/python

import pandas as pd
import sys

# r, rf, l, lf, rout, lout
r = pd.read_csv(sys.argv[1])
rf = pd.read_csv(sys.argv[2])

fi = [x[:-4] + "_prediction.png" for x in rf.file.to_list()]
rf['file'] = fi

l = pd.read_csv(sys.argv[3])
lf = pd.read_csv(sys.argv[4])

fi = [x[:-4] + "_prediction.png" for x in lf.file.to_list()]
lf['file'] = fi

rmerg = r.merge(rf, how = "inner", on = "file")
lmerg = l.merge(lf, how = "inner", on = "file")

print("right", r.shape[0], rf.shape[0], rmerg.shape[0])
print("left", l.shape[0], lf.shape[0], lmerg.shape[0]) 

rout = sys.argv[5] + "right_joint_space.csv"
lout = sys.argv[6] + "left_joint_space.csv"
rmerg.to_csv(rout, index=False)
lmerg.to_csv(lout, index=False)