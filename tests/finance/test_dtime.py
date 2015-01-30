#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

from m2py.finance.dtime import date_range


print(40*"-")
print("""Function: pprint( date_range("08/12/2014", "13/12/2014"))""")
print("Date range from 08/12/2014 to 13/12/2014\n")

pprint(date_range("08/12/2014", "13/12/2014"))
