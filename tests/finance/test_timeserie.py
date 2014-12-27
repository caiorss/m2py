#!/usr/bin/env python
# -*- coding: utf-8 -*-


from m2py.finance.timeserie import Tserie  #selic as Selic

selic = Tserie.from_csv("/home/tux/PycharmProjects/m2py/m2py/finance/series/datasets/selic.csv")

#selic = Selic.selic
selic2 = selic.time_range_serie()


selic.info()

selic.head()

selic.tail()

selic.plot('VNA')
selic.show()

print(" TIME REFERENCE TO DATE ZERO")

#selic2 = selic.time_range_serie()

selic2.info()
selic2.head()
selic2.tail()
selic2.plot('VNA')
selic2.show()

#print selic.ts.time_formated()

#tsr = selic.ts.time_range_serie_du()
