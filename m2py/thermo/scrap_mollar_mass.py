# http://www.convertunits.com/molarmass/H2
# id('EchoTopic')//x:big/x:b
#  
#  "//p//big//b" 
#

import urllib.request, urllib.error, urllib.parse
import lxml.etree
from tabulate import tabulate
from pprint import pprint

def url2req(url, user_agent= "Mozilla/5.0"):
    """
    Return html code to given URL
    using firefox user agent

    """
    import urllib.request, urllib.error, urllib.parse

    # Fake user agent
    #user_agent = 'Mozilla/5.0'
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(url,None,headers)
    req = urllib.request.urlopen(req)
    return req

def url2tree(url):
    data = url2req(url)
    parser = lxml.etree.HTMLParser()
    tree = lxml.etree.parse(data, parser)
    return tree

def show(xpath):
    """
    Print xpath of mutiple elements
    """
    dat = [u.text for u in data.xpath(xpath)]
    #pprint(dat)
    return dat

#data = url2tree(r"http://www.convertunits.com/molarmass/H2")
#d = data.xpath(r"""id('EchoTopic')//x:big/x:b""")


def get_molar_mass(chemformula):
    """
    Get molar mass in kg/mol
    """
    url = r"http://www.convertunits.com/molarmass/%s" % chemformula
    data = url2tree(url)
    txt = data.xpath("//p//b")[0].text
    print("Got %s >>> %s" % (chemformula, txt))
    
    mass = float(txt.split()[0])/1000.0
    try:
        return mass
    except:
        return None

