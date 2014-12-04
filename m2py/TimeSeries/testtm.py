#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
sys.path.append("/home/tux/PycharmProjects/stockmarket")

from stockmarket import yahoo
from TimeSerie import TimeSerie


#jsonstr = open("petr4.json").read()

#t = TimeSerie.from_json(jsonstr)


d= yahoo.fetch_stock("PETR4.SA",2013)

t = TimeSerie(headers= ['ts', 'low', 'high', 'close'],
               ts=d['Date'],
               low=d['Low'],
               high=d['High'],
               close=d['Close'])

def find_indices(lst, condition):
  return [i for i, elem in enumerate(lst) if condition(elem)]

d1 =  datetime.datetime(2000, 1, 14, 0, 0)
d2 =  datetime.datetime(2000, 1, 3, 0, 0)

idx = find_indices(t.ts, lambda e: e < d2)
