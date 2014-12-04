#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import sin, cos, pi, arctan2
from math import floor, log10

__factors__ = { "10^-9": "p","10^-6": "u",  "10^-3": "m", "10^3": "k", "10^6": "M", "10^9": "G" }

def deg2rad(deg):
    return deg * pi / 180

def rad2deg(rad):
    return rad / pi * 180

def sind(x):
    return sin(deg2rad(x))

def cosd(x):
    return cos(deg2rad(x))

def tand(x):
    return sind(x)/cosd(x)

# def atand(x):
#     return rad2deg(atan(x))

def arctan2d(x, y):
    return rad2deg(arctan2(x, y))


def __powerise10__(x):

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
    """Return a string representing x in an engineer friendly notation"""
    a , b = __powerise10__(x)
    if -3<b<3: return "%.4g" % x
    a = a * 10**(b%3)
    b = b - b%3
    return "%.4g*10^%s" %(a,b)


def eng2(x):
    """Return a string representing x in an engineer friendly with prefix"""

    e = eng(x)
    base, factor = e.split("*")

    try:
        s= __factors__[factor]
        return "%s %s" % (base, s)
    except:
        return e