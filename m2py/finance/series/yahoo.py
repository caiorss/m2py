#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# !/usr/bin/env python2

# http://download.finance.yahoo.com/d/quotes.csv?s=USDBRL=X&f=sl1d1t1c1ohgv&e=.csv


from requests import request

from m2py.finance import dtime


yahoo_apiurl = "http://download.finance.yahoo.com/d/quotes.csv?s={symbols}&f={settings}&e=.csv"


def yahoo_url(symbols, settings):
    url = yahoo_apiurl.format(symbols=",".join(symbols), settings="".join(settings))
    return url


def fetch_yahoo(symbols, setting):
    """
    Fetch Stock Symbols From Yahoo Web API

    :param symbols: List of Symbols.
    :param setting: Settings for Yahoo API
    :return: JSON data from the API
    """
    url = yahoo_url(symbols, setting)
    data = request("GET", url).text     # Data is in CSV Format
    data = [e.split(",") for e in data.strip("\r\n").split("\r\n")]
    return data


def stocks(symbols):
    """
    :param symbols: List of Symbols
    :return:

    """
    data = fetch_yahoo(symbols, "pc1ej4vd1")
    return data


def bovespa_stocks(symbols):
    """
    :param symbols: List of Symbols of Bovespa Stock Exchange without .SA
    :return:

    Example: symbols =  [ "VALE5", "PETR4", "BBSA3"]

    y.bovespa_stocks([ "VALE5", "PETR4", "OGXP3"])
    Out[6]:
    [['16.85', '-0.66', '0.00', '0', '18917400', '"1/29/2015"'],
     ['9.03', '-0.28', '0.00', '0', '109784800', '"1/29/2015"'],
     ['0.07', '0.00', '0.027', '-5.424B', '9102900', '"1/29/2015"']]

    """
    tickers = [x + ".SA" for x in symbols]
    data = fetch_yahoo(tickers, "pc1ej4vd1")
    return data



def historical_stock_price(symbol, year):
    """
    Fetch Stock Table containing

     ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']


    :param symbol:
    :param year:
    :return:
    """

    url = "http://ichart.finance.yahoo.com/table.csv?s={}&c={}"
    url = url.format(symbol, year)

    fd = request("GET",url)

    headers = fd.readline().strip().split(',')

    data = [x.strip().split(',') for x in fd.readlines()]
    data = list(zip(*data))

    time = [dtime.date_ymd(x, '-') for x in data[0]]

    data = data[1:]

    data = [[float(x) for x in v] for v in data]

    out = dict(list(zip(headers[1:], data)))
    out[headers[0]] = time
    out['headers'] = headers

    return out



