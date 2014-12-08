#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://nf.nci.org.au/facilities/software/Matlab/techdoc/ref/datestr.html

"""

import re
from datetime import datetime


__date_patterns = {

    '%d/%m' : re.compile( r'^\d{2}/\d{2}$', re.M),

    # 'yyyy-mm-dd'
    '%Y-%m-%d': re.compile("\d{4}-\d{2}-\d{2}"),

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



def main():
    print dtime("03/01")

    print dtime("2010-10-08")

    print dtime("03/01/2000")

    print dtime("08-10-2010")

    print dtime("2010")

    # yyyyddmm
    print dtime('20100103')

    print dtime('15:45:17')


    print dtime('20000301T15:45:17')


    print dtime('now')

    print dtime(2001, 12, 19)

    #print datetime.strptime("apr", "%b")

    #print parse_date('2000-03-01 15:45:17')

if __name__ == "__main__":
    main()