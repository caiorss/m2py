#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download Brazilian Financial, Economic and Statistical data From IPEA

Institute of Applied Economic Research of Brazil ( Instituto de Pesquisa Econômica Aplicada)
http://www.ipeadata.gov.br

"""


def __download(url):
    import requests

    payload = {
        'bar_oper': 'oper_exibeseries',
        'oper': 'exportCSVUS',
    }
    # url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=36482&module=M"
    r = requests.post(url, data=payload)
    return r.text


def _download_dataset(dataset):
    url = datasets_collection[dataset]["url"]
    data = __download(url)
    return data


def read_csv_string(csvstring, skipline=None, colmax=None):
    return [x.strip().split(",")[:colmax] for x in csvstring.strip().splitlines()[skipline:]]


def show_dataset():
    for key, data in datasets_collection.items():
        print("Dataset: ", key)
        print(data["short"])
        print("\n")


def show_description():
    import re

    for key, data in datasets_collection.items():
        print("Dataset: ", key)

        print(data["description"])

        print(data["url"])

        print(70 * "-")
        print("")


def _getIPCA():
    from datetime import datetime

    data = _download_dataset("IPCA")
    data = read_csv_string(data, 1, 2)

    # Column Data Types
    date = lambda ds: datetime.strptime(ds, "%Y.%m")
    types =  [ date, float ]

    data = [ list(map(converter, column)) for converter, column in  zip(types, list(zip(*data)))]

    return data

def _getLTN():
    from datetime import datetime

    data = _download_dataset("LTN")
    data = read_csv_string(data, 1, 2)

    # Column Data Types
    date = lambda ds: datetime.strptime(ds, "%Y.%m")
    types =  [ date, float ]

    data = [ list(map(converter, column)) for converter, column in  zip(types, list(zip(*data)))]

    return data


def _getTR():
    from datetime import datetime

    data = _download_dataset("TR")
    data = read_csv_string(data, 1, 2)

    data  = [x for x in data if x[1]]

    date = lambda ds: datetime.strptime(ds, "%d/%m/%Y")
    types =  [ date, float ]
    data = [ list(map(converter, column)) for converter, column in  zip(types, list(zip(*data)))]
    return data


def _getCDB():
    from datetime import datetime

    data = _download_dataset("CDB_PREFIXADO")
    data = read_csv_string(data, 1, 2)

    data  = [x for x in data if x[1]]

    date = lambda ds: datetime.strptime(ds, "%Y.%m")
    types =  [ date, float ]
    data = [ list(map(converter, column)) for converter, column in  zip(types, list(zip(*data)))]
    return data

def _getUSD_BRL_ASK():
    from datetime import datetime

    data = _download_dataset("USD_BRL_EXCHANGE_ASK")
    data = read_csv_string(data, 1, 2)

    data  = [x for x in data if x[1]]

    date = lambda ds: datetime.strptime(ds, "%d/%m/%Y")
    types =  [ date, float ]
    data = [ list(map(converter, column)) for converter, column in  zip(types, list(zip(*data)))]
    return data


def _getPOUPANCA():
    from datetime import datetime

    data = _download_dataset("POUPANCA")
    data = read_csv_string(data, 1, 2)

    data  = [x for x in data if x[1]]

    date = lambda ds: datetime.strptime(ds, "%Y.%m")
    types =  [ date, float ]
    data = [ list(map(converter, column)) for converter, column in  zip(types, list(zip(*data)))]
    return data


def download(dataset):
    handler = datasets_collection[dataset]["handler"]
    return handler()



datasets_collection = {
    "IPCA": {
        'short': 'Indice de Preços ao Consumidor',

        'description': \
            """
IPCA - geral - índice (dez. 1993 = 100)
Frequência: Mensal de 1979.12 até 2014.11
Fonte: Instituto Brasileiro de Geografia e Estatística, Sistema Nacional de Índices de Preços ao Consumidor (IBGE/SNIPC)
Unidade: -
Comentário: Índice Nacional de Preços ao Consumidor Amplo (IPCA). Obs.: O índice de agosto de 1991, excepcionalmente, foi calculado pelo IBGE como média geométrica dos valores observados em julho e setembro. Por isso, as taxas de variação apresentadas para agosto e setembro de 1991 são iguais.
Atualizado em: 08/12/2014
            """,
        'url': 'http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=36482&module=M',
        'handler' : _getIPCA,
    },

    "POUPANCA": {
        'short': 'Brazilian Saving Account Interest Rate ',

        'description': \
            """
Poupança: rendimento nominal - 1º dia útil
Frequência: Mensal de 1990.01 até 2014.11
Fonte: Associação Brasileira das Entidades dos Mercados Financeiro e de Capitais (Anbima)
Unidade: (% a.m.)
Comentário: Refere-se ao rendimento do primeiro dia útil do mês.
Atualizado em: 11/12/2014
             """,

        "url": "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=31878&module=M",

        'handler' : _getPOUPANCA,

    },
    "TR": {
        'short': 'TR Interst Rate',

        'description': \
            """
Taxa de juros: TR
Frequência: Diária de 04/01/1999 até 10/12/2014
Fonte: Banco Central do Brasil, Sistema Gerenciador de Séries Temporais (BCB outras/SGS)
Unidade: (% a.m.)
Comentário: Taxa Referencial de juros (TR). Obs.: Percentagem no período de 30 dias iniciado na data de referência.
Atualizado em: 11/12/2014
http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38597&module=M
        """,

        "url": "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38597&module=M",

        "handler" : _getTR,
    },

    "USD_BRL_EXCHANGE_ASK": {

        'short': 'USD/ BRL Exchange Rate Ask Price',


        'description': \
            """
Taxa de câmbio comercial para compra: real (R$) / dólar americano (US$) - média
Frequência: Diária de 02/01/1985 até 11/12/2014
Fonte: Banco Central do Brasil, Sistema Gerenciador de Séries Temporais (BCB outras/SGS)
Unidade: R$
Atualizado em: 11/12/2014
            """,

        'url': 'http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M',


        'handler' : _getUSD_BRL_ASK,
    },


    "CDB_PREFIXADO": {
        'short': "Taxa de juros: CDB pré-fixado",

        "description": \
            """
Taxa de juros: CDB pré-fixado
Frequência: Mensal de 1984.02 até 2004.04
Fonte: Associação Brasileira das Entidades dos Mercados Financeiro e de Capitais (Anbima)
Unidade: (% a.m.)
Comentário: Certificado de Depósito Bancário (CDB) pré-fixado de 30 dias. Para cálculo do rendimento, utiliza-se a taxa líquida do primeiro dia útil do mês. Série descontinuada pela fonte.
Atualizado em: 01/06/2004
        """,

        "url": "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=31876&module=M",
        
        "handler" : _getCDB,
    },

    "LTN": {
        "short": "Estrutura a termo da taxa de juros prefixadas LTN - prazo 1 mês",

        "description": \
            """
Frequência: Mensal de 2000.05 até 2014.11
Fonte: Associação Brasileira das Entidades dos Mercados Financeiro e de Capitais (Anbima)
Unidade: (% a.a.)
Comentário: Estrutura a termo da taxa de juros prefixadas calculada tendo como base a curva do LTN. Obs: prazo em 21 dias úteis (1 mês) .
Atualizado em: 11/12/2014
        """,

        "url": "http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=1711885175&module=M",
        
        'handler' : _getLTN,

    }

}

