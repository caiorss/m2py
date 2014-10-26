#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Automated Testing of Steam Equations

"""

from __xsteam__ import *


tol = 1e-3

p = [0.0035, 0.0035, 30]  # Mpa
T = [300, 700, 700]  # K

print """
#----------------------------------#
#  Testing Values for Region 2     #
#----------------------------------#
Test Value:
Table 15. Page 17
Thermodynamic property values calculated from Eq. (15)
for selected values of T and p
"""

print """
Testing v2_pt - m3/kg
"""
expected = [0.394913866e2, 0.923015898e2, 0.542946619e-2]  # m3/kg
test_eq(v2_pT, (p, T), expected)

print """
Testing h2_pt - kJ/kg
"""
expected = [0.254991145e4, 0.333568375e4, 0.263149474e4]  # kJ/kg
test_eq(h2_pT, (p, T), expected)

print """
Testing u2_pT - kJ/kg
"""

expected = [0.241169160e4, 0.301262819e4, 0.246861076e4]
test_eq(u2_pT, (p, T), expected)

print """
Testing s2_pT - kJ.kg–1.K–1
"""
expected = [0.852238967e1, 0.101749996e2, 0.517540298e1]  # kJ.kg–1.K–1
test_eq(s2_pT, (p, T), expected)

print """
Testing CP2_pt(p, T) -
"""
expected = [ 0.191300162e1, 0.208141274e1, 0.103505092e2]
test_eq(Cp2_pT, (p, T), expected)

#print v2_pT

print """
#----------------------------------#
#  Testing Values for Region 2     #
#----------------------------------#

The Backward Equations T( p, h ) for Subregions 2a, 2b, and 2c

T2_ph - K
"""

p = [0.001,3, 3, 5, 5, 25, 40, 60, 60]                                              # Pressure   MPa
h = [3000, 3000, 4000, 3500, 4000, 3500, 2700, 2700, 3200 ]                         # Entalphy   h/(kJ.kg)
T = [0.534433241e3, 0.575373370e3, 0.101077577e4, 0.801299102e3,
     0.101531583e4, 0.875279054e3, 0.743056411e3, 0.791137067e3, 0.882756860e3 ]    # Temperatur K
test_eq(T2_ph, (p, h), T )


