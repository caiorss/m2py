#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""


def format_currency(number, flag=False):
    """
    Format number as currency

    :param number: Number to be formated (float)
    :param flag:   True/False
    :return:       Number string formated as currency

    flag:
        False:  Uses comma ',' as thousands separators and dot '.' as decimal separator
        True:   Comma ',' as as decimal separator and dot '.' as thousands separators
    """

    n = round(number, 2)
    _number = '{0:,}'.format(n)

    if not flag:
        return _number

    a, b = _number.split('.')
    return "".join([a.replace(',', '.'), ',', b])


def format_percent(number, digits=2):
    return "%.{}f%%".format(digits) % (100*number)



# print format_currency(1000000.67987)
# print format_currency(1000000.67987, True)
# print format_percent(0.0221, 4)