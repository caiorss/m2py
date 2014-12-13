#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

curl -d "dataInicial=01/07/2000&dataFinal=07/12/2014&method=listarTaxaDiaria&tipoApresentacao=arquivo&Submit=Consultar" \
-A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) \
Chrome/12.0.742.112 Safari/534.30" http://www3.bcb.gov.br/selic/consulta/taxaSelic.do


dataInicial 01/07/2000
dataFinal   01/07/2003
method  listarTaxaDiaria
tipoApresentacao    arquivo
Submit      Consultar

"""

import requests
import os
from m2py.finance.timeserie import Tserie, cumproduct
from m2py.finance import dtime


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


def build_database():
    import utils

    now = dtime.date2str_dmy(dtime.dtime('now'), '/')

    print "Downloading Database to : ", now

    dates, rates = get_selic("01/07/2000", now)
    dates = dates[:-1]
    rates = rates[:-1]


    dailyfactor = lambda s: round((1+s/100.0)**(1/252.0), 8)
    factors = map(dailyfactor, rates)
    VNA = cumproduct(factors)
    VNA.insert(0, 1.0)
    VNA = VNA[:-1]
    VNA= map(lambda x: x*1000.0, VNA)


    ts = Tserie(dates,
                [ rates, factors, VNA],
                headers=['rate', 'factor', 'VNA'],
                name = "Taxa SELIC")



    ts.datprovider = "Brazil Central Bank (Banco Central do Brasil)"
    ts.description = "Brazilian Daily Interest Rate Since 1/7/2000"
    ts.url = "www3.bcb.gov.br/selic/consulta/taxaSelic.do?method=listarTaxaDiaria"

    thisdir = utils.this_dir()
    datasets = utils.resource_path("datasets")

    ts.to_csv(os.path.join(thisdir, "../datasets", "selic.csv"))
    #ts.to_bin("selic.tsdat")


if __name__ == "__main__":
    build_database()



