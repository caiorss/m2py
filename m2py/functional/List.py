#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
List Object based on SCALA List
using functional programming principles

"""
from functools import reduce

class List():

    def __init__(self, lst):
        self.lst = lst

    def copy(self):
        return List(self.lst.copy())

    def all(self):
        return all(self.lst)

    def any(self):
        return any(self.lst)

    def reverse(self):
        reversed = self.lst
        reversed.reverse()
        return List(reversed)

    def map(self, function):
        return List(list(map(function, self.lst)))

    def filter(self, function):
        return List(list(filter(function, self.lst)))

    def reduce(self, function):
        return reduce(function, self.lst)

    def size(self):
        return len(self.lst)

    def __str__(self):
        return str(self.lst)

    def __repr__(self):
        return str(self.lst)

    def sum(self):
        return sum(self.lst)

    def __contains__(self, item):
        return item in self.lst

    def __int__(self):
        return  List(list(map(int, self.lst)))

    def __float__(self):
        return List(list(map(float, self.lst)))

    def float(self):
        return List(list(map(float, self.lst)))

    def int(self):
        return  List(list(map(int, self.lst)))


    def __bool__(self):
        return len(self.lst) == 0

    def transpose(self):
        return List(list(zip(*self.lst)))

    def enumerate(self):
        return List(list(enumerate(self.lst)))

    def sort(self):
        return List(sort(self.lst))

    def joinstr(self, param=""):
        return param.join(map(str, self.lst))

    def is_allequal(self):
        return all([x == self.list[0] for x in self.list])

    def array(self):
        return numpy.array(self.lst)