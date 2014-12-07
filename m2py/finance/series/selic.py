#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

curl -d "dataInicial=01/07/2000&dataFinal=07/12/2014&method=listarTaxaDiaria&tipoApresentacao=arquivo&Submit=Consultar" \
-A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) \
Chrome/12.0.742.112 Safari/534.30" http://www3.bcb.gov.br/selic/consulta/taxaSelic.do


dataInicial	01/07/2000
dataFinal	01/07/2003
method	listarTaxaDiaria
tipoApresentacao	arquivo
Submit	    Consultar

"""

import requests

safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"

headers = {
    'User-Agent': safari
}

# r= requests.post("http://echo.httpkit.com", data=payload, headers=headers)



def get_selic_raw_data(start_date, end_date):
    """
    Get daily SELIC brazilian rate


    :param start_date:  Start date in dd/mm/yyyy format
    :param end_date:    Start date in dd/mm/yyyy format
    :return:            Selic raw data in text format
    :type start_date:   str
    :type end_date:     str
    :rtype:             str
    """
    payload = {
        "dataInicial": start_date,
        "dataFinal": end_date,
        "method": "listarTaxaDiaria",
        "tipoApresentacao": "arquivo",
        "Submit": "Consultar",
    }

    r = requests.post("http://www3.bcb.gov.br/selic/consulta/taxaSelic.do", data=payload, headers=headers)
    return r.text.strip()


def skiplines(text, N):
    data = "\n".join(text.splitlines()[N:])
    return data


def comma_to_dot(text):
    import re

    return re.sub(",", ".", text)


def splitcsv(text, separator=",", columnrange=0):
    if not columnrange:
        return map(lambda x: filter(lambda x: x, x.split(separator)), text.splitlines())
    else:
        return map(lambda x: filter(lambda x: x, x.split(separator)[:columnrange]), text.splitlines())


def trasnpose(lst):
    return zip(*lst)


def product(factors):
    import operator

    return reduce(operator.mul, factors)


def process_raw_data(text):
    text = skiplines(text, 2)
    text = comma_to_dot(text)
    text = splitcsv(text, ";", 2)
    columns = trasnpose(text)
    return columns


def parse_columns(columns):
    import m2py.finance.dtime as dt

    dates = map(dt.date_dmy, columns[0])
    rates = map(float, columns[1])
    return dates, rates


def get_selic(start_date, end_date):
    #text = get_selic_raw_data("01/01/2013", "7/12/2014")
    text = get_selic_raw_data(start_date, end_date)
    columns = process_raw_data(text)
    return parse_columns(columns)


import os
import shelve

if not os.path.isfile("selic.dat"):
    dates, rates = get_selic("01/07/2000", "07/12/2014")

    f = shelve.open("selic.dat")
    f['dates'] = dates
    f['rates'] = rates
    f.close()
else:
    f = shelve.open("selic.dat")
    dates = f['dates']
    rates = f['rates']


from tabulate import tabulate
from m2py.finance import dtime
from m2py.finance import daycounting


from matplotlib import pyplot as plt


class Tserie:

    def __init__(self, time, data, headers=[], name="", description=""):
        self.time = time
        self.data = data
        self.format = "%Y-%m-%d"
        self.headers = ['time']
        self.headers.extend(headers)
        self.description = description
        self.name = name
        self.datprovider = ""
        self.url = ""

    def get_table(self):
        table = [self.time]
        map(table.append, self.data)
        table = zip(*table)
        return table

    def get_table_formated(self):
        times = map(lambda d: d.strftime(self.format), self.time)
        table = [times]
        map(table.append, self.data)
        table = zip(*table)
        return table

    def __str__(self):
        return tabulate(self.get_table_formated())

    def head(self, n=10, out=True):
        import m2py.finance.dtime as dt

        times = map(lambda d: dt.date2str_ymd(d, "-"), self.time)

        table = [times]
        map(table.append, self.data)

        #print table

        #print len(table)

        table = zip(*table)[:n]
        print tabulate(table, headers=self.headers)


    def tail(self, n=10, out=True):
        import m2py.finance.dtime as dt
        times = map(lambda d: dt.date2str_ymd(d, "-"), self.time)
        table = [times]
        map(table.append, self.data)


        table = zip(*table)[-n:]
        print tabulate(table, headers=self.headers)

    def start(self):
        table = [self.time]
        map(table.append, self.data)
        return zip(*table)[0]

    def end(self):
        table = [self.time]
        map(table.append, self.data)
        return zip(*table)[-1]

    def date_range(self, start_date, end_date):

        start_date = dtime.date_dmy(start_date)
        end_date = dtime.date_dmy(end_date)

        table = [self.time]
        map(table.append, self.data)
        table = zip(*table)

        table2 = filter(lambda d: start_date <= d[0] <= end_date, table)

        table2 = zip(*table2)

        return Tserie(time=table2[0], data=table2[1:])

    def get_date(self, date, prevbusday=False):
        date = dtime.date_dmy(date)
        table = self.get_table()

        if prevbusday:
            date = daycounting.prevbusday(date)
        return filter(lambda d: d[0] == date, table)

    def add_column(self, column, name=''):
        self.data.append(column)
        self.headers.append(name)

    def to_csv(self, filename):
        import csv
        c = csv.writer(open(filename, "wb"))
        table = self.get_table_formated()
        c.writerow(["Name: {}".format(self.name)])
        c.writerow(["Data Provider: {}".format(self.datprovider)])
        c.writerow(["Url: {}".format(self.url)])
        c.writerow(["Description: {}".format(self.description)])
        c.writerow(self.headers)
        for row in table:
            c.writerow(row)
        #c.close()


    def to_bin(self, filename):
        """
        Save time serie as binary database
        """
        import shelve
        s = shelve.open(filename)
        s['name'] =  self.name
        s['datprovider'] = self.datprovider
        s['url'] = self.url
        s['description'] = self.description
        s['headers'] = self.headers
        s['time'] = self.time
        s['data'] = self.data
        s.close()
    
    @classmethod    
    def from_bin(cls, filename):
        """
        Load time Serie from binary database
        """
        import shelve
        s = shelve.open(filename)
        name  = s['name']
        datprovider  = s['datprovider']
        url  = s['url']
        description  = s['description']
        headers  = s['headers']
        time  = s['time']
        data  = s['data']        
        
        new = Tserie(time, data,headers, name, description)
        new.datprovider = datprovider
        new.url = url

        return new

        

    def timelenght(self):
        return (self.time[-1] - self.time[0]).days

    def column(self, name):
        if isinstance(name, int):
            return self.data[name]
        else:
            idx = self.headers.index(name)
            return self.data[idx-1]

    def columns(self, colist):
        return map(self.column, colist)

    def _plot(self, column_name):
        column = self.column(column_name)
        plt.plot(self.time, column)
        plt.xlabel("Time")
        plt.grid()
        #plt.ylabel(column_name)

    def plot(self, columns):
        map(self._plot, columns)



def cumproduct(vector):
    """
    :param vector:
    :return:
    """
    rng = xrange(1, len(vector)+1)
    #return map(lambda i: round(product(vector[0:i]), 8), rng)
    return map(lambda i: product(vector[0:i]), rng)




#print tabulate(table2)
from m2py.misc import vectorize
dailyfactor = lambda s: round((1+s/100.0)**(1/252.0), 8)
#dailyfactor = vectorize.vectf(dailyfactor)


dates = dates[:-1]
rates = rates[:-1]

factors = map(dailyfactor, rates)
#_factors = factors
#_factors[0] = 1000*factors[0]
acumfactor = cumproduct(factors)


ts = Tserie(dates,
            [rates, factors, acumfactor],
            headers=['rate', 'factor', 'accum'],
            name = "Taxa SELIC")

ts.datprovider = "Banco Central do Brasil"
ts.description = "Taxa SELIC Diaŕia desde 1/7/2000"
ts.url = "www3.bcb.gov.br/selic/consulta/taxaSelic.do?method=listarTaxaDiaria"
ts.to_csv("selic.csv")
ts.to_bin("selic.tsdat")

ts.plot(["rate"])
plt.figure()
ts.plot(["accum"])
plt.show()

def getVNA(date):
    date = dtime.date_dmy(date)
    date = daycounting.daysadd(date, -1)
    date = dtime.date2str_dmy(date)

    return round(1000.0*ts.get_date(date)[0][-1], 2)

