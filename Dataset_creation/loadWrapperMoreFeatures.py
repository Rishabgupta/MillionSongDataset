import pandas as pd 
import numpy as np 
import hdf5_utils as HDF5
import hdf5_getters as g
import glob
import itertools
import collections
import sys

import LoadMSDMoreFeatures
import os


out_csv = 'files/moreFeatures.csv'
in_arg = sys.argv[1]
print(in_arg)
df = LoadMSDMoreFeatures.getData(int(in_arg))  
print('writing to df ' + in_arg + '.csv')
#df.to_csv('files/' + i + '.csv', sep=',')
df.to_csv(out_csv,header=False,index=True, mode='a')
