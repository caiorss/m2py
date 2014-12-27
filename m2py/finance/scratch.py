#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reference:

    * http://www.ericbenhamou.net/documents/Encyclo/Accrued%20interest%20and%20day%20count%20convention.pdf

    * http://www.maplesoft.com/support/help/maple/view.aspx?path=Finance%2FExamples%2FCalendarsAndDayCounters

"""
import datetime

Date = lambda datestr: datetime.datetime.strptime(datestr, "%d-%m-%Y")

date2ymd = lambda date: (date.year, date.month, date.day)


def daycounting_actual(date1, date2):
    """
    Actual/Actual Day Counting

    Used for Treasury bonds and notes, it is the most intuitive of the day counting
    schemes. In this convention, the number of days between two dates is the
    actual number of days.

    :param date1:
    :param date2:
    :return:
    """
    date1 = Date(date1)
    date2 = Date(date2)
    #print dict(date1=date1, date2=date2)
    return (date2 - date1).days


def daycounting_30_360(date1, date2):
    """
    30/360 Day Counting

    :param date1:
    :param date2:
    :return:

    30/360 Day Counting
    Used for corporate bonds, U.S. Agency bonds, and all mortgage backed
    securities, the 30/360 day counting scheme was invented at a time that


     The number of days from M1/D1/Y1
    to M2/D2/Y2 is computed according to the following procedure:
    1. If D1 is 31, change D1 to 30.
    2. if D2 is 31 and D1 is 30 or 31, then change D2 to 30.
    3. If M1 is 2, and D1 is 28 (in a non-leap year) or 29, then change D1 to 30.
    Then the number of days, N is:
    N = 360(Y2 - Y1) + 30(M2 - M1) + (D2 - D1)

    Reference:
    """
    date1 = Date(date1)
    date2 = Date(date2)
    Y1, M1, D1 = date2ymd(date1)
    Y2, M2, D2 = date2ymd(date2)

    if D1 == 31:
        D1 = 30

    if D2 == 31 and ( D1 == 30 or D1 == 31):
        D2 = 30

    if M1 == 2 and ( D1 == 28 or D1 == 29):
        D1 = 30

    N = 360 * (Y2 - Y1) + 30 * (M2 - M1) + (D2 - D1)
    return N


def year_fraction(date1, date2, convention):

    conventions = {
        'ISDA' : 365.0,
        'Actual/360' : 360.0
    }

    convention_functions = {
        'ISDA' : daycounting_actual,
        'Actual/360' : daycounting_actual
    }

    func = convention_functions[convention]
    denominator = conventions[convention]

    return func(date1, date2)/denominator



print(daycounting_actual('15-01-2002', '05-03-2002'))

print(daycounting_actual('01-01-2006', '01-07-2006'))

print(year_fraction('01-01-2006', '01-07-2006', 'ISDA'))