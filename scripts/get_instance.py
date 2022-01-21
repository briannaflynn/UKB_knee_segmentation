#!/usr/bin/python

import pandas as pd
import sys

path = sys.argv[1] #example: "./"
type = sys.argv[2] #example: "left, right"
outname = path + type + "_i2i3_filter.csv"
inst = pd.read_csv(path + type + "_file_instance.csv")

i3 = inst.loc[inst['instance'] == 3][['eid', 'instance']]
i3 = i3.rename(columns = {'instance': 'instance_3'})
i2 = inst.loc[inst['instance'] == 2][['eid', 'instance']]
i2 = i2.rename(columns = {'instance': 'instance_2'})

i = i2.merge(i3, on = "eid")

df = inst[['file', 'eid']].merge(i, on = "eid")

data = df[['file']].merge(inst, on = "file")
print(data)
data.to_csv(outname, index = False)