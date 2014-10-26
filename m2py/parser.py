#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyparsing as p
from pyparsing import alphanums, alphas,\
    nums, OneOrMore, Optional, Word, Combine, Or, ZeroOrMore
from pyparsing import Literal, oneOf

lbracket = p.Suppress('[')
rbracket = p.Suppress(']')
Quote = Literal("'")

sign = p.oneOf('+ -')
Num = Word(nums)
Variable = Combine(Word(alphas) +  Optional(Num))

E = oneOf("E e")

fltnum = Optional(sign) + \
         Or([Num,
             Optional(Num) + '.' + Num,
             Num + '.' + Optional(Num)]) + \
         Optional(E + Optional(sign) + Num)

fltnum = Combine(fltnum)


mlist = lbracket + ZeroOrMore(Or(fltnum, Variable )) + rbracket

# fltnum = Word(fltnum)
#fltnum = Combine(sign + Optional(Nums) + Optional(".") + Optional(Nums) + E + Optional(Nums))

arange = Literal('(') + fltnum + Literal(":") + fltnum + Literal(":") + fltnum + Literal(")")

txt = """
x = (0:0.2:10)';
y1 = trimf(x, [3 4 5]);
y2 = trimf(x, [2 4 7]);         % some commentary
y3 = trimf(x, [1 4 9]);
subplot(211), plot(x, [y1 y2 y3]);%some commentary4344
y1 = trimf(x, [2 3 5]);
y2 = trimf(x, [3 4 7]);
y3 = trimf(x, [4 5 9]); % Another commentary
subplot(212), plot(x, [y1 y2 y3]);
set(gcf, 'name', 'trimf', 'numbertitle', 'off')
"""

txt= txt.replace(';', '')      # Remove semicolon end line
txt = txt.replace('%', '#')    # Replace commentary symbol



print "arange", arange.searchString(txt)

for s in mlist.searchString(txt):
    print s


