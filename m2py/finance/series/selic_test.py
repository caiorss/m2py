#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify in: http://www.anbima.com.br/vna/vna.asp

"""

from m2py.finance import dtime
#from m2py.finance import dtime
from m2py.finance.timeserie import Tserie

import requests

from utils import resource_path

safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"

headers = {
    'User-Agent': safari
}

selic = Tserie.from_bin(resource_path("selic2.tsdat"))


#ts.info()

#ts.head()

#ts.tail()
#
#ts.plot(['rate'])
#ts.plot(['accum'])
#ts.to_csv("selic2.txt")
#ts.show()




def get_vna(date):
    #date = dtime.date_dmy(date)
    date = dtime.dtime(date)

    #print "Date ", date
    #date = dtime.daysadd(date, -1)
    date = dtime.prevbusday(date)

    #print "date = ", date
    data = selic.get_date(date)
    #print "data = ", data
    return round(data[0][-1], 8), date




def selic_acfactor(start_date, end_date):
    """
    Get daily SELIC brazilian treasury bond rate accumulated factor


    :param start_date:  Start date in dd/mm/yyyy format
    :param end_date:    Start date in dd/mm/yyyy format
    :return:            Selic raw data in text format
    :type start_date:   str
    :type end_date:     str
    :rtype:             str
    """
    payload = {
    "indicadorConsulta": "periodo",
    "dataInicial":  start_date,
    "dataFinal":    end_date,
    "tipoApresentacao": "arquivo",
    "Submit": "Consultar",
    }
    url =  "http://www3.bcb.gov.br/selic/consulta/taxaSelic.do?method=listarFatoresAcumulados"
    r = requests.post(url, data=payload, headers=headers)

    return float(r.text.strip().splitlines()[-1].split(';')[-2].replace(",", "."))

def get_vna_bc(date):
    date = dtime.dtime(date)
    date = dtime.date2str_dmy(date, '/')
    return 1000.0*selic_acfactor("01/07/2000", date)


#print getVNA("16/11/2014")
