#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m2py.finance.dtime import dtime as d
from m2py.finance.dtime import date_range
from pprint import pprint

print 40*"-"
print """Function: pprint( date_range("08/12/2014", "13/12/2014"))"""
print "Date range from 08/12/2014 to 13/12/2014\n"

pprint(date_range("08/12/2014", "13/12/2014"))
