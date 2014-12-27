#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .__init__ import *
from m2py.finance import *


print("Function xirr")
print("Variable cash flow, example from: http://www.mathworks.com/help/finance/xirr.html")

CashFlow = [-10000, 2500, 2000, 3000, 4000];
CFDates = ['01/12/2007', '02/14/2008', '03/03/2008', '06/14/2008', '12/01/2008'];

Return = xirr(CashFlow, CFDates)
print(100*Return)

