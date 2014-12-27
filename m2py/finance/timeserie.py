#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tabulate import tabulate
from m2py.finance import dtime

from matplotlib import pyplot as plt

import numpy
from functools import reduce


def lst2array(obj):
    if isinstance(obj, numpy.ndarray):
        return obj
    else:
        return numpy.array(obj)


def sprint(txt, *args):
    return txt + "".join(map(str, args)) + '\n'


class Tserie:
    """
    Class To Manipulate Time Serie Object
    """

    def __init__(self, time, data, headers=[], name="", description="", dataprovider="", url=""):

        self.time = lst2array(time)
        self.data = list(map(lst2array, data))
        self.format = "%Y-%m-%d"
        self.headers = ['time']
        self.headers.extend(headers)
        self.description = description
        self.name = name
        self.dataprovider = dataprovider
        self.url = url
        self.serie_type = 'tserie'  # type 1 - Time serie , type 2 date range serie

    def __getitem__(self, item):

        if isinstance(item, int):

            if item > 1:
                return self.data[item-1]
            elif item == -1:
                return self.data[-1]
            else:
                return self.time

        elif isinstance(item, str):

            if item == "time":
                return self.time
            else:
                return self.column(item)

        #return self.data[self.headers.index(item)]

    def copy(self):

        t = Tserie(self.time, self.data, self.headers, self.name, self.description, self.dataprovider, self.url)
        t.format = self.format
        t.headers.pop(0)
        return t

    def get_table(self):
        table = [self.time]
        list(map(table.append, self.data))
        table = list(zip(*table))
        return table

    def time_formated(self):
        if self.serie_type == "tserie":
            times = [d.strftime(self.format) for d in self.time]
        else:
            times = self.time

        return times

    def get_table_formated(self):

        times = self.time_formated()
        table = [times]
        list(map(table.append, self.data))
        table = list(zip(*table))
        return table

    def __str__(self):
        return tabulate(self.get_table_formated())


    def head(self, n=10, out=True):
        """
        Shows the first ten lines from the dataset

        :param n:
        :param out:
        :return:
        """

        # times = map(lambda d: dt.date2str_ymd(d, "-"), self.time)
        times = self.time_formated()

        table = [times]
        list(map(table.append, self.data))

        #print table

        #print len(table)

        table = zip(*table)[:n]
        print(tabulate(table, headers=self.headers))


    def tail(self, n=10, out=True):
        """
        Shows the last ten lines from the dataset

        :param n:
        :param out:
        :return:
        """
        # import m2py.finance.dtime as dt

        #times = map(lambda d: dt.date2str_ymd(d, "-"), self.time)


        times = self.time_formated()
        table = [times]
        list(map(table.append, self.data))

        table = zip(*table)[-n:]

        print("")
        print(tabulate(table, headers=self.headers))
        print("")

    def start(self):
        table = [self.time]
        list(map(table.append, self.data))
        return zip(*table)[0]

    def end(self):
        table = [self.time]
        list(map(table.append, self.data))
        return zip(*table)[-1]

    def date_range(self, start_date, end_date):

        if self.serie_type == "rserie":
            return None

        start_date = dtime.date_dmy(start_date)
        end_date = dtime.date_dmy(end_date)

        table = [self.time]
        list(map(table.append, self.data))
        table = list(zip(*table))

        table2 = [d for d in table if start_date <= d[0] <= end_date]

        table2 = list(zip(*table2))

        return Tserie(time=table2[0], data=table2[1:])

    def get_time_range(self):
        return self.time[0], self.time[-1]


    def get_date(self, date, prevbusday=False):

        if self.serie_type == "rserie":
            return None

        date = dtime.dtime(date)
        table = self.get_table()

        if prevbusday:
            date = dtime.prevbusday(date)

        return [d for d in table if d[0].day == date.day and d[0].month == date.month
                                and d[0].year == date.year]

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
            # c.close()
    @classmethod
    def from_csv(cls, filename):

        import csv
        fp = open(filename, "rb")

        name = fp.readline().split(":")[1].strip()
        dataprovider = fp.readline().split(":")[1].strip()
        url = fp.readline().strip().split(":")[1].strip()
        description = fp.readline().strip().split(":")[1].strip()
        headers = [x.strip() for x in fp.readline().strip().split(",")]

        column = lambda m, i: [e[i] for e in m]

        rows = list(csv.reader(fp))

        data = [column(rows, i) for i in range(len(headers))]
        time = data.pop(0)
        time = [dtime.date_ymd(d, '-') for d in time]

        data = [list(map(float, c)) for c in data]

        #headers.pop(0)

        fp.close()
        new = Tserie(time, data, headers, name, description, dataprovider)
        new.url = url
        new.headers.pop(0)
        return new



    def to_bin(self, filename):
        """
        Save time serie as binary database
        """
        import shelve

        s = shelve.open(filename)
        s['name'] = self.name
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
        name = s['name']
        dataprovider = s['dataprovider']
        url = s['url']
        description = s['description']
        headers = s['headers']
        time = s['time']
        data = s['data']
    
        new = Tserie(time, data, headers, name, description, dataprovider)
        new.url = url
        
        new.headers.pop(0)

        return new

    def timelenght(self):
        if self.serie_type == "tserie":
            return (self.time[-1] - self.time[0]).days

        elif self.serie_type == "rserie":
            return self.time[-1]

    def timedureation(self):
        return dtime.duration360days(self.timelenght())


    def column(self, name):
        if isinstance(name, int):
            return self.data[name]
        else:
            idx = self.headers.index(name)
            return self.data[idx - 1]

    def columns(self, colist):
        return list(map(self.column, colist))

    def _plot(self, column_name):
        column = self.column(column_name)
        plt.plot(self.time, column)
        plt.xlabel("Time")
        plt.grid()
        # plt.ylabel(column_name)

    def plot(self, columns, xlabel="", ylable="", title=""):

        if isinstance(columns, list):
            list(map(self._plot, columns))
        else:
            self._plot(columns)

        plt.xlabel(xlabel)
        plt.ylabel(ylable)
        plt.title(title)
        plt.grid()


    def time2offset(self):
        return dtime.date2ofsset(self.time)

    def time2offset_bu(self):
        return dtime.date2offset_bu(self.time)

    def time_range_serie(self):
        time_offset = self.time2offset()
        serie = self.copy()
        serie.time = numpy.array(time_offset)
        serie.serie_type = "rserie"
        return serie

    def time_range_serie_bu(self):
        time_offset = self.time2offset_bu()
        serie = self.copy()
        serie.time = numpy.array(time_offset)
        serie.serie_type = "rserie"
        return serie

    @classmethod
    def show(cls):
        plt.show()

    def info(self):

        print("\n")
        print("Name:           ", self.name)
        print("Description:    ", self.description)
        print("Data Provider:  ", self.dataprovider)
        print("URL:            ", self.url)
        print("Headers:        ", self.headers)
        print("Time lenght     ", self.timelenght(), "  days")
        print("Duration         {} years, {} month {} days".format(*self.timedureation()))
        print("Type:           ", self.serie_type)
        print("Rows:           ", len(self.time))
        print("\n")


    def __repr__(self):

        text = "\n"
        text = sprint(text, "Name:           ", self.name)
        text = sprint(text, "Description:    ", self.description)
        text = sprint(text, "Data Provider:  ", self.dataprovider)
        text = sprint(text, "URL:            ", self.url)
        text = sprint(text, "Headers:        ", str(self.headers))
        text = sprint(text, "Time lenght     ", self.timelenght(), "  days")
        text = sprint(text, "Duration         {} years, {} month {} days".format(*self.timedureation()))
        text = sprint(text, "Type:           ", self.serie_type)
        text = sprint(text, "Rows:           ", len(self.time))
        text += '\n'
        return text


def product(factors):
    import operator

    return reduce(operator.mul, factors)


def cumproduct(vector):
    """
    :param vector:
    :return:
    """
    rng = range(1, len(vector) + 1)
    # return map(lambda i: round(product(vector[0:i]), 8), rng)
    return [product(vector[0:i]) for i in rng]


def plot_against(serie1, serie2, columns, title="", xlabel="Date", labels =[] ):
    """

    :param serie1:
    :param serie2:
    :type serie1: Tserie
    :type serie2: Tserie
    :param columns:
    :return:
    """

    c1, c2 = columns

    if not labels:
        L1 = serie1.name
        L2 = serie2.name
    else:
        L1, L2 = labels

    fig, ax1 = plt.subplots()
    ax1.plot(serie1.time, serie1[c1], 'b')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(L1)
    ax1.set_title(title)

    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(serie2.time, serie2[c2], 'r')
    ax2.set_ylabel(L2)

    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    plt.xlabel("Date")


    plt.grid()



