#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tabulate import tabulate
from m2py.finance import dtime
from m2py.finance import daycounting


from matplotlib import pyplot as plt


class Tserie:

    def __init__(self, time, data, headers=[], name="", description="", dataprovider="", url=""):
        self.time = time
        self.data = data
        self.format = "%Y-%m-%d"
        self.headers = ['time']
        self.headers.extend(headers)
        self.description = description
        self.name = name
        self.dataprovider = dataprovider
        self.url = url

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
        c.writerow(["Data Provider: {}".format(self.dataprovider)])
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
        s['dataprovider'] = self.dataprovider
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
        dataprovider  = s['dataprovider']
        url  = s['url']
        description  = s['description']
        headers  = s['headers']
        time  = s['time']
        data  = s['data']

        new = Tserie(time, data, headers, name, description, description, dataprovider)
        new.headers.pop(0)

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

    @classmethod
    def show(cls):
        plt.show()

    def info(self):

        print "Name:           ", self.name
        print "Description:    ", self.description
        print "Data Provider:  ", self.dataprovider
        print "URL:            ", self.url
        print "Headers:  ", self.headers
        print "Rows:     ", len(self.time)


def product(factors):
    import operator
    return reduce(operator.mul, factors)

def cumproduct(vector):
    """
    :param vector:
    :return:
    """
    rng = xrange(1, len(vector)+1)
    #return map(lambda i: round(product(vector[0:i]), 8), rng)
    return map(lambda i: product(vector[0:i]), rng)
