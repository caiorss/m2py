#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Higher Order Functions
"""


import numpy

try:
    import _thread as thread
except ImportError:
    import _thread


#---------------------------#
#       CONSTANTS           #
#---------------------------#






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

    >>> from m2py import functional as f
    >>> fun = lambda x: x**2
    >>> f.mapl(fun, [1, 2, 3, 4, 5, 6])
    [1, 4, 9, 16, 25, 36]

    """
    return list(map(function, array))


def filterl(predicate, List):
    return list(filter(predicate, List))

def joinfuncs(funclist, array):
    """
    Map a list of functions to an array

    :param funclist: List of functions  [ f0, f1, f2 .. fk]
    :param array:    List of values     x= [ x0, x1, x2, ... xn]
    :return:         [map(f0, x), map(f1, x), ... map(fn, x)]


    juxt takes two or more functions and returns a function that returns
    a vector containing the results of applying each function on its
    arguments. In other words, ((juxt a b c) x) => [(a x) (b x) (c x)].
    This is useful whenever you want to represent the results of using 2
    different functions on the same argument(s), all at once rather than separately:

    Example:

    >>> from m2py import functional as f
    >>>
    >>> x = [1, 2, 3, 4, 5]
    >>> fun1 = lambda x: x**2 - 10.0
    >>> fun2 = lambda x: 10*x + 8
    >>> fun3 = lambda x: 100.0/x - 4
    >>> fun= [fun1, fun2, fun3 ]
    >>> f.joinfuncs(fun, x)
    [[-9.0, -6.0, -1.0, 6.0, 15.0],
     [18, 28, 38, 48, 58],
     [96.0, 46.0, 29.333333333333336, 21.0, 16.0]]


    Note: Function taken from cloujure and R
    https://clojuredocs.org/clojure.core/juxt
    """
    return [ list(map(fi, array)) for fi in funclist ]


def maplx(function, arglist):
    """
    Map list of tuples as function arguments

    :param function: Function of tuples
    :param arglist:  List of arguments of f
    :return:         list of results

    Let be
        function: f( a, b, c, d, ...)
        arglist :  [ (a0, b0, c0, ...), (ak, bk, ck, ...), ... ]

        Xk = [ ak, bk, ck, ... ]
        return [ f(X0), f(X1), ... f(Xn)]

    Example:

    >>> from m2py import functional as f
    >>>
    >>> x= [ (0, 2, 4), (-3, 4, 8), (4, 2, 5), (22, -10, 23)]
    >>>
    >>> def fun(a, b, c): return a**2 - 10*b + c
    ...
    >>>
    >>> f.maplx(fun, x)
    [-16, -23, 1, 607]
    """
    return list([function(*params) for params in arglist])


def zipl(*lists):
    """
    Equivalent to python2 zip, return a list instead
    of a generatory in python3
    """
    return list(zip(*lists))

def reduce(function, array):
    """
    Example:

    >>> from m2py import functional as f
    >>> >>> f.reduce(lambda a, b: a*b, [ 1, 2, 3, 4, 5])
    120
    >>>
    >>> f.reduce(lambda a, b: a+b, [ 1, 2, 3, 4, 5, 6, 7, 8])
    36
    >>>
    """

    y = array[0]

    for i in range(len(array)-1):
        #print("array = ", array)
        #print("y = ", y)
        y = function(y, array[i+1])

    return y


def mapif(condition, function, list):
    """

    """
    result = list.copy()

    for i, x in enumerate(list):

        if condition(x):
            result[i] = function(x)

    return result

def currying(function, variable, **constants):
    """
    :param function:  Function
    :param variable:  Variable symbol (str), free parameter
    :param constants: Constant parameters dictionary
    :return:          Curried function

    Example:

    Create a new function fun_x(x) from f(x)
    such that fun_x(x) = fun(x, y=2, z=3)

    >>> from m2py import functional as f
    >>>
    >>> def fun(x, y, z): return x**2 - y*z
    ...
    >>> fun_x = f.currying(fun, "x", y=2, z=3)
    >>> f.mapl(fun_x, [2, 3, 4, 5, 7])
    [-2, 3, 10, 19, 43]
    """

    params = constants

    def curried_function(x):
        params[variable] = x
        return function(**params)

    return curried_function



def compose(*funclist):
    """
    Returns the composition of a list of functions, where each function
    consumes the return value of the function that follows. In math terms,
    composing the functions f()

    :param funclist: List of functiosn [f0, f1, f2, f3, ... fn-1]
    :return:         New function f(x) = f0(f1(...fn-3(fn-2(fn-1(x))))
    :type funclist:  list(function)
    :rtype funclist: function

    Create f(x) such that

    f(x) = (f0.f1.f2...fn-1)(x)


    Example:

    Compute inc(double(10)) = 21

    >>>
    >>> imoort functional as f
    >>>
    >>> inc = lambda x: x+1
    >>> double = lambda x: x*2
    >>>
    >>> f.compose(inc, double)(10)
    21
    """
    flist = list(funclist)
    flist.reverse()

    def f(x):

        _x = x

        for f in flist:
            _x = f(_x)

        return _x

    return f


def zipwith(Combine, *Lists):
    """
    Combine the elements of two lists of equal length into one list.
    For each pair X, Y of list elements from the two lists, the element
    in the result list will be Combine(X, Y).

    zipwith(fun(X, Y) -> {X,Y} end, List1, List2) is equivalent to zip(List1, List2).

    Example:
    >>> from m2py.functional import zipwith
    >>>
    >>> f = lambda x, y, z: x**2+y**2 - z
    >>> zipwith(f, [1, 2, 3], [4, 5, 6], [3, 9, 8])
    [14, 20, 37]

    Note: Function taken from Erlang -
    http://erldocs.com/17.3/stdlib/lists.html#zipwith
    """
    return [Combine(*row) for row in zip(*Lists)]


def ifelse(condition, trueValue, falseValue):
    """
    :param condition:   Flag
    :param trueValue:   Return value if flag is True
    :param falseValue:  Return value if flag is False
    :type  condition:   Flag (bol value) True/False
    :return:            trueValue if condition is True, FalseValue otherwise

    Example:

    >>> from m2py import functional as f
    >>>
    >>> x = 3
    >>>
    >>> f.ifelse(x> 2, x**2, x-10)
    9
    >>> x= 1
    >>> f.ifelse(x> 2, x**2, x-10)
    -9
    >>> x= 2
    >>> f.ifelse(x> 2, x**2, x-10)
    -8
    >>>

    """
    return [falseValue, trueValue](condition)


def ifelsef(condition, trueFunction, falseFunction=identity):
    """
    :param condition:       Condition function
    :param trueFunction:    Function to be executed if condition is True
    :param falseFunction:   Function to be executed if condition is False
    :type condition:        function
    :type trueFunction:     function
    :type falseFunction:    function
    :return:                Conditional function

    Create a new function such that

    function(x):
     if condition(x):
        return trueFun(x)
     else
        return falseFun(x)

    Example:

    Crete
                /  x^2  , if x < 3
        f(x)  =
                \  x/3  , if x >= 3

    >>> from m2py import functional as f
    >>>
    >>> fx = f.ifelsef(lambda x: x<3, lambda x: x**2, lambda x: x/3.0)
    >>>
    >>> f.mapl(fx, [-3, -2, -1, 0, 1, 2, 3, 6, 9, 18, 27])
    [9, 4, 1, 0, 1, 4, 1.0, 2.0, 3.0, 6.0, 9.0]
    >>>
    >>> fx = f.ifelsef(lambda x: x<3, f.constant(0))
    >>> f.mapl(fx, [-3, -2, -1, 0, 1, 2, 3, 6, 9, 18, 27])
    [0, 0, 0, 0, 0, 0, 3, 6, 9, 18, 27]
    >>>
    """

    def func(x):
        return [falseFunction, trueFunction][condition(x)](x)

    return func



def nest(function, n):
    """
    fp::nest(f,n) returns the n-fold repeated composition of the function f.
    Thus, given the function f, fp::nest returns the identity function
    id if n is 0 and otherwise the function

    Return f(f(f(f..f(x))))

    Note: Function taken from Matlab Mupad DOC
    http://www.mathworks.com/help/symbolic/mupad_ref/fp-nest.html
    """

    def f(x):
        x_ = x
        for i in range(n):
            x_ = function(x_)

        return x_

    return f


def retry(call, tries, errors=Exception):
    for attempt in range(tries):
        try:
            return call()
        except errors:
            if attempt + 1 == tries:
                raise

def ignore(call, errors=Exception):
    try:
        return call()
    except errors:
        return None





def in_sequence(function_list):
    """
    Create a new function that execute the functions
    in the list in sequence.

    :param function_list: List of functions
    :return:              Function

    """
    def seqfun():
        for f in function_list: f()

    return seqfun

def in_parallel(function_list):
    """
    Create a new function that execute the functions
    in the list in parallel (thread)

    :param function_list: List of functions
    :return:              Function

    Example:

    >>> from m2py import functional as funcp
    >>>
    >>> import time
    >>>
    >>> def print_time(thname, delay):
    ...   for i in range(5):
    ...      time.sleep(delay)
    ...      print (thname, " ", time.ctime(time.time()))
    >>>
    >>> def make_print_time(name, delay): return lambda : print_time(name, delay)
    >>>
    >>> t1 = make_print_time("thread1", 1)
    >>> t2 = make_print_time("thread2", 2)
    >>> t3 = make_print_time("thread3", 3)
    >>> t4 = make_print_time("thread4", 4)
    >>>
    >>> thfun = funcp.in_parallel([t1, t2, t3, t4])
    >>> thfun()
    >>> thread1   Fri Dec 26 23:40:29 2014
    thread2   Fri Dec 26 23:40:30 2014
    thread1   Fri Dec 26 23:40:30 2014
    thread3   Fri Dec 26 23:40:31 2014
    thread1   Fri Dec 26 23:40:31 2014
    thread4   Fri Dec 26 23:40:32 2014
    thread2   Fri Dec 26 23:40:32 2014
    thread1   Fri Dec 26 23:40:32 2014
    thread1   Fri Dec 26 23:40:33 2014
    ...
    """

    def pfun():
        for func in function_list:
            _thread.start_new_thread( func, ())

    return pfun


def call(function, args=()):
    """
    :param function: Function object
    :pram argds:     Function arguments tuple

    In [11]: def f(x, y): return x+y

    In [12]: call(f, (20, 100))
    Out[12]: 120

    In [14]: def f2(): print("hello world")

    In [15]: call(f2)
    hello world


    """
    return function(*args)



def times(function, n):
    """
    Call a function n times

    :param function: Function without argument
    :pram  n:        Number of times to call
    :return:         [y0, y1, y2 ... ]

    for i in range(n):
        yi = function()

    Example:
    >>> fromn functional import ncall
    >>> from random import randint
    >>>
    >>> rnd= lambda : randint(0, 100)
    >>> f.times(rnd, 10)
    [84, 92, 31, 45, 32, 99, 38, 39, 89, 25]
    """
    return [function() for i in range(n)]




def groupby(function, sequence):
    """

    Example:

    >>> from m2py import functional as f
    >>> f.groupby(len, ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank'])
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}
    >>>
    >>>
    >>> f.groupby(f.is_even, [1, 2, 3, 4, 5, 6, 7])
    {False: [1, 3, 5, 7], True: [2, 4, 6]}
    >>>
    """

    output = {}

    for x in sequence:
        y = function(x)

        if not output.get(y):
            output[y] = [x]
        else:
            output[y].append(x)

    return output



def iterate(function, x):
    """
    Repeatedly apply a function func onto an original input
    Yields x, then func(x), then func(func(x)), then func(func(func(x))), etc..

    Example:


    Fixed point Iteration : The transcendental equation f(x) = 0 can be converted algebraically into the form x = g(x) and then using the iterative scheme with the recursive relation
    xi+1= g(xi),   i = 0, 1, 2, . . .,

    Find a root of  x^4-x-10 = 0                                [ Graph]
    Consider g1(x) = 10 / (x^3-1) and the fixed point
    let the initial guess x0 be 2.0

    >>> from m2py import functional as f
    >>>
    >>> itx = f.iterate(lambda x: 10.0/(x**3-10.0), 2)
    >>> # Repeat function calls and accumulate return value
    ...
    >>> x = f.times(itx, 10)
    >>> errx = f.diff(x)  # Calculate the differences  xi+1 - xi (error)
    >>>
    >>> f.disp(x, errx)
    -5           4.92593
    -0.0740741  -0.925885
    -0.999959    0.0908584
    -0.909101   -0.0210157
    -0.930117    0.00459003
    -0.925527   -0.00101653
    -0.926543    0.000224452
    -0.926319   -4.95924e-05
    -0.926368    1.09558e-05
    >>>
    >>> root = x[-1]
    >>> root
    -0.926357323308913
    >>>

    Souce: http://mat.iitm.ac.in/home/sryedida/public_html/caimna/transcendental/iteration%20methods/fixed-point/iteration.html
    """

    def iterf():
        y= function(iterf.x)
        iterf.x = y
        return y

    iterf.x = x

    return iterf


