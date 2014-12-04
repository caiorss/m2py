#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

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

# eps constant
eps = spacing(1)

# plot(x, [y0, y1, y2]) ---> plotx(x, y1, y2, y3)
#
plotx = lambda x, yy: [plot(x, y) for y in yy]


#------------------------------------|
#  Trigonometric degree functions    |
#------------------------------------|



def deg2rad(deg):
    return deg * pi / 180

def rad2deg(rad):
    return rad / pi * 180

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


#######################################
#
#######################################

def powerise10(x):
    
    """ Returns x as a * 10 ^ b with 0<= a <10
    """
    if x == 0: return 0 , 0
    Neg = x <0
    if Neg : x = -x
    a = 1.0 * x / 10**(floor(log10(x)))
    b = int(floor(log10(x)))
    if Neg : a = -a
    return a ,b
    
def eng(x):
    """Return a string representing x in an engineer friendly notation"""
    a , b = powerise10(x)
    if -3<b<3: return "%.4g" % x
    a = a * 10**(b%3)
    b = b - b%3
    return "%.4g*10^%s" %(a,b)

__factors__ = { "10^-9": "p","10^-6": "u",  "10^-3": "m", "10^3": "k", "10^6": "M", "10^9": "G" }

def eng2(x):
    """Return a string representing x in an engineer friendly with prefix"""
    
    e = eng(x)
    base, factor = e.split("*")
    
    try:
        s= __factors__[factor]
        return "%s %s" % (base, s)
    except:
        return e


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
        columns = rows.next()
        data = dict.fromkeys(columns, [])
        
        for row in rows:
            for c, r in zip(columns, row):
                
                if dtype == "float":
                    r = float(r)
                    
                data[c].append(r)
        return data
