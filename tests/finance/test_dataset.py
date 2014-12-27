#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m2py.finance import series as s

s.data()

selic = s.Dataset.selic
usd =  s.Dataset.usd2brl

selic.info()
selic.plot("rate")