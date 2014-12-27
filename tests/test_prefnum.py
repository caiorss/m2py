#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from m2py.misc import prefnum

"""
 prefnum([514,7.6,37,0.9],'E6')     Electronic, six steps per decade.
   ans = [470,6.8,33,1]

 prefnum([514,7.6,37,0.9],'E12')    Electronic, twelve steps per decade.
   ans = [560,8.2,39,0.82]

 prefnum([514,7.6,37,0.9],'R10')    Renard, ten steps per decade.
   ans = [500,8.0,40,1]

 prefnum([514,7.6,37,0.9],'R"5')    Renard, five steps per decade, twice rounded.
   ans = [600,6.0,40,1]

 prefnum([514,7.6,37,0.9],'125')    1-2-5, three steps per decade.
   ans = [500,10,50,1]

 prefnum([514,7.6,37,0.9],[25,75])  Custom vector, two steps per decade.
   ans = [750,7.5,25,0.75]

 prefnum([514,7.6,37,0.9],1)        Custom vector, nearest order of magnitude.
   ans = [100,10,10,1]
"""

print(prefnum([514, 7.6, 37, 0.9], 'E6'))  # Electronic, six steps per decade.

print(prefnum([514, 7.6, 37, 0.9], 'E12'))  # Electronic, twelve steps per decade.

print(prefnum([514, 7.6, 37, 0.9], 'R10'))  # Renard, ten steps per decade.

print(prefnum([514, 7.6, 37, 0.9], 'R"5'))  # Renard, five steps per decade, twice rounded.

print(prefnum([514, 7.6, 37, 0.9], '125'))  # 1-2-5, three steps per decade.


# print prefnum([514,7.6,37,0.9],[25,75]) # Custom vector, two steps per decade.


prefnum([514, 7.6, 37, 0.9], 1)  # Custom vector, nearest order of magnitude.
