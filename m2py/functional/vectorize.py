#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""



def maplx_factory(function):
    """
    Example:

    >>> from m2py import functional as f
    >>>
    >>> def fun(a, b, c): return a**2 - 10*b + c
    ...
    >>>
    >>> fun_v = f.maplx_factory(fun)
    >>>
    >>> fun_v( [(0, 2, 4), (-3, 4, 8), (4, 2, 5), (22, -10, 23)] )
    [-16, -23, 1, 607]
    >>>
    >>> fun_v((0, 2, 4))
    -16
    >>> fun_v((-3, 4, 8))
    -23
    >>> fun_v((4, 2, 5))
    1
    """

    def f(x):
        if is_tuple(x):
            return function(*x)

        elif is_list(x):
            return maplx(function, x)
        raise Exception("Argument must be tuple or List")

    return f






def vectorize_juxt(funclist):
    """

    Example:

    >>> from m2py import functional as f
    >>>
    >>> f1 = lambda x: x**2 - 10.0
    >>> f2 = lambda x: 10*x + 8
    >>> f3 = lambda x: 100.0/x - 4
    >>>
    >>> x = [1, 2, 3, 4, 5]
    >>>
    >>>
    >>> fv= f.vectorize_juxt([f1, f2, f3])
    >>> fv(x)
    [[-9.0, -6.0, -1.0, 6.0, 15.0],
     [18, 28, 38, 48, 58],
     [96.0, 46.0, 29.333333333333336, 21.0, 16.0]]
    """
    f = lambda x: maplf(funclist, x)
    return f




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

    >>> from m2py import functional as f
    >>> import math
    >>>
    >>> sqrt = f.vectorize(math.sqrt)
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

def vectorize_var(function, variable, **constants):
    """
    Create a vectorized curried function

    :param function:  Function
    :param variable:  Variable symbol (str), free parameter
    :param constants: Constant parameters dictionary
    :return:          Curried function


    Example:
    Currying - Create a new function fun_x(x) from f(x)
    such that fun_x(x) = fun(x, y=2, z=3)

    >>> def fun(x, y, z): return x**2 - y*z
    ...
    >>> fun_vx = f.vectorize_var(fun, "x", y=2, z=3)
    >>>
    >>> fun_vx([2, 3, 4, 5, 7])
    [-2, 3, 10, 19, 43]
    >>>
    """
    fv  = currying(function, variable, **constants)
    fv =  vectorize(fv)
    return fv


def vectorize_dec():
    """
    Vectorize decorator

    Example:

    import functional as f

    @f.vectorize_dec()
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


def equalize(*args):
    """
    Similar to copy the non constants elemements
    of an spreadsheet to the other rows.

    x   y   z   w           x   y  z  w
    1   -2  8   6           1  -2  8  6
    2   -1                  2  -1  8  6
    3   0                   3   0  8  6
    4   1          ===>     4   1  8  6
    5   2                   5   2  8  6
    6   3                   6   3  8  6

    Example:

    >>> fp.equalize([1, 2, 3, 4, 5, 6], [-2, -1, 0, 1, 2, 3], 8, 6)
    [[1, 2, 3, 4, 5, 6],
     [-2, -1, 0, 1, 2, 3],
     [8, 8, 8, 8, 8, 8],
     [6, 6, 6, 6, 6, 6]]

    Note: I don't have a good name to this function yiet.
    """
    args = list(args)
    v = find(is_list, args)
    if v is not None:
        N = len(v)
        columns = mapif(is_num,  lambda x: duplicate(N, x), args)
    else:
        columns = args
    return columns

def vectorize_args(function):
    """
    Creates a new function that accepts
    array or number as input.
    This function is Useful for spreadsheet
    like numerical computations.


    Example:

    f(x , y , z, w) = x*y – 10*z + w

    x   y   z   w   f(x, y, z=8, w=6)
    1   -2  8   6   -76
    2   -1  8   6   -76
    3   0   8   6   -74
    4   1   8   6   -70
    5   2   8   6   -64
    6   3   8   6   -56


    >>> from m2py.functional import vectorize_args
    >>> x = [  1,  2, 3, 4, 5, 6 ]
    >>> y = [ -2, -1, 0, 1, 2, 3 ]
    >>> z = 8
    >>> w = 6
    >>>
    >>> def f(x, y, z, w): return x*y - 10*z + w
    ...
    >>>
    >>> mf = vectorize_args(f)
    >>>
    >>> mf(x, y, z, w)
    [-76, -76, -74, -70, -64, -56]
    >>>
    """
    def func(*args):
        columns =  equalize(*args)
        return maplx(function, list(zip(*columns)))

    return func
