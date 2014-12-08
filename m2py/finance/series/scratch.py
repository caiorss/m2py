#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"

headers = {
    'User-Agent': safari
}

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

def get_selicVNA(date):
    return selic_acfactor("01/07/2000", date)


#print get_selicVNA("01/10/2007")
