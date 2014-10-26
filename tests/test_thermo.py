#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

from m2py.thermo import steam as s


print "Psat(100 °C) = ", s.P_sat(100)

print "Tsat(100 kPa) = ", s.T_sat(100)
