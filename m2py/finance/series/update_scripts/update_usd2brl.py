#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""


import os
import utils
from pprint import pprint

import scraplib as s
import m2py.finance.dtime as dt

from m2py.finance.timeserie import Tserie

import matplotlib.pyplot as plt

import json

baseurl = "https://www.debit.com.br/"
url = "https://www.debit.com.br/consulta20.php?indexador=12&imes=01&iano=2000&fmes=12&fano=2014"


# Get column i, from a matrix: list of tuples or list
column = lambda m, i: map(lambda e: e[i], m)

# Get Transpose Matrix
transpose = lambda M: zip(*M)

make_dict = lambda headers, columns: dict(zip(headers, columns))

def get_nextlink():
    try:
        page= s.data.xpath('//div[@class="listagem_paginacao"]//a')[1].attrib['href']
        return os.path.join(baseurl, page)
    except:
        return ""


data = []

s.scrap(url)
page0 = s.data.xpath('//div[@class="listagem_paginacao"]//a')[0].attrib['href']
link = os.path.join(baseurl, page0)


while True:

    dates= s.xlist('//td[@class="ta-left"]')
    values = s.xlist('//td[@class="ta-right"]')
    data.extend(zip(dates, values))

    pprint(zip(dates, values)[0:10])

    s.scrap(link)
    link = get_nextlink()

    print "Next = ", link

    if not link:
        break

    print "----------"

_dates = column(data, 0)
values= column(data, 1)

dates  = map( lambda d: dt.date_dmy(d, '/'), _dates)
values = map( lambda s: float(s.replace(',', '.')), values)


usd2brl = Tserie(dates, [values ], headers=["rate"],
                 name="usd2brl",
                 description="Dollar to BRL exchange Rate",
                 dataprovider="https://www.debit.com.br",
                 url="https://www.debit.com.br/consulta20.php?indexador=12&imes=01&iano=2000&fmes=12&fano=2014",
                 )

thisdir = utils.this_dir()
datasets = utils.resource_path("datasets")
usd2brl.to_csv(os.path.join(thisdir, "../datasets", "usd2brl.csv"))

# dict_data = {
#     'dates' : map(lambda x: dt.date2str_ymd(x, '-'), dates),
#     'values' : values,
# }
#
