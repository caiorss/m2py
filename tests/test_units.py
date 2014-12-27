#!/usr/bin/env python
# -*- coding: utf-8 -*-

import m2py.units as u

from m2py.utils import run_example


print("Converting 100 atm to torr")
run_example("""print 100*u.atm/u.torr""")

print("Converting 1500 kPa to psi")
run_example("""print 1500*u.kPa/u.psi""")

print("Convertin 10 psi to kPa")
run_example("""print u.convert(10, 'psi', 'kPa')""")