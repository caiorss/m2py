# -*- coding: utf-8 -*-
"""
Plota Taxa SELIC
"""

from m2py.finance.series.selic import selic

selic

selic.head()

selic.tail()

selic.plot('rate')

selic.plot("VNA")