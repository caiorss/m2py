#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Type Detection Functions


"""
from constants import POSINF, NEGINF

try:
    from numpy import ndarray, isnan
except ImportError:
    pass

def is_list(var):
    """
    Test if variable var is list

    :return: True if var is list, False if var is not list
    :rtype:  bol
    """
    return isinstance(var, list)

def is_tuple(var):
    return isinstance(var, tuple)

def is_num(var):
    """
    Test if variable var is number (int or float)

    :return: True if var is number, False otherwise.
    :rtype:  bol
    """
    return isinstance(var, int) or isinstance(var, float)


def is_string(var):
    return isinstance(var, str)

def is_function(var):
    """
    Test if variable is function (has a __call__ attribute)

    :return: True if var is function, False otherwise.
    :rtype:  bol
    """
    return hasattr(var, '__call__')

def is_none(var):
    return var is None

def is_empty(lst):
    return len(lst) == 0

def is_ndarray(lst):
    return isinstance(ndarray, lst)

def is_nan(var):
    return isnan(var)

def is_posinf(x):
    return x >= POSINF

def is_neginf(x):
    return x <= NEGINF

def is_finite(x):
    return NEGINF < x < POSINF

def is_pos(x):
    return x > 0

def is_neg(x):
    return x < 0
