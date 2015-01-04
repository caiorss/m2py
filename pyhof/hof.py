#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Higher Order Functions
"""


import numpy
from .check import is_tuple, is_list, is_num, is_dict

try:
    import _thread as thread
except ImportError:
    import _thread


#---------------------------#
#      PRIMITIVES           #
#---------------------------#



def identity(x):
    return x

def constantly(value):
    """
    Creates a function that returns the same value that is used
    as the argument of

    >>> import function as f
    >>> std_gravity = f.constantly(9.81) # m/s2
    >>> std_gravity(2)
    9.81
    """
    def f(x):
        return value

    return f

def nope():
    pass

def contains(lst, value):
    return value in lst





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



def starmap(function, arglist):
    """
    map tuple
    
    Map list of function arguments to the function

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


def mapif(predicate, function, list):
    """

    """
    result = list.copy()

    for i, x in enumerate(list):

        if predicate(x):
            result[i] = function(x)

    return result



def joinf(funclist):
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
    def joined_functions(x):
        return [ f(x) for f in funclist ]
    
    return joined_functions
    #return [ list(map(fi, array)) for fi in funclist ]


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


def pipe(*funclist):
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

    def f(x):

        _x = x

        for f in funclist:
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
    >>> from m2py.functional.hof import zipwith
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
    return [falseValue, trueValue][condition]


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
            thread.start_new_thread( func, ())

    return pfun


def caller(function, args=(), kwargs=None):
    """
    :param function: Function object
    :pram argds:     Function arguments tuple

    In [11]: def f(x, y): return x+y

    In [12]: call(f, (20, 100))()
    Out[12]: 120

    In [14]: def f2(): print("hello world")

    In [15]: call(f2)
    hello world
    """
    if not kwargs:
        kwargs = {}
    return lambda : function(*args, **kwargs)


def call(function, args=(), kwargs=None):
    if not kwargs:
        kwargs = {}
    return function(*args, **kwargs)


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
    for i in range(n):
        function()




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


def addl(list2, list1):
    return [ (b+a) for a, b in zip(list2, list1)]

def difl(list2, list1):
    return [ (b-a) for b, a in zip(list2, list1)]

def mull(list2, list1):
    return [ (b*a) for b, a in zip(list2, list1)]

def divl(list2, list1):
    return [ (b/a) for b, a in zip(list2, list1)]


def sliding_window(array, k):
    """
    A sequence of overlapping subsequences

    Example:

    >>> from m2py import functional as f
    >>>
    >>> x = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9']
    >>>
    >>> print(f.sliding_window(x, 1))
    [('x0',), ('x1',), ('x2',), ('x3',), ('x4',), ('x5',), ('x6',), ('x7',), ('x8',), ('x9',)]
    >>>
    >>> print(f.sliding_window(x, 2))
    [('x0', 'x1'), ('x1', 'x2'), ('x2', 'x3'), ('x3', 'x4'), ('x4', 'x5'), ('x5', 'x6'), ('x6', 'x7'), ('x7', 'x8'), ('x8', 'x9')]
    >>>
    >>> print(f.sliding_window(x, 3))
    [('x0', 'x1', 'x2'), ('x1', 'x2', 'x3'), ('x2', 'x3', 'x4'), ('x3', 'x4', 'x5'), ('x4', 'x5', 'x6'), ('x5', 'x6', 'x7'), ('x6', 'x7', 'x8'), ('x7', 'x8', 'x9')]
    >>>

    Note: http://toolz.readthedocs.org/en/latest/api.html#toolz.itertoolz.sliding_window
    """
    return list(zip(*[ array[i:] for i in range(k)]))

def dictzip(keys, values):
    """
    >>> dictzip(["x", "y", "z"], [1, 2,3])
    {'y': 2, 'x': 1, 'z': 3}
    """
    return dict(list(zip(keys, values)))


def transpose(matrix):
    return list(zip(*matrix))

def unzip_l(matrix):
    return list(zip(*matrix))


def find(predicate, array):
    """
    find_.find(list, predicate, [context]) Alias: detect
    Looks through each value in the list, returning the first one that
    passes a truth test (predicate), or undefined if no value passes the
    test. The function returns as soon as it finds an acceptable element,
    and doesn't traverse the entire list.

    var even = _.find([1, 2, 3, 4, 5, 6], function(num){ return num % 2 == 0; });
    => 2
    """
    for x in array:
        if predicate(x):
            return x
    return None


def find_index(predicate, List):
    """
    (a → Boolean) → [a] → [Number]

    Return the index of first element that satisfy the 
    predicate
    """
    for i, x in enumerate(List):
        if predicate(x):
            return i
    
def find_indices(predicate, List):
    """
    Returns an array of all the indices of the 
    elements which pass the predicate. Returns an 
    empty list if the predicate never passes.
    find-indices even, [1 2 3 4] #=> [1, 3]
    
    >>> find_indices(lambda x: x > 2, [1, 2, 30, 404, 0, -1, 90])
    [2, 3, 6]
    """
    result = []
    
    for i, x in enumerate(List):
        if predicate(x):
            result.append(i)
    
    return result
            
    


def tail(list, n):
    """ Return the last n elements of a list """
    return list[:n]

def head(list, n):
    """Return the firsts n elements of a list """
    return list[:n]

def every(function, array):
    """
    every_.every(list, [predicate], [context]) Alias: all
    Returns true if all of the values in the list pass the predicate truth test.

    >>> from m2py import functional as f
    >>> f.every(lambda x: x> 4, [1, 2, 3, 4, 5 ,6 , 7, 8])
    False
    >>>
    >>>
    >>> f.every(lambda x: x> 4, [5 ,6 , 7, 8])
    True
    >>>
    """
    return reduce(lambda a, b: a and b, mapl(function, array)) == True


def some(function, array):
    """
    Returns true if any of the values in the list pass the predicate
    truth test. Short-circuits and stops traversing the list if a true
    element is found.

    Example:

    >>> from m2py import functional as f
    >>> f.some(lambda x: x> 4, [1, 2, 3, 4])
    False
    >>> f.some(lambda x: x> 4, [1, 2, 3, 4, 5 ,6 , 7, 8])
    True
    >>>
    """
    return reduce(lambda a, b: a or b, mapl(function, array)) == True


def unique(lst):
    """
    Remove repeated elements from an aray
    """
    return sort(set(lst))


def reverse(array):
    """
    Return reversed array (list)

    :param array: List or Tuple of values
    :return:      Reversed array

    >>> from m2py import functional as f
    >>>
    >>> f.reverse((1, 2, 3, 4, 5))
    [5, 4, 3, 2, 1]
    >>>
    >>>
    >>> f.reverse([1, 2, 3, 4, 5])
    [5, 4, 3, 2, 1]
    """
    if is_list(array):
        c = array.copy()
    elif is_tuple(array):
        c = list(array)
    else:
        raise Exception("Error: array must be tuple or list")

    c.reverse()
    return c

def last(array):
    """
    Return the last element of a list
    """
    return array[-1]

def first(array):
    """
    Return the first element of a list
    """
    return array[0]

def nth(array, n):
    """

    nth(N, List) -> Elem

    > lists:nth(3, [a, b, c, d, e]).
    c

    Idea from: http://erldocs.com/17.3/stdlib/lists.html
    """
    return array[n]


def inc(x):
    return x+1

def sort(array):
    """

    sort(List1) -> List2

        List1 = List2 = [T]
        T = term()

    Returns a list containing the sorted elements of List1.

    Idea from: http://erldocs.com/17.3/stdlib/lists.html
    """
    if is_list(array):
        c = array.copy()
    else:
        c = list(array)

    c.sort()
    return c

def sublist(list, start, len):
    """
    Returns the sub-list of List1 starting at Start and with (max) Len elements. It is not an error for Start+Len to exceed the length of the list.

    >>> x
    [-1, 2, 10, 23, 23.23]
    >>> f.sublist(x, 1, 3)
    [2, 10, 23]
    >>> f.sublist(x, 2, 3)
    [10, 23, 23.23]
    >>>
    >>>
    """
    return list[start:(start+len)]

def is_allequal(List):
    """
    Test if all elements of
    a list are the same.

    return True  if all elements are equal
    return False if elements are different
    """
    return all([x == List[0] for x in List])


def duplicate(N, Elem):
    """

    N = integer() >= 0
    Elem = T
    List = [T]
    T = term()

    Returns a list which contains N copies of the term Elem. For example:

    > lists:duplicate(5, xx).
    [xx,xx,xx,xx,xx]

    Note: Function taken from Erlang -
    http://erldocs.com/17.3/stdlib/lists.html#duplicate
    """
    if hasattr(Elem, "copy"):
        return [Elem.copy() for i in range(N)]
    else:
        return [Elem for i in range(N)]



def copy(object):
    """
    Returns a clone of object

    Note: From cloujure Language
    http://docs.oracle.com/javase/6/docs/api/java/util/Vector.html#indexOf%28java.lang.Object%29
    """

    if hasattr(object, "copy"):
        return object.copy()
    else:
        return object




def append(*ListOfLists):
    """
    ListOfLists = [List]
    List = List1 = [T]
    T = term()

    Returns a list in which all the sub-lists of ListOfLists have been appended. For example:

    > lists:append([[1, 2, 3], [a, b], [4, 5, 6]]).
    [1,2,3,a,b,4,5,6]

    >>> from m2py import functional as f
    >>> f.append([1, 2, 3], ['a', 'b'], [4, 5, 6])
    [1, 2, 3, 'a', 'b', 4, 5, 6]

    Note: Function taken from Erlang -
    http://erldocs.com/17.3/stdlib/lists.html#append
    """
    newlist = []
    mapl(lambda x: newlist.extend(x), ListOfLists)
    return newlist



def mapdict_values(function, dic):
    """
    Apply a function to a dictionary values,
    creating a new dictionary with the same keys
    and new values created by applying the function
    to the old ones.

    :param function: A function that takes the dictionary value as argument
    :param dic:      A dictionary
    :return:         A new dicitonary with same keys and values changed

    Example:

    >>> dic1 = { 'a' : 10, 'b' : 20, 'c' : 30 }
    >>> mapdict_values(lambda x: x*2, dic1)
    {'a': 20, 'b': 40, 'c': 60}
    >>> dic1
    {'a': 10, 'b': 20, 'c': 30}
    """
    return dict(map(lambda x: (x[0], function(x[1])), dic.items()))


def mapdict_keys(function, dic):
    """
    Apply a function to a dictionary keys,
    creating a new dictionary with the same values
    and new values created by applying the function
    to the old ones.

    :param function: A function that takes the dictionary key as argument
                      and returns a new dictionary key
    :param dic:      A dictionary
    :return:         A new dicitonary with same keys and values changed

    Example:

    >>> dic1 = { 'a' : 10, 'b' : 20, 'c' : 30 }
    >>>
    >>> mapdict_keys(lambda x: str(x) + "_hello", dic1)
    {'a_hello': 10, 'b_hello': 20, 'c_hello': 30}
    >>>
    >>> dic1
    {'a': 10, 'b': 20, 'c': 30}
    """
    return dict(map(lambda x: (function(x[0]), x[1]), dic.items()))


def merge_dict(*dictionaries):
    """
    Merge a list of dictionaries returning a new one.
    
    :param dictionaries: A list of dictionaries
    :return:             A new dicitonary
    :rtype:              dict
    """
    result = {}
    
    for d in dictionaries:
        result.expand(d)
    
    return result
    

def reverse_dict(dic):
    """
    
    """
    return dictzip(*reverse(unzip_l(dic.items())))


def product(list):
    """
    Returns a product of a List

    :param list:
    :return:
    """

    prod = 1
    for e in list:
        prod = prod*e
    return prod


def get(property):
    """
    >>> user =  {'name': 'Bemmu', 'uid': '297200003'}
    >>> get("name")(user)
    'Bemmu'
    """

    def get_property(object):

        if is_dict(object):
            return object.get(property)
        else:
            return getattr(object, property)

    return get_property



def pluck(property):
    """

    This pattern of combining splat and get is very
    frequent in JavaScript code.
    So much so, that we can take it up another level:

    :param property:
    :return:
    
    Example:
    
   users = [
       {
       "name" : "Bemmu",
       "uid" : "297200003"
       },
       {
       "name" : "Zuck",
       "uid" : "4"
       }
   ]   
   >>> get_name = pluck("name")
   >>> get_name(users)
   ['Bemmu', 'Zuck']

    
    
    
    """

    def fun(object_array):


        if is_list(object_array):

            if is_dict(object_array[0]):
                out = map(lambda obj: obj.get(property), object_array)
            else:
                out = map(lambda obj: getattr(obj, property), object_array)
        else:

            if is_dict(object_array):
                out = object_array.get(property)
            else:
                out = getattr(object_array, property)

        return list(out)

    return fun

    

def printf(function):
    def printer(*args, **kwargs):
        print(function(*args, **kwargs))
    return printer
    

def take_while(predicate, List):
    result = []
    for e in List:
        if not predicate(e):
            return result
        else:
            result.append(e)

def drop_while(predicate, List):
    result = List.copy()
    
    for e in List:
        if not predicate(e):
            return result.pop(0)
        else:
            result.pop(0)


def once(func):
    """
    Once will create a function you can only run once. 
    Subsequent invocations will return the first result.
    """
    cache = []
    #def once_function(x):
    
    
    
def memoize(func):
    
    cache = {}
    
    def memoized(x):
        
        out =  cache.get(x)     
        if not out:
            out = func(x)
            cache[x] = out
            return out
        else:
            return out
            
    return memoized
            


def fibbonaci(n):
    
    if n > 2:
        return fibbonaci(n-1) + fibbonaci(n-2)
    else:
        return 1
        
        
    
def __fib(n):
    
    if n > 2:
        
        c = __fib.cache.get(n)
        if c:
            return c        
        
        a = __fib.cache.get(n-1)
        b = __fib.cache.get(n-2)
        
        if not a:            
            a = __fib(n-1) 
            __fib.cache[n-1] = a
        
        if not b:
            b = __fib(n-2)
            __fib.cache[n-2] = b
        
        c =  a + b 
        __fib.cache[n] = c
        return c
    else:
        return 1
                
__fib.cache = {}


def fib(n):
    if not __fib.cache.get(n-1):
        mapl(__fib, range(n))
    return __fib(n)
    


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
    f = lambda x: juxt(funclist, x)
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

    >>> from m2py.functional.vectorize import equalize
    >>> equalize([1, 2, 3, 4, 5, 6], [-2, -1, 0, 1, 2, 3], 8, 6)
    [[1, 2, 3, 4, 5, 6], [-2, -1, 0, 1, 2, 3], [8, 8, 8, 8, 8, 8], [6, 6, 6, 6, 6, 6]]

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


    >>> from m2py.functional.vectorize import vectorize_args
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

