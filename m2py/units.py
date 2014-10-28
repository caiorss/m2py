#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: unit.py 

This module implements factos of SI units and physical constants
that are usefult to physics and engineering calculations. 
All units defined in this module are defined at SI basic units.

The system works with standard units, example:

    when we are going to make the calculations using a pressure quantity
    we write  x= 3 # Mpa , in this module we can do   x=3*Mpa and then
    we get x= 3*1e6.

Basic Units:  m - s - kg - K
Usage:


>> 23*ft        #
7.0104                  # 23 feets= 7.0104 meters

>> 450*psi
3102750.0       # Pa

>> 450*KPa/psi      # 450 KPa into psi
65.264          # psi

>> a=20.0       # km/h
>> a*(km/m)/(h/s)   #
5.5555          # m/s


Available Units and Convertion Functions:
------------------------------------------

# SI prefix
pico  
nano  
micro 
mili 
kilo 
mega 
giga 

# Lenght Unit
************************************************
m um mm cm km IN inch ft angstrom 

# Mass
************************************************
mg    g     kg    slug  lbm   pound oz    tonne

# Area
************************************************
acre hectare galon 

# Pressure
************************************************
Pa kPa MPa GPa psi kpsi bar torr atm

# Force
************************************************
N kN MN GN lbf kgf dyne 

# Time
************************************************
s ms us min h

# Energy units
************************************************
joule J kJ MJ cal kcal Wh  kWh eV Btu 

# Power
************************************************
w watt kW MW GW HP CV 

# Angular Speed and frequency
************************************************
Hz  kHz MHz rads rpm  rpm2rads rads2rpm hz2rads  rads2hz  


"""
from __future__ import division

pi = 3.141592653589793

# SI prefix
pico = 1e-12
nano = 1e-9
micro = 1e-6
mili = 1e-3
kilo = 1e3
mega = 1e6
giga = 1e9

# Lenght Unit
m = 1.0
um = 1.0e-6
mm = 1.0e-3
cm = 1.0e-2
km = 1.0e3

IN = 0.0254
inch = 0.0254
ft = 0.3048
yard = 3 * ft
yd = yard
mile = 1609.344
nautical_mile = 1852
angstrom = 10e-8 * cm


# Mass
mg = 1e-6
g = 1e-3
kg = 1
slug = 14.594  # kg - 32.174 lbm
lbm = 1.0 / 2.2046  # kg
pound = 0.45359237
oz = 1.0 / 16 * lbm  # Ounce
tonne = 1000  # Metric tonne


# Area
acre = 4046.9  # m2
hectare = 10000  # m2
galon = 0.0037854  # m3 US Gallon
cm2 = 1e-4
mm2 = 1e-6
m2 = 1
km2 = 1e6
in2 = inch ** 2  # Squared inches
inch2 = in2
ft2 = ft ** 2
yd2 = yd ** 2
mile2 = mile ** 2


# Pressure
Pa = 1.0
kPa = 1.0e3
MPa = 1.0e6
GPa = 1.0e9
psi = 6.895 * 1e3
kpsi = 1e3 * psi
Mpsi = 1e3 * kpsi
bar = 1e5
torr = 133.322
atm = 1.01325 * 1e5  # Force

# Force
N = 1.0
kN = 1e3
MN = 1e6
GN = 1e9
lbf = 4.448222
kgf = 9.80665
dyne = 1e-5


# Time
s = 1.0
ms = 1e-3
us = 1e-6
min = 60.0
h = 3600

# Energy units
joule = 1
J = 1
kJ = 1e3
MJ = 1e6
cal = 4.184  # J Calories
kcal = 1e3 * cal  # Kilocal
Wh = 3600
kWh = 3.6 * mega
eV = 1.602 * 1e-19
Btu = 3412.14  # International Table

# Power 
W = 1
watt = 1
kW = 1e3
MW = 1e6
GW = 1e9
HP = 746  # Horsepower
CV = 735.5  # Cavalo Vapor

# Angular Speed and frequency
Hz = 1.0  # Hertz
kHz = 1.0e3  # Kilo Hertz
MHz = 1.0e6
rads = 1 / (2 * pi)  # [Hertz] - Radians per second
rpm = 1.0 / 60  # [Hertz]
rpm2rads = lambda x: x * rpm / rads
rads2rpm = lambda x: x * rads / rpm
hz2rads = lambda x: x * Hz / rads
rads2hz = lambda x: x * rads / Hz

# Units dictionary
units = dict(

    # Length
    m=m,
    um=um,
    mm=mm,
    cm=cm,
    km=km,
    IN=IN,
    inch=inch,
    ft=ft,
    yard=yard,
    mile=mile,
    nautical_mile=nautical_mile,

    # Area
    m2=m2,
    cm2=cm2,
    mm2=mm2,
    km2=km2,
    in2=in2,
    yd2=yd2,

    # Mass
    mg=mg,
    g=g,
    kg=kg,
    slug=slug,
    lbm=lbm,
    pound=pound,
    oz=oz,
    tonne=tonne,

    # Pressure
    Pa=Pa,
    kPa=kPa,
    MPa=MPa,
    GPa=GPa,
    psi=psi,
    kpsi=kpsi,
    Mpsi=Mpsi,
    bar=bar,
    torr=torr,
    atm=atm,

    # Force
    N=N,
    kN=kN,
    MN=MN,
    GN=GN,
    kgf=kgf,
    lbf=lbf,

    # Time
    s=s,
    ms=ms,
    us=us,
    min=min,
    h=h,

    # Energy
    joule=joule,
    J=J,
    kJ=kJ,
    MJ=MJ,
    cal=cal,
    kcal=kcal,
    Wh=Wh,
    kWh=kWh,
    eV=eV,
    Btu=Btu,

    # Power
    watt=watt,
    W=W,
    kW=kW,
    MW=MW,
    GW=GW,
    HP=HP,
    CV=CV,

    # Angular Speed
    Hz=Hz,
    kHz=kHz,
    MHz=MHz,
    rads=rads,
    rpm=rpm,
)

units['in'] = IN


def convert(value, fromunit, tounit):
    """
    Convert unit from_unit to to_unit
    
    Example:
        10 atm in PSI
            In [24]: u.convert(1, "atm", "psi")
            Out[24]: 14.695431472081218
    """
    fromunit = units[fromunit]
    tounit = units[tounit]
    return value * fromunit / tounit


def factor(conversio_string):
    """
    Coversion factor to unit conversion.

    :param   conversio_string:  Unit to convert from
    :type    conversio_string:  str
    :return:                    Converstion Factor
    :rtype:  float

    Uasage:

    factor("<unit-to-convert>/<current-unit>")

    Example:

    Convert 300 HP into kW

    >>> import m2py.units as u
    >>> 300*u.factor("HP/kW")
    223.8


    """

    # tounit, fromunit = conversio_string.split("/")
    # fromunit = units[fromunit]
    # tounit = units[tounit]
    #eturn tounit/fromunit
    f = eval(conversio_string, units)
    return f


# Temperature conversion functions
#
def kelvin2celcius(K):
    """
    Convert Kelvin to Celcius

    :param K: Temperature in Kelvin
    :return:  Temperature in Celcius
    """
    return K - 273.15


def celcius2kelvin(C):
    """
    Convert Celcius to Kelvin

    :param C: Temperature in Celcius
    :return:  Temperature in Kelvin
    """
    return C + 273.5


def fahrenheit2celcius(F):
    """
    Convert Fahrenheit to Celcius

    :param F: Temperature in Fahrenheit
    :return:  Temperature in Celcius
    """
    return 5.0 / 9.0 * (F - 32)


def celcius2farenheit(C):
    """
    Convert Celcius to Fahrenheit

    :param C: Temperature in Celcius
    :return:  Temperature in Fahrenheit
    """
    return 9.0 / 5.0 * C + 32


def fahrenheit2kelvin(F):
    """
    Convert Fahrenheit to Kelvin

    :param F: Temperature in Fahrenheit
    :return:  Temperature in Kelvin
    """
    return 5.0 / 9.0 * (F + 459.67)


def kelvin2farenheit(K):
    """
    Convert Kelvin to Fahrenheit

    :param K: Temperature in Kelvin
    :return:  Temperature in Fahrenheit
    """
    return 9.0 / 5.0 * K - 459.67


def kelvin2rankine(K):
    """
    Convert Kelvin Temperature to Rankine

    :param K: Temperature in Kelvin
    :return:  Temperature in R Rankine
    """
    return 9.0 / 5.0 * K


def rankine2celcius(R):
    """
    Convert Rankine Temperature to Celcius

    :param R: Temperature in Rankine
    :return:  Temperature in Celcius
    """
    return (R - 491.67) * 5.0 / 9


def rankine2kelvin(K):
    """
    Convert Rankine Temperature to Kelvin

    :param K: Temperature in K Kelvin
    :return:  Temperature in R Rankine
    """
    return 5.0 / 9.0 * K

def rankine2fahrenheit(R):
    """
    Convert Rankine Temperature to Kelvin

    :param R: Temperature in Rankine
    :return:  Temperature in Fahrenheit
    """
    return R - 459.67

def farenheit2rankine(F):
    """
    Convert Farenheit to Rankine

    :param F: Temperature in Fahrenheit
    :return:  Temperature in Rankine
    """
    return F + 459.67

k2c = kelvin2celcius
c2k = celcius2kelvin
f2c = fahrenheit2celcius
c2f = celcius2farenheit
f2k = fahrenheit2kelvin
k2f = kelvin2farenheit
r2c = rankine2celcius
r2k = rankine2kelvin
r2f = rankine2fahrenheit
k2r = kelvin2rankine