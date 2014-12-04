#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import array
import datetime
from tabulate import tabulate
import matplotlib.pylab as plt


class TimeSerie:
    def __init__(self, headers=['ts'], **kwargs):

        self._fields = {}

        for k in kwargs.keys():
            self._fields[k] = array(kwargs[k])

        self._headers = headers
        self.date_format = "%d-%m-%Y"

    def addfield(self, label, data):
        self._fields[label] = data

    def datefmt(self, date_format):
        self.date_format = date_format

    @property
    def ts(self):
        return self._fields['ts']

    @property
    def start(self):
        return self.ts[0]

    @property
    def end(self):
        return self.ts[-1]

    @property
    def headers(self):
        if not self._headers:
            return self._fields.keys()
        else:
            return self._headers

    def index(self, i):
        return map(lambda x: x[i], map(self._fields.get, self._headers))


    def date_range(self, start_date, end_date):
        pass


    def head(self, n=10, out=True):

        table = map(self._fields.get, self._headers)
        table = zip(*table)[:n]

        if out:
            print tabulate(table, headers=self._headers)
        else:
            return table

    def tail(self, n=10, out=True):
        table = map(self._fields.get, self._headers)
        table = zip(*table)[-n:]

        if out:
            print tabulate(table, headers=self._headers)
        else:
            return table


    def plot(self, field, title="", xlabel="", ylabel="", show=False):
        plt.plot(self.ts, self._fields[field])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if show:
            plt.show()


    def to_json(self):
        import json

        ts = map(lambda x: (x.year, x.month, x.day), self.ts)
        columns = map(lambda x: self._fields.get(x).tolist(), self.headers[1:])

        data = dict(zip(self.headers[1:], columns))
        data['ts'] = ts
        data['headers'] = self.headers
        #table = zip(ts, *columns)
        #data = dict(table=table, headers=self.headers)
        return json.dumps(data)

    def to_jsonf(self, filename):
        fp = open(filename,'w')
        fp.write(self.to_json())
        fp.close()

    @classmethod
    def from_json(cls, jsonstr):
        import json
        data = json.loads(jsonstr)
        headers = data.pop('headers')
        t= TimeSerie(headers=headers, **data)
        return t

    @classmethod
    def from_jsonf(self, filename):
        jsonstr = open(filename).read()
        return self.from_json(jsonstr)





def dic2tms(dic, header):
    """
    :param dic:
    :param ts_field:
    :param headers:
    :return:
    """

    t = TimeSerie(ts=dic.pop(header[0]))


