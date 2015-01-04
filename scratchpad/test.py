#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pyparsing import Word, alphas, Regex, Suppress, CaselessLiteral, Combine
from pyparsing import Word, Literal, alphas, nums, Optional, OneOrMore
import string

# define grammar
point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
number = Word(nums)
integer = Combine(Optional(plusorminus) + number)
floatnumber = Combine(integer +
                      Optional(point + Optional(number)) +
                      Optional(e + integer)
)



comma = Literal(",")
dot = Literal(".")
floatnum = Word(nums + '.' + nums)
matlab_list = Suppress('[') + OneOrMore(floatnum) + Suppress(']')

greet = Word(alphas) + "," + Word(alphas) + "!"
greeting = greet.parseString("Hello, World!")
print(greeting)

numeric_const_pattern = r"""
 [-+]? # optional sign
 (?:
     (?: \d* \. \d+ )
     |
     (?: \d+ \.? )
 )
 (?: [Ee] [+-]? \d+ ) ?
 """

txt = """
x = (0:0.2:10)';
y1 = trimf(x, [3 4 5]);
y2 = trimf(x, [2 4 7]);
y3 = trimf(x, [1 4 9]);
subplot(211), plot(x, [y1 y2 y3]);
y1 = trimf(x, [2 3 5]);
y2 = trimf(x, [3 4 7]);
y3 = trimf(x, [4 5 9]);
subplot(212), plot(x, [y1 y2 y3]);
set(gcf, 'name', 'trimf', 'numbertitle', 'off'
"""

# floatt = Word(FLOAT)

print(floatnumber.searchString(txt))

#rx = re.compile(numeric_const_pattern, re.VERBOSE)