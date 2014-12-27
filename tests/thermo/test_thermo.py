#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from .__init__ import *

from m2py.thermo import steam as s
from m2py.thermo import xsteam as xs

print("xsteam - Psat(100 °C) = ", xs.psat_t(100))
print("steam  - Psat(100 °C) = ", s.p_satT(100))

#print "Psat(100 °C) = ", s.p_satT(100)
#print "Tsat(100 kPa) = ", s.T_sat(100)
