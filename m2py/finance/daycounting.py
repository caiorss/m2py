#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


References:
    http://knowpapa.com/dcc/

    http://www.mathworks.com/help/finance/days360.html

    http://www.deltaquants.com/day-count-conventions.html

    http://books.google.com.br/books?id=yZEiBAAAQBAJ&pg=PA27&lpg=PA27&dq=30/360++PSA&source=bl&ots=CixnlbvO4b&sig=EmG_w-zwMVA31Pgx6Tid8gO4Ulw&hl=en&sa=X&ei=OS2CVPmhG4aUNrj3gMgK&ved=0CFMQ6AEwCQ#v=onepage&q=30%2F360%20%20PSA&f=false

    http://wiki.treasurers.org/wiki/Day_count_conventions

    http://books.google.co.uk/books?id=4C-wInTw8uwC&pg=PT147&lpg=PT147&dq=day+counting+convention+yearfraction&source=bl&ots=kvq9OIO4qY&sig=tbDpALN82q95CYGQMNwjQEgzXAI&hl=en&sa=X&ei=CDWCVJ_-LsGaNqb2g6gF&ved=0CEgQ6AEwBw#v=onepage&q=day%20counting%20convention%20yearfraction&f=false
"""

import datetime
import utils

Date = lambda datestr: datetime.datetime.strptime(datestr, "%d-%m-%Y")
date2ymd = lambda date: (date.year, date.month, date.day)


import shelve
__brazil_holydays_database = utils.resource_path("holydays/brazil_holydays.dat")
sh = shelve.open(__brazil_holydays_database)
brazil_holydays = sh["brholydays"]
sh.close()

def is_leap_year(date):
    import calendar

    return calendar.isleap(date.year)


def eomday(year, month):
    """
    Returns the last day of month

    :param year:    Year Integer
    :param month:   Month Interger  1-12
    :return:
    """
    import calendar

    return filter(lambda x: x != 0, calendar.monthcalendar(year, month)[-1])[-1]


actual_actual = lambda date1, date2: (date2 - date1).days


def days360(date1, date2):
    # date1 = Date(date1)
    # date2 = Date(date2)

    from calendar import isleap

    Y1, M1, D1 = date2ymd(date1)
    Y2, M2, D2 = date2ymd(date2)

    if D1 == 31:
        D1 = 30

    if D2 == 31 and D1 in [30, 31]:
        D2 = 30

    if M1 == 2 and ((D1 == 28 and not isleap(Y1)) or D1 == 29):
        D1 = 30

    N = 360 * (Y2 - Y1) + 30 * (M2 - M1) + (D2 - D1)
    return N


def days360e(date1, date2):
    # date1 = Date(date1)
    # date2 = Date(date2)

    Y1, M1, D1 = date2ymd(date1)
    Y2, M2, D2 = date2ymd(date2)

    if D1 == 31:
        D1 = 30

    if D2 == 31:
        D2 = 30

    N = 360 * (Y2 - Y1) + 30 * (M2 - M1) + (D2 - D1)
    return N


def days360isda(date1, date2):
    # date1 = Date(date1)
    # date2 = Date(date2)

    Y1, M1, D1 = date2ymd(date1)
    Y2, M2, D2 = date2ymd(date2)

    if D1 == 31:
        D1 = 30

        if D2 == 31:
            D2 = 30

    N = 360 * (Y2 - Y1) + 30 * (M2 - M1) + (D2 - D1)
    return N


def days360psa(date1, date2):
    # date1 = Date(date1)
    # date2 = Date(date2)

    Y1, M1, D1 = date2ymd(date1)
    Y2, M2, D2 = date2ymd(date2)

    if D1 == 31:
        D1 = 30

    if M1 == 2 and D1 == eomday(Y1, 2):
        D1 = 30

    if D1 == 30:
        D2 = 30

    N = 360 * (Y2 - Y1) + 30 * (M2 - M1) + (D2 - D1)
    return N


def daysbus(date1, date2, holydays=brazil_holydays):

    from dtime import networkdays
    return networkdays(date1 , date2, holydays)


def isbusday(date, holydays=brazil_holydays):

    #print dict(date=date, week=date.isoweekday())

    if date.isoweekday() in [6, 7] or date in holydays:
        return False
    else:
        return True

    #return date.weekday() not in [5, 6] and date not in holydays

def nextbusday(date):
    """
    Get the first business day after some date,
    if the date is as business day returns the date.

    :param date:
    :return:
    """
    nextdate = date

    while True:

        if isbusday(nextdate):
            return nextdate
        nextdate = daysadd(nextdate, 1)

def prevbusday(date):
    """
    Get the first business day before some date,
    if the date is as business day returns the date.

    :param date:
    :return:
    """
    nextdate = date

    while True:

        if isbusday(nextdate):
            return nextdate
        nextdate = daysadd(nextdate, -1)


def daysdif(StartDate, EndDate, Basis=0):
    """

    :param StartDate:
    :param EndDate:
    :param Basis:
    :return:

    StartDate	Enter as serial date numbers or date strings.
    EndDate	Enter as serial date numbers or date strings.


    Basis	"(Optional) Day-count basis of the instrument. A vector
        0 = actual/actual (default)
        1 = 30/360 (SIA)                United States
        2 = actual/360
        3 = actual/365
        4 = 30/360 (PSA)
        5 = 30/360 (ISDA)
        6 = 30/360 (European)
        7 = actual/365 (Japanese)
        8 = actual/actual (ISMA)
        9 = actual/360 (ISMA)
        10 = actual/365 (ISMA)
        11 = 30/360E (ISMA)
        12 = actual/365 (ISDA)
        13 = BUS/252                    Brazil Government Bonds
    """
    date1 = Date(StartDate)
    date2 = Date(EndDate)
    day_counting = daysdif.convention_list[str(Basis)]

    ndays = day_counting(date1, date2)
    return ndays

daysdif.convention_list = {
    '0': actual_actual,
    '2': actual_actual,
    '3': actual_actual,
    '7': actual_actual,
    '8': actual_actual,
    '9': actual_actual,
    '10': actual_actual,
    '12': actual_actual,

    '1': days360,
    '4': days360psa,
    '5': days360isda,
    '6': days360e,
    '11': days360e,

    '13': daysbus,
}


def yearfrac(StartDate, EndDate, Basis):
    """

    :param StartDate:
    :param EndDate:
    :param Basis:
    :return:

    StartDate	Enter as serial date numbers or date strings.
    EndDate	Enter as serial date numbers or date strings.


    Basis	"(Optional) Day-count basis of the instrument. A vector
        0 = actual/actual (default)
        1 = 30/360 (SIA)                United States
        2 = actual/360
        3 = actual/365
        4 = 30/360 (PSA)
        5 = 30/360 (ISDA)
        6 = 30/360 (European)
        7 = actual/365 (Japanese)
        8 = actual/actual (ISMA)
        9 = actual/360 (ISMA)
        10 = actual/365 (ISMA)
        11 = 30/360E (ISMA)
        12 = actual/365 (ISDA)
        13 = BUS/252                    Brazil Government Bonds

    Reference: http://www.mathworks.com/help/finance/yearfrac.html
    """
    denom = yearfrac.denominators[str(Basis)]
    Ndays = daysdif(StartDate, EndDate, Basis)
    return Ndays / denom


yearfrac.denominators = {
    # 360 days
    '1': 360.0,
    '2': 360.0,
    '4': 360.0,
    '5': 360.0,
    '6': 360.0,
    '9': 360.0,
    '11': 360.0,

    # 365
    '3': 365.0,
    '7': 365.0,
    '10': 365.0,
    '12': 365.0,

    # 252 Business days ( Brazil)
    '13': 252.0,
}


def daysadd(StartDate, NumDays, Basis=0):
    """

    :param StartDate:
    :param NumDays:
    :param Basis:
    :return:

    Reference: http://www.mathworks.com/help/finance/daysadd.html
    """
    #print StartDate
    return StartDate + datetime.timedelta(days=NumDays)



def test_days_360():
    print days360('15-01-2000', '15-03-2000')

    # moredays = [ '15-03-2000', '15-04-2000', '15-06-2000']
    # print map(lambda d2: days360('15-01-2000', d2), moredays)

    print days360('28-02-2015', '13-09-2012')


def test_year_frac():

    print yearfrac('1-1-2000', '1-1-2001', 9)


#test_days_360()

#test_year_frac()