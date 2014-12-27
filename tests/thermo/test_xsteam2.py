#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .__init__ import *
import m2py.thermo.xsteam as xs


def calcerror(p):
    return 100*abs(p[1] - p[0])/p[0]


def test_function(function, arg, y):

    _y = list(map(function, arg))

    #print _y

    error = list(map(calcerror, list(zip(y, _y))))

    print(["%.3f" % e for e in _y])
    print(["%.3f" % e for e in error])
    print("Max Error %.3f%%" % max(error))


# Test Tast P
Ts = [50,     60,     100,   150,  200, 300, 370]
Ps = [12.350, 19.941, 101.3, 475.9, 1533.8, 8581.0, 21028 ]
Hf = [209.31, 251.11, 419.02, 632.18, 852.43, 1344.01, 1890.37]

#_Ps = map(xs.psat_t, Ts)

print("Testing xs.psat_t")

test_function(xs.psat_t, Ts, Ps)

#print map(lambda e: "%.3f" % e, _Ps)
#print map(lambda e: "%.3f%%" % e, Error)

print(80 * "-")
#-------------------------------------------------------------

print("Testing xs.tsat_p")

test_function(xs.tsat_p, Ps, Ts)

#_Ts = map(xs.tsat_p, Ps)
#Error = map(calcerror, zip(Ts, _Ts))
#-------------------------------------------------------------

print(80 * "-")

print("Testign xs.h_px(p, 0) or hf(p)")

hf_p = lambda p: xs.h_px(p, 0)

test_function(hf_p, Ps, Hf)

#-------------------------------------------------------------

print(80 * "-")

print("Testign xs.h_tx(p, 0) or hf(t)")

hf_t = lambda t: xs.h_tx(t, 0)

test_function(hf_t, Ts, Hf)

#-------------------------------------------------------------

print(80 * "-")

print("Testing xs.h_pt")

pt = [(10, 50), (10, 100), (10, 400), (10, 700), (10, 1000), (10, 1200), (100, 200), (100, 700), (300, 250), (300, 600),
    (300, 1200), (500, 400), (800, 1000)]
h  = [2592.56,  2687.46,   3279.51,   3928.73,    4640.58,   5147.78,    2875.27, 3928.23,        2728.69,  3703.20,
    5147.08, 3271.83, 4638,20 ]

#_h = map(lambda r: xs.h_pt(r[0], r[1]), pt)


test_function(lambda r: xs.h_pt(r[0], r[1]), pt, h)


#print map(lambda e: "%.3f" % e, _h)


#hg_p = lambda p: "%.3f" % xs.h_px(p, 1)

#print map(hf_p, Ps)
#print map(hg_p, Ps)