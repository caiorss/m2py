# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 00:37:28 2014

@author: tux
"""

from m2py.finance import series as S
from m2py.finance.series import ipea


S.data()

selic =  S.Dataset.selic

selic.info()

selic.plot("VNA")

selic.plot("rate")


#END