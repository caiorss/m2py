#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Matrix Manipulation Utilities
#
#


# Get column i, from a matrix: list of tuples or list
column = lambda m, i: [e[i] for e in m]
column.__doc__ = """
Get column i, from a matrix: list of tuples or list

            a  b  c
matrix = [ (1, 2, 3),
           (5, 6, 7),
           (9, 8, 7)]

Example:

>>> import m2py.matrix as m
>>> matrix = [ (1,2,3), (5,6,7), (9, 8, 7)]
>>>
>>> m.column(matrix, 0)
[1, 5, 9]
>>> m.column(matrix, 1)
[2, 6, 8]
>>> m.column(matrix, 2)
[3, 7, 7]
"""
import numpy
# Get Transpose Matrix
transpose = lambda M: list(zip(*M))

make_dict = lambda headers, columns: dict(list(zip(headers, columns)))


def __mapf__(f, x):
    if isinstance(x, list):
        return list(map(f, x))
    elif isinstance(x, numpy.ndarray):
        return numpy.array(list(map(f, x)))
    else:
        return f(x)


def vectf(function):
    """
    vectf - Vectorize one-variable function.
    to make it accept list as argument or a single
    number

    Example:

        >>> from m2py.misc.vectorize import vectf
        >>> from math import *
        >>> def f1(x): return exp(-x) -3*log(x)
        ...
        >>> fv = vectf(f1)
        >>>
        >>> fv(10)
        -6.907709879052375
        >>>
        >>> fv([1,2,3,4,5])
        [0.36787944117144233,
         -1.944106258443223,
         -3.246049797636465,
         -4.140567444470937,
         -4.821575790303215]
        >>>
        >>>
    """
    vectorized = lambda x: __mapf__(function, x)
    vectorized.__doc__ = function.__doc__
    return vectorized


def vectf2(function):
    """

    :param function:
    :return:

    >>> from m2py.misc import vectorize as m    >>> from math import *
    >>> def f(x, y, z):
    ...   return sqrt(x**2+y**2+z**2)
    ...
    >>>
    >>> fv = m.vectf2(f)
    >>>
    >>> fv([[1,23,5], [23, 49,5], [12,4,6]])
    [23.558437978779494, 54.35991169970753, 14.0]
    """
    vectorized = lambda rows: [function(*x) for x in rows]
    vectorized.__doc__ = function.__doc__

    return vectorized


def __mapfxy__(f, xx, yy):
    if isinstance(xx, list) and isinstance(yy, list):
        return [f(*z) for z in zip(xx,yy)]

    elif isinstance(xx, list):
        return [f(x, y=yy) for x in xx]

    elif isinstance(yy, list):
        return [f(x=xx, y=y) for y in yy]

    else:
        return f(xx, yy)

def vectxy(function):
    """
    :param function:
    :return:

    Example:

        >>> from m2py import vectorize as m
        >>> import math
        >>>
        >>> def f(x, y): return math.sqrt(x**2 + y**2)
        ...
        >>> ff= m.vectxy(f)
        >>>
        >>> ff([1, 3, 4], [3, 6, 10])
        [3.1622776601683795, 6.708203932499369, 10.770329614269007]
        >>>
        >>> ff([1, 8, 4], [3, 6, 10])
        [3.1622776601683795, 10.0, 10.770329614269007]
        >>>
        >>> ff(1, [3, 6, 10])
        [3.1622776601683795, 6.082762530298219, 10.04987562112089]
        >>>
        >>>
        >>> ff([3, 6, 10], 8)
        [8.54400374531753, 10.0, 12.806248474865697]
        >>>
        >>> ff(3, 4)
        5.0
        >>>
    """
    vectorized = lambda x, y: __mapfxy__(function, x, y)
    return vectorized

# import math
# def f(x, y): return math.sqrt(x ** 2 + y ** 2)
