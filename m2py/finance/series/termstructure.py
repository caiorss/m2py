#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from m2py.finance import dtime


safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"

headers = {
    'User-Agent': safari
}

url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp'

payload = {
      'Data'  : '13/06/2013',
      'Data1' : '20141207',
      'slcTaxa': 'PRE',
}


from lxml import etree
from lxml.etree import ElementTree as ET
#parser = lxml.etree.(recover=True)


r = requests.get(url, data=payload, headers=headers)


from bs4 import BeautifulSoup

soup = BeautifulSoup (r.text)

table = soup.findAll("table")

table = str(table[1])
tree = ET(etree.fromstring(table)).getroot()

t = tree.xpath('//td[@class="tabelaConteudo1" or @class="tabelaConteudo2"]')

d = [t.text.strip().replace(',', '.') for t in t]

rows = [ (d.pop(0), d.pop(0), d.pop(0), )  for r  in d  ]
columns = list(zip(*rows))

from numpy import array, log

terms = array(list(map(int, columns[0])))
rates = array(list(map(float, columns[1])))


log_pu = (1+rates)**(terms/252.0)

# import matplotlib.pyplot as plt
#
# plt.plot(terms, rates)
# plt.show()

#import utils
#out = utils.run("w3m -dump '%s'" % url)




# http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data=13/06/2013&Data1=20141207&slcTaxa=PRE