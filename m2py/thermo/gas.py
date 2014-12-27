#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http://www.myengineeringworld.net/2013/10/Excel-thermochemical-NASA-polynomials-Burcat.html

"""

#
# http://www.wsp.ru/en/..%5Cdownload%5Cdocs%5Carticles%5Cen%5CTENG221.pdf
# http://www.wsp.ru/en/test/wspgGCGS.asp?gas_specification=air
#import sys
#sys.path.append("/home/tux/PycharmProjects/m2py")

from math import (log, exp)
from m2py import units
from m2py.utils import resource_path
from m2py import utils

#import shelve
import json

#data = shelve.open(resource_path("thermo_nasa_poly7.dat"))
data =  utils.load_json_file((resource_path("data/gas_nasa_poly7.json")))


nasapoly7coefs = data['coefficients']
molarmass      = data['molarmass']
substances     = data['substances']

# Unity conversion factors
cal2J = units.factor("cal/J")
J2cal = units.factor("J/cal")

R_ = 1.987204118 # cal/(mol.K)

p0 = 0.1  # MPa
R = 8.31451*1e-3  # KJ/(mol.K)
Tr = 1000  # K


air_table = [-3.62171168554944, 13.1878685737717, -11.61002657829, 6.1800155085671, -1.97996023924462,
             0.352570060264284, -0.026853107411115, 1.26880226994069, 4.69260613574416e-1,
             -3.09569582156729e-1, 7.2153490824886e-2, -8.07371553566351e-3, 3.61550066177588e-4]



def Rgas(gas):
    """
    Return the specific gas constant
    """
    return R/molarmass[gas]

def cp_t(T, a):
    tau = T / Tr  # Reduced temperature

    C = 0
    for i in range(6):
        C += a[i] * tau ** i

    _tau = 1 / tau
    for i in range(7, 12):
        C += a[i] * _tau ** (i - 6)

    cp = C * R
    return cp


def h_t(T, hint, a):
    tau = T / Tr

    C = 0
    for i in range(6):
        C += a[i] / (i + 1) * tau ** i

    C = a[7] * log(tau)

    _tau = 1 / tau
    for i in range(8, 12):
        C = a[i] / (7 - i) * _tau ** (i - 7)

    h = Tr*R*C #+ hint

    return h

def get_substances():
    return list(nasapoly7coefs.keys())

def get_molarmass(substance):
    """Return molar mass in kg/mol"""
    return molarmass[substance]

def __cp_nasap_p7__(T, substance):
    """
    Calculates Heat Capacity cp - [cal/(mol.K)] 
    from Nasa 7-coefficient Polynomials. 
    
    Cp/R = a1 + a2 T + a3 T^2 + a4 T^3 + a5 T^4
    
    :param T: Temperature in K
    :return: cp Heat Capacity/ Cp heat in [cal/(mol.K)]
    """
    a = nasapoly7coefs[substance]
    
    C = 0
    for i in range(5):
        C = C + a[i]*T**i
    
    return round(C*R_, 2)

def cp_nasa_p7_mol(T, substance):
    """
    Calculates Heat Capacity cp - [J/(mol.K)] 
    from Nasa 7-coefficient Polynomials. 
    
    Cp/R = a1 + a2 T + a3 T^2 + a4 T^3 + a5 T^4
    
    :param T: Temperature in C
    :return: cp Heat Capacity/ Cp heat in [ J/(mol.K)]
    """  
    T = units.c2k(T)
    cp = __cp_nasap_p7__(T, substance)
    cp = cal2J*cp
    return cp

def cp_nasa_p7(T, substance):
    """
    Calculates Heat Capacity cp - [J/(kg.K)] 
    from Nasa 7-coefficient Polynomials. 
    
    Cp/R = a1 + a2 T + a3 T^2 + a4 T^3 + a5 T^4
    
    :param T: Temperature in C
    :return: cp Heat Capacity/ Cp heat in [ J/(kg.K)]
    """  
    m = molarmass[substance]
    T = units.c2k(T)
    cp = __cp_nasap_p7__(T, substance)
    cp = cal2J*cp/m
    return cp

def s_nasa_p7(T, substance):
    """
    S/R  = a1 lnT + a2 T + a3 T^2 /2 + a4 T^3 /3 + a5 T^4 /4 + a7
    """
    a = nasapoly7coefs[substance]
    C = a[0]*log(T) + a[1]*T + a[2]*T**2 /2 + a[3]*T**3 /3 + a[4]*T**4 /4 + a[6]
    C = C*R_
    return round(C, 2)

def h_nasa_p7(T, substance ):
    """
    :param T: Temperature in K
    :param substance: Substance Name
    """
    a = nasapoly7coefs[substance]
    
    C =  a[0] + a[1]*T/2 + a[2]*T**2 /3 + a[3]*T**3 /4 + a[4]*T**4 /5 + a[5]/T
    H = R_*T*C
    return H
    
 


"""
3.03399249E+00 2.17691804E-03-1.64072518E-07-9.70419870E-11 1.68200992E-14    2
-3.00042971E+04 4.96677010E+00 4.19864056E+00-2.03643410E-03 6.52040211E-06    3
-5.48797062E-09 1.77197817E-12-3.02937267E+04-8.49032208E-01    

"""   
