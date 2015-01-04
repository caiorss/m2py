#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import roots
from . import numerical



def logbase(base):
    from math import log
    logbase_ = log(base)
    f = lambda x: log(x)/logbase_
    return f



def derivate(func, delta=1e-3):
    """
    Builds the derivate of a function
    """
    def derv_func(x):
        return (func(x+delta) - func(x))/delta
    return derv_func
