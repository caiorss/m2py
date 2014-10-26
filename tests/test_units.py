#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *
import m2py.units as u

from utils import run_example


print "Converting 100 atm to torr"
run_example("""print 100*u.atm/u.torr""")

print "Converting 1500 kPa to psi"
run_example("""print 1500*u.kPa/u.psi""")

print "Convertin 10 psi to kPa"
run_example("""print u.convert(10, 'psi', 'kPa')""")