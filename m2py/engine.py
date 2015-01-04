#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This module can be used to implement
a matlab like environment


"""
import os
import sys
from numpy.core.umath import spacing, tan
import numpy as np
import matplotlib as mp

import os
from datetime import datetime


from matplotlib.pylab import ion, plot, show, clf, figure
from numpy import array, sin, cos, log10, exp
from numpy import linspace, logspace, arange
# Numpy statistical functions
from numpy import std, var, mean, average, cov, corrcoef
from numpy import cumsum, cumprod, min, max, sum
from numpy import histogram

ion()

exit = sys.exit

system = os.system
abspath = os.path.abspath
joinpath = os.path.join

from numpy import *
from matplotlib.pylab import *

ion()

try:
    from linalg import inv, pinv, rank, eig
except:
    pass

__version__ = "0.1"



# plot(x, [y0, y1, y2]) ---> plotx(x, y1, y2, y3)
#
plotx = lambda x, yy: [plot(x, y) for y in yy]


#------------------------------------|
#  Trigonometric degree functions    |
#------------------------------------|



def sind(x):
    return sin(deg2rad(x))

def cosd(x):
    return cos(deg2rad(x))

def tand(x):
    return tan(deg2rad(x))



# Alias for arctan functions
atan  = arctan
atan2 = arctan2

def atand(x):
    return rad2deg(atan(x))

def atan2d(x, y):
    return rad2deg(atan2(x, y))





def read_csv_table(filename, dtype="float"):
    """
    Read table from csv file.
    The first line contains the header
    (sysmbols of columns). 
    
    Example:

        T,P,vf,vfg,vg,uf,ufg,
        0.01,0.6113,0.001
        5,0.8721,0.001,147
            
    """
    import csv
    
    with open(filename, "rb") as db:
        
        rows = csv.reader(db)
        
        # Read column names
        columns = next(rows)
        data = dict.fromkeys(columns, [])
        
        for row in rows:
            for c, r in zip(columns, row):
                
                if dtype == "float":
                    r = float(r)
                    
                data[c].append(r)
        return data
