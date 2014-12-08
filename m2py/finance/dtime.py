#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
$ python -c "import dtime ; from pprint import pprint ; import shelve ; holydays= dtime.get_brazil_holidays() ; fp = shelve.open('holydays.dat') ; fp['brholydays']=holydays ;  fp.close()"

"""

from datetime import timedelta
from datetime import datetime
import re

#from dateutil.parser import parser

# started from the code of Casey Webster at
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/ddd39a02644540b7




# Define the weekday mnemonics to match the date.weekday function
(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)
weekends=(SAT,SUN)


#-------------------------------------------------------#
#                BUSINESS DAY AND DURATION              #
#-------------------------------------------------------#

def networkdays(start_date, end_date, holidays=[]):
    delta_days = (end_date - start_date).days + 1
    full_weeks, extra_days = divmod(delta_days, 7)
    # num_workdays = how many days/week you work * total # of weeks
    num_workdays = (full_weeks + 1) * (7 - len(weekends))
    # subtract out any working days that fall in the 'shortened week'
    for d in range(1, 8 - extra_days):
        if (end_date + timedelta(d)).weekday() not in weekends:
             num_workdays -= 1
    # skip holidays that fall on weekends
    holidays =  [x for x in holidays if x.weekday() not in weekends]
    # subtract out any holidays
    for d in holidays:
        if start_date <= d <= end_date:
            num_workdays -= 1
    return num_workdays

def _in_between(a,b,x):
    return a <= x <= b or b <= x <= a

def __cmp(a, b):
    return (a > b) - (a < b)

def workday(start_date, days=0, holidays=[]):
    full_weeks, extra_days = divmod(days,7 - len(weekends))
    new_date = start_date + timedelta(weeks=full_weeks)
    for i in range(extra_days):
        new_date += timedelta(days=1)
        while new_date.weekday() in weekends:
            new_date += timedelta(days=1)
    # to account for days=0 case
    while new_date.weekday() in weekends:
        new_date += timedelta(days=1)

    # avoid this if no holidays
    if holidays:
        delta = timedelta(days=1 * __cmp(days,0))
        # skip holidays that fall on weekends
        holidays =  [x for x in holidays if x.weekday() not in weekends ]
        holidays =  [x for x in holidays if x != start_date ]
        for d in sorted(holidays, reverse = (days < 0)):
            # if d in between start and current push it out one working day
            if _in_between(start_date, new_date, d):
                new_date += delta
                while new_date.weekday() in weekends:
                    new_date += delta
    return new_date


def ndays(date1, date2):
    """
    Number of Days between two dates

    :param date1: Start date
    :param date2: End   date
    :type  date1: datetime.datetime or date tuple (year, date, month)
    :type  date2: datetime.datetime or date tuple (year, date, month)
    :return:      Number of Days between two dates
    :rtype:      int
    """
    if isinstance(date1, tuple):
        date1 = datetime(*date1)
    if isinstance(date2, tuple):
        date2 = datetime(*date2)

    Ndays = (date2 - date1).days
    Ndays  = abs(Ndays) -1
    return Ndays


def nbdays(date1, date2, holydays):
    """
    Number of Business Days between two dates

    Return the number of business days  between two dates
    date2 > date1

    :param date1: Start date
    :param date2: End   date
    :type  date1: datetime.datetime or date tuple (year, date, month)
    :type  date2: datetime.datetime or date tuple (year, date, month)
    :return:      Number of Days between two dates
    :rtype:       int
    """
    if isinstance(date1, tuple):
        date1 = datetime(*date1)
    if isinstance(date2, tuple):
        date2 = datetime(*date2)
    return networkdays(date1,date2, holydays)


def nbdays_br(date1, date2):
    """
    Number of Business Days between two dates

    Return the number of business days  between two dates inb Brazil,
    regarding all bank-holydays until 2078

    date2 > date1

    :param date1: Start date
    :param date2: End   date
    :type  date1: datetime.datetime or date tuple (year, date, month)
    :type  date2: datetime.datetime or date tuple (year, date, month)
    :return:      Number of Days between two dates
    :rtype:       int
    """

    return networkdays(date1 , date2, [])


#------------------------------------------------------#
#               DATE PARSERS  - string to date object  #
#------------------------------------------------------#


def date2ymd(date):
    """
    Split datetime.datetime object into tuple

    :param date: Date datetime.datetime object
    :return: tuple (year, month, day)
    """
    return date.year, date.month, date.day

def date_dmy(datestr, separator="/"):
    """
    Parse Date Format  dd/mm/yyyy


    :param datestr:     Date string
    :param separator:   Date string separator
    :return:            datetime.datetime object

    Example:  01/12/2013
        >>> import dtime as d
        >>> d.date_dmy("01/12/2013")
        datetime.datetime(2013, 12, 1, 0, 0)
        >>>
    """
    fmt = "%d{separator}%m{separator}%Y".format(separator=separator)
    return datetime.strptime(datestr, fmt)

def date_mdy(datestr, separator="/"):
    """
    Parse American Date Format  mm/dd/yyyy


    :param datestr:     Date string
    :param separator:   Date string separator
    :return:            datetime.datetime object

    Example: 12/01/2013
        >>> import dtime as d
        >>> d.date_mdy("12/01/2013")
        datetime.datetime(2013, 12, 1, 0, 0)
        >>>

    """
    fmt = "%m{separator}%d{separator}%Y".format(separator=separator)
    return datetime.strptime(datestr, fmt)

def date_ymd(datestr, separator="/"):
    """
    Parse Date Format  yyyy/mm/dd
    Example:  2013/12/01

    :param datestr:     Date string
    :param separator:   Date string separator
    :return:            datetime.datetime object

    Example:
        >>> import dtime as d
        >>> d.date_ymd("2013/12/01")
        datetime.datetime(2013, 12, 1, 0, 0)
        >>>
    """
    fmt = "%Y{separator}%m{separator}%d".format(separator=separator)
    return datetime.strptime(datestr, fmt)


def format_date(date, fmt):
    return date.strftime(fmt)



#------------------------------------------------------#
#    DATE object to String                             #
#------------------------------------------------------#

def date2str_dmy(date, separator="/"):
    """

    :param date:
    :param separator:
    :return:

        >>> import dtime as d
        >>>
        >>> date =  d.date_dmy("01/12/2013")
        >>>
        >>> d.date2str_mdy(date)
        '12/01/2013'
    """
    fmt = "%d{separator}%m{separator}%Y".format(separator=separator)
    return date.strftime(fmt)

def date2str_mdy(date, separator="/"):
    """

    :param date:
    :param separator:
    :return:

        >>> import dtime as d
        >>>
        >>> date =  d.date_dmy("01/12/2013")
        >>>
        >>> d.date2str_mdy(date)
        '12/01/2013'
        >>>
    """
    fmt = "%m{separator}%d{separator}%Y".format(separator=separator)
    return date.strftime(fmt)

def date2str_ymd(date, separator="/"):
    """

    :param date:
    :param separator:
    :return:

        >>> import dtime as d
        >>>
        >>> date =  d.date_dmy("01/12/2013")
        >>>
        >>> d.date2str_ymd(date, '-')
        '2013-12-01'
        >>>
        >>> d.date2str_ymd(date, '_')
        '2013_12_01'
    """
    fmt = "%Y{separator}%m{separator}%d".format(separator=separator)
    return date.strftime(fmt)



def ymd2date(y, m, d):
    """
    Convert (y, m, d) tuple to datetime.datetime object
    where y, m, d are year, mont and date integers 
    Example (2013, 12, 20)
    
    :param tpl: Tuple inf (y, m, d) format
    :return: datetime.datetime object

    Example:
        >>> import dtime as d
        >>> d.tdate_ymd((2013,12,20))
        datetime.datetime(2013, 12, 20, 0, 0)
        >>>
    """
    #y, m, d  = tpl
    return datetime(y, m, d)


def dates2time(datelst, number_of_days=360.0):
    """
    Convert a list of date (datime.datetime) objects
    to time vector.

    :param datelst:
    :return:

    For example converts a datelist like, to:

        [date0, date1, date2, date3 ]
        [0, t1, t2, t3, t4 ]

        t1 = date1 - date0
        t2 = date2 - date0
        t3 = date3 - date2
        t4 = date4 - date3


    >>> from dtime import date_mdy, dates2time
    >>>
    >>> dates = map(date_mdy,  ["01/02/2015", "04/01/2015", "07/01/2015", "10/01/2015", ])
    >>> dates
    [datetime.datetime(2015, 1, 2, 0, 0),
     datetime.datetime(2015, 4, 1, 0, 0),
     datetime.datetime(2015, 7, 1, 0, 0),
     datetime.datetime(2015, 10, 1, 0, 0)]
    >>>
    >>> dates2time(dates) # in years
    [0.0, 0.24722222222222223, 0.5, 0.7555555555555555]
    >>>
    >>> dates2time(dates, 1) # Time vector, in days
    [0, 89, 180, 272]
    >>>
    """
    zerodate = datelst[0]
    timevector = map(lambda d: (d - zerodate).days / number_of_days, datelst)
    return timevector

def date2time_du(datelst):
    """
    Retorna Série Temporal em dias úteis

    :param datelst:
    :return:
    """
    zerodate = datelst[0]
    timevector = map(lambda d:  nbdays_br(zerodate, d), datelst)
    return timevector

def utcnow():
    return datetime.utcnow()

def now():
    return datetime.now()


def datenum2datetime(matlab_datenum):
    """
    Convert Matlab dtime integer to python datetime.datetime object

    :param matlab_datenum: Matalab date integer representation
    :type  matlab_datenum: int
    :return:               datetime.datetime object
    :rtype:                datetime.datetime
    """

    return datetime.fromordinal(matlab_datenum) + \
           timedelta(days=matlab_datenum % 1) - timedelta(days = 366)


def datetime2datenum(dt):
    """
    Convert datetime.datetime object to Matalab date representation
    dtime equivalent

    :param dt:  Datetime.datetime object
    :return:    dtime number Matlab representation
    """
    ord = dt.toordinal()
    mdn = dt + timedelta(days = 366)
    frac = (dt-datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
    return mdn.toordinal() + frac


__date_patterns = {

    '%d/%m' : re.compile( r'^\d{2}/\d{2}$', re.M),

    # 'yyyy-mm-dd'
    '%Y-%m-%d': re.compile("\d{4}-\d\d-\d\d"),

    '%Y/%m/%d': re.compile("\d{4}/\d{2}/\d{2}"),

    # yyyymmdd
    '%Y%m%d' : re.compile('\d{8}$'),

    # dd/mm/yy
    '%d/%m/%y': re.compile("\d{2}/\d{2}/\d{2}$"),

    # dd/mm/yyyy
    '%d/%m/%Y': re.compile("\d{2}/\d{2}/\d{4}"),


    '%d-%m-%Y': re.compile("\d{2}-\d{2}-\d{4}"),

    # yyyy
    r'%Y': re.compile("\d{4}$"),

    '%Y-%m-%d %H:%M:%S': re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'),
    '%Y%m%dT%H%M%S' : re.compile('\d{8}T\d{6}'),

    '%H:%M:%S' : re.compile('\d{2}:\d{2}:\d{2}'),
}

# American Dates
__date_patterns2 = {

    '%m/%d' : re.compile( r'^\d{2}/\d{2}$', re.M),

    # 'yyyy-mm-dd'
    '%Y-%m-%d': re.compile("\d{4}-\d{2}-\d{2}"),

    '%Y/%m/%d': re.compile("\d{4}/\d{2}/\d{2}"),

    # yyyymmdd
    '%Y%m%d' : re.compile('\d{8}$'),

    # /mm/dd/yy
    '%m/%d/%y': re.compile("\d{2}/\d{2}/\d{2}$"),

    # /mm/dd/yyyy
    '%m/%d/%Y': re.compile("\d{2}/\d{2}/\d{4}"),


    '%d-%m-%Y': re.compile("\d{2}-\d{2}-\d{4}"),

    # yyyy
    r'%Y': re.compile("\d{4}$"),

    '%Y-%m-%d %H:%M:%S': re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'),
    '%Y%m%dT%H%M%S' : re.compile('\d{8}T\d{6}'),

    '%H:%M:%S' : re.compile('\d{2}:\d{2}:\d{2}'),
}


def parse_date(datestr):
    """
    Parse date string

    :param datestr:
    :return:

    Convention: Day before Month
    """
    for fmt, pat in __date_patterns.iteritems():
            if pat.match(datestr):

                #print "-----------------"
                #print "datestr = ", datestr, "fmt = ", fmt

                return datetime.strptime(datestr, fmt)
                #return datetime.strptime(datestr, fmt)

                #print "-----------------"

def parse_date2(datestr):
    """
    Parse Americam date string

    :param datestr:
    :return:

    Convention: Month before day
    """
    for fmt, pat in __date_patterns2.iteritems():
            if pat.match(datestr):

                #print "-----------------"
                #print "datestr = ", datestr, "fmt = ", fmt

                return datetime.strptime(datestr, fmt)


def dtime(*param):
    """
    DateNumber = dtime(t)example
    DateNumber = dtime(DateString)
    DateNumber = dtime(DateString,formatIn)example
    DateNumber = dtime(DateString,PivotYear)
    DateNumber = dtime(DateString,formatIn,PivotYear)example
    DateNumber = dtime(DateVector)example
    DateNumber = dtime(Y,M,D)example
    DateNumber = dtime(Y,M,D,H,MN,S)

    :param param:
    :return:
    """

    if len(param) ==  1:

        if isinstance(param[0], datetime):
            return param[0]

        if param[0] == 'now':
            return datetime.now()

        datestr = param[0]

        if dtime.flag:
            return parse_date(datestr)
        else:
            return parse_date2(datestr)

    if len(param) >= 3:
        return datetime(*param)

dtime.flag = False
