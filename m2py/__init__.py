#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Matlab functions and functionality implemented in Python


"""

# __all__ = [ "units",
#             "constants", "disp", "lag", "diff", "growth", "signum","vectorizer", "vectorize", "maxdiff",
#             "transpose", "unitfactor",
#
#            "spacing", "tan", "arctan", "arcsin", "arccos", "sin", "cos", "log", "exp"
#            "log10", "linspace", "logspace", "arange", "floor", "ceil"]

# from thermo import xsteam
#from prefnum import prefnum
from .misc import units
from .misc import constants
from .utils import is_num, is_list, is_dict, is_tuple

import numpy as np
from numpy.core.umath import spacing, tan, arctan, arcsin, arccos, arctan2, floor, ceil
from numpy.core.umath import sin, cos, log, log10, exp
from numpy import linspace, logspace, arange

try:
    from linalg import inv, pinv, rank, eig
except:
    pass

unitfactor = units.factor

# eps constant
EPS = spacing(1)
eps = EPS
PI = 3.141592653589793
E = 2.7182818284590451  # Euler's number exp(1)
SQRT2 = 1.4142135623730951  # sqrt(2)
SQRT1_2 = 0.70710678118654757  # sqrt(1/2)
SQRT_PI = 1.7724538509055159  # sqrt(pi)
LN2 = 0.69314718055994529  # ln(2)
LN10 = 2.3025850929940459  # ln(10)
POSINF = 1e200  # Negative Infinite number
NEGINF = -1e200  # Positive infinite number


def is_finite(x):
    return NEGINF < x < POSINF


def is_pos(x):
    return x > 0


def is_neg(x):
    return x < 0


def is_ndarray(lst):
    return isinstance(numpy.ndarray, lst)


def is_nan(var):
    return numpy.isnan(var)


def is_posinf(x):
    return x >= POSINF


def is_neginf(x):
    return x <= NEGINF


def addl(list2, list1):
    return [(b + a) for a, b in zip(list2, list1)]


def difl(list2, list1):
    return [(b - a) for b, a in zip(list2, list1)]


def mull(list2, list1):
    return [(b * a) for b, a in zip(list2, list1)]


def divl(list2, list1):
    return [(b / a) for b, a in zip(list2, list1)]


def transpose(matrix):
    return list(zip(*matrix))


def mapl(function, array):
    """
    Map a function to an array
    (equivalent to python2 map)

    :param function: Function to be mapped
    :param array:    List of values
    :return:         List of returns values

    f = function
    array = [x0, x1, x2, ... xn]
    [f(x0), f(x1), f(x2) ... f(xn)] = mapl(f, array)

    Example:

    >>> fun = lambda x: x**2
    >>> mapl(fun, [1, 2, 3, 4, 5, 6])
    [1, 4, 9, 16, 25, 36]

    """
    return list(map(function, array))


try:
    from tabulate import tabulate
except:
    print("Couldn't import tabulate module")


def disp(*params, **options):
    """
    Function To Display Numpy Matrix
    on terminal in a nice way.

    Requires tabulate module

    Example:

    >>> import pyhof as f
    >>> x = [0.0, 0.1, 0.2, 0.4, 0.5, 0.8, 1.0]
    >>> y = [0.3, 0.6, 0.7, 0.7, 0.9, 1.0, 1.0]
    >>>
    >>> disp(x,y)
    0    0.3
    0.1  0.6
    0.2  0.7
    0.4  0.7
    0.5  0.9
    0.8  1
    1    1
    >>>
    >>>
    >>> disp((x, y))
    0    0.3
    0.1  0.6
    0.2  0.7
    0.4  0.7
    0.5  0.9
    0.8  1
    1    1
    >>>
    >>>
    >>>
    >>> disp((x, y), headers=["x", "y"])
      x    y
    0    0.3
    0.1  0.6
    0.2  0.7
    0.4  0.7
    0.5  0.9
    0.8  1
    1    1
    """
    from tabulate import tabulate

    headers = options.get("headers", "")
    tablefmt = options.get("tablefmt", "plain")

    if not params:
        return

    if len(params) == 1:
        if isinstance(params, list) or isinstance(params[0], tuple):
            out = zip(*params[0])
            #print tabulate(zip(*params[0]), headers=headers)

        else:
            #print tabulate(map(lambda x: [x], map(float, params[0])), headers=headers)
            out = map(lambda x: [x], map(float, params[0]))
    else:
        out = zip(*params)
        #print tabulate(zip(*params), headers=headers)

    print(tabulate(out, headers=headers, tablefmt=tablefmt))


def lag(array, n=1):
    """
    >>> x = [19, 100, 36, 6, 100, 20, 75, 66, 98, 55]
    >>> lag(x)
    [100, 36, 6, 100, 20, 75, 66, 98, 55]
    >>> lag(x, 2)
    [36, 6, 100, 20, 75, 66, 98, 55]
    """
    return array[n:]


def diff(array, n=1):
    """
    diff(x) = lag(x, 1) -  x

    Let the array be called x

    x = [x0, x1, x2, x3 .., xn]
    diff(x, 1) = [x1 - x0, x2 - x1, x3 - x2, ... xn - xn-1]
    diff(x, k) = [xk - xk-1, xk+2 - xk+1, ...]


    Example1:

    >>> x = [19, 100, 36, 6, 100, 20, 75, 66, 98, 55]
    >>> diff(x)
    [81, -64, -30, 94, -80, 55, -9, 32, -43]


    Example2:

    >>> x = [0.0, 0.1, 0.2, 0.4, 0.5, 0.8, 1.0]
    >>> y = [0.3, 0.6, 0.7, 0.7, 0.9, 1.0, 1.0]
    >>>
    >>> dx = diff(x)
    >>> dy = diff(y)
    >>> slopes = divl(dy, dx)
    >>>
    >>> disp(dx, dy, slopes, headers=["dx", "dy", "slopes"])
      dx    dy    slopes
     0.1   0.3  3
     0.1   0.1  1
     0.2   0    0
     0.1   0.2  2
     0.3   0.1  0.333333
     0.2   0    0
    >>>
    """
    return difl(array[n:], array)


def growth(array):
    """
    Builds a growth Sequence of an array
    This function can be useful to financial
    analysis.

    :param array: List of numbers
    :return:      Growth of sequence

    x = [x0, x1, x2, x3 .., xn]

    growth(x) =  [ (x1-x0)/x0, (x2-x1)/x1, .... (xn - xn-1)/xn-1 ]

    Example:


    >>> x = [19, 100, 36, 6, 100, 20, 75, 66, 98, 55]
     >>> growth(x)
    [4.2631578947368425,
     -0.64,
     -0.8333333333333334,
     15.666666666666666,
     -0.8,
     2.75,
     -0.12,
     0.48484848484848486,
     -0.4387755102040816]

    """
    df_array = difl(array[1:], array)
    return divl(df_array, array)


def maxdiff(array1, array2):
    """
    Return the maximum difference between array 1 and array2
    max(array1[i] - array2[i])

    """
    df = mapl(abs, difl(array2, array1))
    return max(df)


def vectorize(function):
    """
    :param function: Function to be vectorized
    :return:         Vectorized function

    Create new function y= vf(x), such that:

    y = f(x)

        /  map(f, x)  if x is list
    vf =
        \  f(x)       if x is not list

    Example:

    >>> import math
    >>>
    >>> sqrt = vectorize(math.sqrt)
    >>> sqrt(2)
    1.4142135623730951
    >>>
    >>> sqrt([1, 2, 3, 4, 5])
    [1.0, 1.4142135623730951, 1.7320508075688772, 2.0, 2.23606797749979]
    """

    def vectorized_function(x):
        if isinstance(x, list):
            return list(map(function, x))
        return function(x)

    return vectorized_function


def vectorizer():
    """
    Vectorize decorator

    Example:

    import functional as f

    @vectorizer()
    def signum(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    >>> signum([1, 2, -23, 0, -4.23, 23])
    [1, 1, -1, 0, -1, 1]
    >>>
    >>> signum(10)
    1
    >>> signum(-10)
    -1
    >>> signum(0)
    0
    >>>
    """
    import functools

    def wrap(f):
        @functools.wraps(f)
        def wrapper(x):
            if is_list(x):
                return list(map(f, x))
            else:
                return f(x)

        return wrapper

    return wrap


@vectorizer()
def signum(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def product(list):
    """
    Returns a product of a List

    :param list:
    :return:
    """

    prod = 1
    for e in list:
        prod = prod * e
    return prod


def dotproduct(vector1, vector2):
    """
    Dot Product between two lists (vectors)

    :param vector1:
    :param vector2:
    :return:
    """
    return sum(mull(vector1, vector2))


@vectorizer()
def topct(x):
    """
    Convert Decimal Fraction to percent
    
   
    >>> topct([0.01, 0.023, 0.80, -0.23, 1.0])
    [1.0, 2.3, 80.0, -23.0, 100.0]
    >>> 
    """
    return 100.0 * x


@vectorizer()
def fmtpct(x):
    """
    Format sequence to percent
    
    >>> 
    >>> fmtpct(([1.0, 2.3, 80.0, -23.0, 100.0]))
    ['1.00%', '2.30%', '80.00%', '-23.00%', '100.00%']
    >>>     
    """
    return "%.2f%%" % (100.0 * x)


@vectorizer()
def frompct(x):
    """
    Convert Percent values to Decimal fraction

   
    >>> frompct([1.0, 2.3, 80.0, -23.0, 100.0])
    [0.01, 0.023, 0.8, -0.23, 1.0]
    """
    return x / 100.0


def sort_tuple_list(lst, col):
    """
    :param lst: List of tuples
    :param col: Column number of tuple

    Example:

    x = [
    ("Person 1",10),
    ("Person 2",8),
    ("Person 3",12),
    ("Person 4",20)]

    In [21]: sort_tuple_list(x, 1)
    Out[21]: [('Person 2', 8), ('Person 1', 10), ('Person 3', 12), ('Person 4', 20)]

    In [22]: sort_tuple_list(x, 0)
    Out[22]: [('Person 1', 10), ('Person 2', 8), ('Person 3', 12), ('Person 4', 20)]
    """
    import operator

    if is_tuple(lst):
        lst_ = list(lst)
    else:
        lst_ = lst.copy()

    lst_.sort(key=operator.itemgetter(col))
    return lst_


def get_column(matrix, column):
    """
    Get the column of a matrix ( List ) composed
    of list or tuple that represents each row of
    a matrix.

    :param matrix:  List cotaining [ row0, row1, ... rown]  where row_i = [ ai0, ai1, ai2, ... ain]
    :param column:  Column number ( Example: k to get column k)
    :return:        Column k or  [ a0k, a1k, a2k, ... aMk ]

    Example:

    x   y   z
    5   43  83
    52  99  70
    78  27  86
    26  84  49
        
    
    Represented as:
       
    [ 
    (x0, y0, z0),
    (x1, y2, z1),
    (x2, y2, z2),
    ...
    (xn, yn, zn)
    ]
    
    [(5,  43, 83),
     (52, 99, 70),
     (78, 27, 86),
     (26, 84, 49),]
    
    Each List
    >>> M = [(5.0, 52.0, 78.0, 26.0), (43.0, 99.0, 27.0, 84.0), (83.0, 70.0, 86.0, 49.0)]
    >>> get_column(M, 0)
    [5.0, 43.0, 83.0]
    >>> get_column(M, 1)
    [52.0, 99.0, 70.0]
    >>> get_column(M, 2)
    [78.0, 27.0, 86.0]
    >>> get_column(M, 3)
    [26.0, 84.0, 49.0]

    """

    return list(map(lambda e: e[column], matrix))


def sort_matrix_by_column(matrix, column):
    """
    :param matrix:  List cotaining [ row0, row1, ... rown]  where row_i = [ ai0, ai1, ai2, ... ain]
    :param column:  Column number ( Example: k to get column k)
    :return:        Column k or  [ a0k, a1k, a2k, ... aMk ]
    """
    sorted_ = sort_tuple_list(list(zip(*matrix)), column)
    return list(zip(*sorted_))


def deg2rad(deg):
    """
    :param deg: Angle in Degrees
    :return:    Angle in Radians
    """
    return deg * PI / 180


def rad2deg(rad):
    """
    :param rad: Angle in Radians
    :return:    Angle in Degrees
    """
    return rad / PI * 180


def sind(x):
    return sin(deg2rad(x))


def cosd(x):
    return cos(deg2rad(x))


def tand(x):
    return tan(deg2rad(x))


# Alias for arctan functions
atan = arctan
atan2 = arctan2



def atand(x):
    return rad2deg(atan(x))


def atan2d(x, y):
    return rad2deg(atan2(x, y))


def cummulated_function(function, array, init=0):

    result = []
    acc = init    # Accumulator

    for e in array:

        acc = function(acc, e)
        result.append(acc)

    return result

def cumsum(array):
    """
    Cummulated Sum

    :param array: A list of scalar
    :return:
    """
    return cummulated_function(lambda x, y: x+y, array, 0)

def cumprod(array):
    """
    Cummulated Sum

    :param array: A list of scalar
    :return:
    """
    return cummulated_function(lambda x, y: x*y, array, 1)



def __powerise10(x):

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
    """
    Return a string representing x in an engineer friendly notation

    """
    a , b = __powerise10(x)
    if -3<b<3: return "%.4g" % x
    a = a * 10**(b%3)
    b = b - b%3
    return "%.4g*10^%s" %(a,b)

__factors__ = { "10^-9": "p","10^-6": "u",  "10^-3": "m", "10^3": "k", "10^6": "M", "10^9": "G" }

def eng2(x):
    """
    Return a string representing x in an engineer friendly with prefix

    """

    e = eng(x)
    base, factor = e.split("*")

    try:
        s= __factors__[factor]
        return "%s %s" % (base, s)
    except:
        return e