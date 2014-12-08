#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m2py.finance import dtime
from m2py.finance import daycounting
from m2py.finance.timeserie import Tserie


ts = Tserie.from_bin("selic2.tsdat")
ts.info()

ts.head()

ts.tail()
#
# ts.plot(['rate'])
# ts.plot(['accum'])
# ts.to_csv("selic2.txt")
# ts.show()

def getVNA(date):
    #date = dtime.date_dmy(date)
    date = dtime.parser(date).date()

    print "Date ", date
    # date = daycounting.daysadd(date, -1)
    # date = dtime.date2str_dmy(date)
    #
    # return round(1000.0*ts.get_date(date)[0][-1], 2)

print getVNA("8/9/2010")