#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: unit.py 

This module implements factos of SI units and physical constants
that are usefult to physics and engineering calculations. 
All units defined in this module are defined at SI basic units.


Available Units and Convertion Functions:
------------------------------------------

# SI prefix
pico   nano   micro  mili  kilo  mega  giga 

# Angles
************************************************
rad ,deg ,radian ,degree ,minute ,second ,turn ,mil 
    
    *mil - A unit of angle measure, used in the military 
    for artillery settings. The mil is equal to 1/1600 right angle. 
    
    *turn   - Full circle
    *minute - 1/60 degrees
    *second - 1/60 minutes

# Lenght Unit
************************************************
m um mm cm km IN inch ft feet angstrom mile nmile
 * nmile : Nautical Mile

# Mass
************************************************
mg    g     kg    slug  lbm   pound oz    tonne

# Area
************************************************
acre hectare galon 

# Volume
************************************************
m3  mm3  cm3  in3  inch3  ft3  L  mL kL liter oil_barrel

# Pressure
************************************************
Pa kPa MPa GPa psi kpsi bar torr mtorr atm mmHg inHg 

# Force
************************************************
N kN MN GN lbf kgf dyne 

# Time
************************************************
s ms us min h

# Energy units
************************************************
joule J kJ MJ cal kcal Wh  kWh eV Btu erg

# Power
************************************************
w watt kW MW GW HP CV 

# Angular Speed and frequency
************************************************
Hz  kHz MHz rads rpm  rpm2rads rads2rpm hz2rads  rads2hz  

# Speed
#***********************************************
kmph -  Kilometers per hour         km/h
mph  -  miles/h   Miles per hour    miles/h
nmph -  Nautical miles per hour     nmiles/h
inps -  Inches per second           in/s
fps  -  Feet per second             ft/s


# Temperature Conversion Functions
#***********************************************

From Kelvins            
    Function Name       Alias
    -------------------------
    kelvin2celcius      k2c         Convert Kelvin to Celcius
    kelvin2farenheit    k2f         Convert Kelvin to Fahrenheit
    kelvin2rankine      k2r         Convert Kelvin to Rankine

From Celcius            
    Function Name       Alias
    -------------------------
    celcius2farenheit   c2f         Convert Celcius to Fahrenheit
    celcius2kelvin`     c2k         onvert Celcius to Kelvin
    celcius2rankine     c2r         Convert Celcius to Rankine

From Fahrenheit
    fahrenheit2celcius  f2c         Convert Fahrenheit to Celcius
    fahrenheit2kelvin   f2k         Convert Fahrenheit to Kelvin
    farenheit2rankine   f2r         Convert Farenheit to Rankine

From Rankine
    rankine2celcius     r2c         Convert Rankine to Celcius
    rankine2kelvin      r2k         Convert Rankine to Kelvin
    rankine2fahrenheit  r2f         Convert Rankine to Fahrenheit
 

# General Unit Conversion Functions
#**************************************************

Function                                Alias
    factor(conversio_string)            f
    convert(value, fromunit, tounit)    c
    

EXAMPLES
----------------------------------------------------

    >>> from m2py import units as u
    >>> 
    >>> # Convert 160 mmHg to inHg
    ... 
    >>> 160*u.factor("mmHg/inHg")
    6.216837929413121
    >>> 
    >>> # Convert 100 atms to psi
    ... 
    >>> 100*u.factor("atm/psi")
    1469.5431472081218
    >>> 
    >>> # Temperature convertion 100 Fahrenheit to Kelvins, Celcius, Rankine
    ... 
    >>> u.f2k(100)
    310.9277777777778
    >>> u.f2c(100)
    37.77777777777778
    >>> u.f2r(100)
    559.6700000000001
    >>>
    >>>
    >>> # Convert 100 km/h to miles per hour or mph
    >>> u.convert(100, "kmph", "mph")
    62.1371192237334
    >>>
    >>> # Compound Units conversion km/h to m/s
    >>> 100*u.factor("km/h")
    27.77777777777778
    >>> u.factor("100*km/h")
    27.77777777777778
    >>>
    >>>
    # Reverse convertsion 27.77  m/s to km/h
    >>> 27.778*u.factor("(m/s)/(km/h)")
    100.00079999999998
    >>>
    >>> 
    # Convert 300 HP to kW using `factor` alias
    >>> 300*u.f("HP/kW")
    223.8
    >>> 
    >>> # Convert 200 knot to km/h
    >>> 200*u.f("knot/kmph")
    370.39968
    >>>
    >>> # Reverse Conversion
    >>> 370.399*u.f("kmph/knot")
    199.99963282905645
    >>> 
    >>> # Conversion using alias
    >>> u.c(200, "knot", "kmph")
    370.39968
    >>> 
    >>> u.c(300, "MPa", "psi")
    43509.789702683105
    >>> 
    >>> u.c(300, "mmHg", "psi")
    5.724972329300408
    >>> 
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
 
# Angle - Basic Unit - Degree
radian = 1/0.01745329
degree = 1
rad = radian
deg = degree
minute = 60*degree
seconds = 60*minute
turn    = 360*degree            # Full Circle
mil     =  90*degree/1600       # 

# Lenght Unit
m = 1.0
um = 1.0e-6
mm = 1.0e-3
cm = 1.0e-2
km = 1.0e3

IN = 0.0254
inch = 0.0254
feet = 0.3048
ft = 0.3048
yard = 3 * ft
yd = yard
mile = 1609.344
nautical_mile = 1852
nmile = nautical_mile
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

#Volume
m3 = 1
mm3 = mm**3
cm3 = cm**3
in3 = inch**3
inch3 = inch**3
ft3 = ft**3
L   = 0.001     # liter
mL  = 0.000001
kL  = 1
liter = 0.001
oil_barrel = 160*liter

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
mtorr = torr*1e-3
atm = 1.01325 * 1e5  # Force
mmHg = 131.57894736842104
inHg =  3386.3889999999997

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
erg = 1e-7

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


# Speed 
kmph = km/h      # Kilometers per hour
mph = mile/h     # Miles per hour
nmph = nautical_mile/h  # Nautlical miles per hour
inps = inch/s    # Inches per second
fps  = feet/s    # feets per second
knot = 0.514444  # Nautical miles/h

# Units dictionary
units = dict(
    __builtins__ = None,
    
    # Angles
    rad=radian,
    deg=deg,
    radian=radian,
    degree=degree,
    minute=minute,
    second=seconds,
    turn=turn,  # Full Circle
    mil=mil,  #
        
    # Length
    m=m,
    um=um,
    mm=mm,
    cm=cm,
    km=km,
    IN=IN,
    inch=inch,
    feet=feet,
    ft=ft,
    yard=yard,
    mile=mile,
    nmile=nmile,
    nautical_mile=nautical_mile,

    # Area
    m2=m2,
    cm2=cm2,
    mm2=mm2,
    km2=km2,
    in2=in2,
    yd2=yd2,
        
    #Volume
    m3=m3,  
    mm3=mm3,  
    cm3=cm3,  
    in3=in3,  
    inch3=inch3,  
    ft3=ft3,  
    L=L,    
    mL=mL,   
    kL=kL,   
    liter=liter,  
    oil_barrel=oil_barrel,  

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
    mtorr = mtorr,
    atm=atm,
    mmHg = mmHg,
    inHg = inHg,

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
    erg=erg,

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
    
    # Speed
    mph = mph,
    nmph = nmph,
    kmph = kmph,
    inps = inps,
    fps  = fps,
    knot = knot,
    
)

units['in'] = IN


def dms_deg(degree_tuple):
    """
    Convert degree minute'  second'' to decimal angle
    
    :param degree_tuple: (degree, minute, second) tuple
    :return: Decimal angle in degrees
    
    Example:   
        >>> import units as u
        >>> 
        >>> u.dms_deg((45, 23, 34))
        45.39277777777778
    
    """
    degree, minute, second = degree_tuple
    decimal_degree = degree + minute/60.0 + second/3600.0
    return decimal_degree
    
def deg_dms(decimal_degree):
    """
    Convert angle in degrees to degree, minute, second tuple

    :param degree: Angle in degrees
    :return:   (degree, minutes, second) 
    
    Example:
        >>> import units as u
        >>> 
        >>> u.dms_deg((45, 23, 34))
        45.39277777777778
        >>> 
        >>> u.deg_dms(45.392778)
        (45, 23, 34)    
    """
    degree = int(decimal_degree) # Extract integer part
    rm = 60*(decimal_degree - degree)
    minutes = int(rm)
    seconds = int(60*(rm-minutes))
    return (degree, minutes, seconds) 

def rad_dms(radian_angle):
    """
    Convert angle in radians to (degree, minute, second) tuple

    :param degree: Angle in radians
    :return:   (degree, minutes, second) 
    """
    degrees = radian_angle*randian
    return deg_dms(degrees)

def dms_rad(degree_tuple):
    """
    Convert degree minute'  second'' to randian angle
    
    :param degree_tuple: (degree, minute, second) tuple
    :return: Angle in radians
    
    Example:   
    
    """
    degrees = dms_deg(degree_tuple)
    return degrees/radians

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
    
    if fromunit == "in":
        fromunit = inch
    if tounit == "in":
        tounit == inch
        
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
    
def celcius2rankine(C):
    """
    Convert Celcius to Fahrenheit

    :param C: Temperature in Celcius
    :return:  Temperature in Fahrenheit
    """
    return 9.0/5.0*C + 491.67


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


f = factor
c = convert

c2k = celcius2kelvin
c2f = celcius2farenheit
c2r = celcius2rankine

k2c = kelvin2celcius
k2f = kelvin2farenheit
k2r = kelvin2rankine

f2c = fahrenheit2celcius
f2r = farenheit2rankine
f2k = fahrenheit2kelvin

r2c = rankine2celcius
r2f = rankine2fahrenheit
r2k = rankine2kelvin


class Temperature(object):
    """
    Class to Convert temperature units

    .c - Temperature in  Celcius
    .f - Temperature in  Fahreheint
    .k - Temperature in  Kelvins

    Example:
    >>> from m2py.units import Temperature as Temp
    >>> t = Temp(c=100)
    >>> t.c
    100
    >>> t.f # Temperature in Fahrenheit
    212.0
    >>> t.k # Temperature in Kelvins
    373.5
    >>> t.f = 300
    >>> t.c # Temperature in Celcius
    148.88888888888889
    >>> t.k
    422.03888888888895
    >>>
    >>> t.k = 400
    >>> t.f
    260.33
    >>> t.c
    126.5
    >>>
    """

    def __init__(self, c=0, k=0, f=0):
        self._c = 0
        self._k = 0
        self._f = 0

        if c:
            self.c = c
        if k:
            self.k = k
        if f:
            self.f = f

    @property
    def c(self):
        return self._c

    @property
    def k(self):
        return self._k

    @property
    def f(self):
        return self._f

    @c.setter
    def c(self, c):
        self._c = c
        self._k = c + 273.5
        self._f  = 9.0 / 5.0 * c + 32

    @f.setter
    def f(self, f):
        self._f = f
        self._k = 5.0 / 9.0 * (f + 459.67)
        self._c = 5.0 / 9.0 * (f - 32)

    @k.setter
    def k(self, k):
        self._k = k
        self._f = 9.0 / 5.0 * k - 459.67
        self._c = k - 273.5

