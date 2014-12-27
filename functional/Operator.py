#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Operator to Generate Lambda expressions

    Scala-style lambdas definition

    Idea from: https://github.com/kachayev/fn.py#fnpy-enjoy-fp-in-python

    Example:

    In [1]: from functional import X, mapl, filterl

    In [2]: list(filter(X  < 10, [9, 10, 11]))
    Out[2]: [9]

    In [4]: mapl(X ** 2, [1, 2, 3, 4, 5, 6, 7])
    Out[4]: [1, 4, 9, 16, 25, 36, 49]

    In [2]: mapl(X  / 10, [9, 10, 11])
    Out[2]: [0.9, 1.0, 1.1]

    In [3]:  mapl( 10/X, [9, 10, 11])
    Out[3]: [1.1111111111111112, 1.0, 0.9090909090909091]

"""

class Operator():
    """
    Scala-style lambdas definition

    Idea from: https://github.com/kachayev/fn.py#fnpy-enjoy-fp-in-python

    Example:

    In [1]: from functional import X, mapl, filterl

    In [2]: list(filter(X  < 10, [9, 10, 11]))
    Out[2]: [9]

    In [4]: mapl(X ** 2, [1, 2, 3, 4, 5, 6, 7])
    Out[4]: [1, 4, 9, 16, 25, 36, 49]

    In [2]: mapl(X  / 10, [9, 10, 11])
    Out[2]: [0.9, 1.0, 1.1]

    In [3]:  mapl( 10/X, [9, 10, 11])
    Out[3]: [1.1111111111111112, 1.0, 0.9090909090909091]

    """

    def __add__(self, other):

        if isinstance(other, Operator):
            return lambda x, y: x + y
        return lambda x: x + other

    def __radd__(self, other):
        if isinstance(other, Operator):
            return lambda x, y: x + y
        return lambda x: other  + x

    def __mul__(self, other):

        if isinstance(other, Operator):
            return lambda x, y: x * y
        return lambda x: x * other

    def __rmul__(self, other):

        if isinstance(other, Operator):
            return lambda x, y: x * y
        return lambda x: x * other


    def __sub__(self, other):
        return lambda x: x - other

    def __rsub__(self, other):
        return lambda x: other - x


    def __div__(self, other):
        return lambda x: x / other

    def __truediv__(self, other):
        return lambda x: x / other

    def __floordiv__(self, other):
        return lambda x: x // other

    def __rdiv__(self, other):
        return lambda x: other / x

    def __rtruediv__(self, other):
        return lambda x: other / x

    def __rfloordiv__(self, other):
        return lambda x: other // x

    def __pow__(self, other):
        return lambda x: x ** other

    def __rpow__(self, other):
        return lambda x: other ** x

    def __neg__(self):
        return lambda x:  -x

    def __pos__(self) :
        return lambda x:  x

    def __abs__(self):
        return lambda x: abs(x)

    def __len__(self):
        return lambda x: len(x)

    def __eq__(self, other):
        return lambda x: x == other

    def __ne__(self, other):
        return lambda x: x != other

    def __lt__(self, other):
        return lambda x: x < other

    def __le__(self, other):
        return lambda x: x <= other

    def __gt__(self, other):
        return lambda x: x > other

    def __ge__(self, other):
        return lambda x: x >= other

    def __or__(self, other):
        return lambda x: x or other

    def __and__(self, other):
        return lambda x: x and other

    def __rand__(self, other):
        return lambda x: other and x

    def __ror__(self, other):
        return lambda x: other or x

    def __contains__(self, item):
        return lambda x: item in x

    def __int__(self):
        return lambda x: int(x)

    def __float__(self):
        return lambda x: float(x)

    def split(self, pattern=' '):
        return lambda x: x.split(pattern)

    def strip(self):
        return lambda x: x.strip()

    def map(self, function):
        return lambda x: map(function, x)

    def sum(self):
        return lambda x: sum(x)

    def key(self, keyname):
        """Generate lambda expression for dictionary key """
        return lambda x: x[keyname]

    def item(self, it):
        """Generate lambda function for list item """
        return lambda x: x[it]



X = Operator()


