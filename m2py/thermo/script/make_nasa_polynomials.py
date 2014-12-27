
import sys
import os
import re
import json

from m2py.utils import resource_path
from m2py.thermo.scrap_mollar_mass import get_molar_mass

dat = open(resource_path("data/nasa_poly7gas.txt")).read()
data = "\n".join(dat.splitlines()[4:-2])
data = re.findall("(\S+).*1\n(.*)2\n(.*)3\n(.*)4", data, re.M)

print(data)

README = """
NASA POLYNOMIALS COEFFICIENTS


Temperatures   300.000  1000.000  5000.000
! GRI-Mech Version 3.0 Thermodynamics released 7/30/99
! NASA Polynomial format for CHEMKIN-II
! see README file for disclaimer

http://combustion.berkeley.edu/gri-mech/data/nasa_plnm.html

NASA polynomials you can consult the report by Alex Burcat 
'Thermochemical Data for Combustion Calculations'

The NASA polynomials have the form:

Cp/R = a1 + a2 T + a3 T^2 + a4 T^3 + a5 T^4

H/RT = a1 + a2 T /2 + a3 T^2 /3 + a4 T^3 /4 + a5 T^4 /5 + a6/T

S/R  = a1 lnT + a2 T + a3 T^2 /2 + a4 T^3 /3 + a5 T^4 /4 + a7


"""


thermodata = {}

for cell in data:
    
    substance = cell[0]
    values = " ".join(cell[1:])
    values = values.split()
    values = list(map(float, values))    
    thermodata[substance] = values
    
    print(values)
    
import shelve

substances = list(thermodata.keys())
molar_mass_list = list(map(get_molar_mass, substances))

molar_mass_data = dict(list(zip(substances, molar_mass_list)))

#f = shelve.open(resource_path('data/gas_nasa_poly7'), 'w')

f = {}
f['coefficients'] = thermodata
f['molarmass'] = molar_mass_data
f['substances'] = list(thermodata.keys())
f['README'] = README

fp = open(resource_path('data/gas_nasa_poly7.json'), 'w')
fp.write(json.dumps(f))
fp.close()

#f.close()
