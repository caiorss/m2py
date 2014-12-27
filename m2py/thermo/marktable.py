
import re
import sys
from m2py.utils import Container

def process_table(lines, separator=None):
    name = lines[0].strip("NAME:").strip()
    index = lines[1].strip("INDEX:").split(',')
    index =  [x.strip() for x in index]
    
    lines = lines[2:]
    data = Container()
    data.index = index
    
    for ind in index:
        data[ind] = []
       
    addl = lambda x, y: data[x].append(y)
    
    for lin in lines:        
        fields = list(map(float, lin.split(separator)))
        list(map( lambda k: addl(k[0], k[1]), list(zip(index, fields))))
            
    return name, data


def read_data_tables(filename, separator=None):
    filesignature = "!TABLEDATA"

    fp = open(filename)

    line0 = fp.readline().strip()
    
    #print line0

    if line0 != filesignature:
        raise Exception("Not Formated data table")

    txt = fp.read().strip()
    txt = txt.strip('\n')
    txt = re.sub("#.*", "", txt)
    tables = re.findall("TABLE(.*?)ENDTABLE", txt, re.M+re.DOTALL)
    tables = [x.strip().splitlines() for x in tables]
        
    tables = dict([process_table(x, separator) for x in tables])
    fp.close()
    return tables
    


    
