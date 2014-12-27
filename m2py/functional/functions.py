#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Primitive Useful Functions


"""
from functools import reduce

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
    return dict(list(zip(keys, values)))


def transpose(matrix):
    return list(zip(*matrix))


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


def find(function, array):
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
        if function(x):
            return x
    return None

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
    return storted(set(lst))


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



def identity(x):
    return x

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


