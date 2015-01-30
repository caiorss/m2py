#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# !/usr/bin/env python2

# http://download.finance.yahoo.com/d/quotes.csv?s=USDBRL=X&f=sl1d1t1c1ohgv&e=.csv


from requests import request
import requests
from utils3 import Chain

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


def stock_historical_data(symbol):
    """
    :param symbol: Stock/ Ticker Symbol
    :return:       Dictionaries with the keys  (Dates, Open, High, Low, Close, AdjClose, Volume)

    Example:
    >>> data = stock_historical_data("PETR4.SA")

    >>> data.keys()
    dict_keys(['Close', 'Low', 'High', 'Date', 'Adj Close', 'Open', 'Volume'])

    """

    #url = "http://ichart.finance.yahoo.com/table.csv?s={}&c={}"
    url = "http://ichart.finance.yahoo.com/table.csv?s={}".format(symbol)
    #url = url.format("PETR4.SA")

    req = requests.get(url)
    data = req.text
    lines= data.splitlines()
    headers = lines[0].split(",")
    table = Chain(lines[1:]).reverse().split(",")

    Date = table.select_pos(0).to_date_ymd("-").list
    Open  = table.select_pos(1).to_float().list
    High  = table.select_pos(2).to_float().list
    Low   = table.select_pos(3).to_float().list
    Close = table.select_pos(4).to_float().list
    Volume = table.select_pos(5).to_int().list
    AdjClose = table.select_pos(5).to_float().list

    columns =  Date, Open, High, Low, Close, Volume, AdjClose

    return dict(zip(headers, columns))


def plot_historical_data(symbol):
    from matplotlib import pyplot

    data = stock_historical_data(symbol)
    pyplot.plot(data["Date"], data["Close"])


