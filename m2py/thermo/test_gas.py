
from .marktable import read_data_tables
from . import gas as g
from pprint import pprint

tables = read_data_tables("gas_test_data.txt")

gases = list(tables.keys())

def test_fuction(function, gas, _input, _output):
    

    
    _function = lambda t:  function(t, gas)
    _error =    lambda x:  100*abs(x[1]-x[0])/x[0]
    
    output = list(map(_function, _input))
    error  = list(map(_error, list(zip(output, _output))))
    
    print("GAS : ", gas) 
    print("Testing : ", function.__name__)    
    print("\nMax error %", max(error))
    
    print("x f(x) f'(x) %%error)")
    pprint (list(zip( _input, output, _output, error)))

    
    print("\n\n")
    
test_gas = lambda gas, func, output : test_fuction(func, gas, tables[gas].T,tables[gas][output])

for gas in gases:
    test_gas(gas, g.__cp_nasap_p7__, "cp")
    test_gas(gas, g.s_nasa_p7, "s")
    print(60*"-")
#test_gas("O2", g.__cp_nasap_p7__, "cp")

#CO2 = tables["CO2"]

