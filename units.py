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


"""
pi = 3.141592653589793

# SI prefix
pico  = 1e-12
nano  = 1e-9
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
angstrom = 10e-8*cm

# Mass
mg    = 1e-6
g     = 1e-3
kg    = 1
slug  = 14.594          # kg - 32.174 lbm
lbm   = 1.0/2.2046      # kg
pound = 0.45359237
oz    = 1.0/16*lbm      # Ounce
tonne = 1000            # Metric tonne


# Area
acre = 4046.9   # m2
hectare = 10000 # m2
galon = 0.0037854 #m3 US Gallon

# Pressure
Pa = 1.0
KPa = 1.0e3
MPa = 1.0e6
GPa = 1.0e9
psi = 6.895 * 1e3
kpsi = 6.895 * 1e6
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
joule =1
J = 1
kJ = 1e3
MJ = 1e6
cal = 4.184             # J Calories
kcal = 1e3*cal          # Kilocal
Wh  = 3600
kWh = 3.6*mega  
eV = 1.602*1e-19 
Btu =  3412.14          # International Table

# Power 
w =1
watt = 1
kw = 1e3
Mw = 1e6
Gw = 1e9
HP = 746                # Horsepower
CV = 735.5              # Cavalo Vapor

# Angular Speed and frequency
Hz  = 1.0       # Hertz
kHz = 1.0e3     # Kilo Hertz
MHz = 1.0e6
rads = 1/(2*pi) # [Hertz] - Radians per second
rpm  = 1.0/60   # [Hertz]
rpm2rads = lambda x: x*rpm/rads
rads2rpm = lambda x: x*rads/rpm
hz2rads  = lambda x: x*Hz/rads
rads2hz  = lambda x: x*rads/Hz

# Units dictionary
units = dict(

    # Length
    m = m, 
    um = um, 
    mm = mm, 
    cm = cm, 
    km = km, 
    IN = IN, 
    inch = inch, 
    ft = ft, 
    
    # Mass
    mg    = mg,
    g     =  g,
    kg    = kg,
    slug  = slug,
    lbm   = lbm,
    pound = pound,
    oz    = oz,
    tonne = tonne,
    
    # Pressure
    Pa = Pa,  
    KPa = KPa,  
    MPa = MPa,  
    GPa = GPa,  
    psi = psi,  
    kpsi = kpsi,  
    bar = bar,  
    torr = torr,  
    atm = atm,  
    
    # Force
    N = N,  
    kN = kN,  
    MN = MN,  
    GN = GN,   
    kgf = kgf,  
    lbf = lbf,
    
    # Time
    s = s,  
    ms = ms,  
    us = us,  
    min = min,  
    h = h,  
    
    # Energy
    joule = joule, 
    J = J, 
    kJ = kJ, 
    MJ = MJ, 
    cal = cal, 
    kcal = kcal, 
    Wh = Wh,  
    kWh = kWh, 
    eV = eV, 
    Btu = Btu, 
    
    # Power
    watt = watt,
    w = w,
    kw = kw,
    Mw = Mw,
    Gw = Gw,
    HP = HP,
    CV = CV,
    
    # Angular Speed
    Hz = Hz,  
    kHz = kHz, 
    MHz = MHz, 
    rads = rads, 
    rpm = rpm,  
)
    

def convert(value, fromunit, tounit):
    """
    Convert unit from_unit to to_unit
    
    Example:
        10 atm in PSI
            In [24]: u.convert(1, "atm", "psi")
            Out[24]: 14.695431472081218
    """
    fromunit = units[fromunit]
    tounit   = units[tounit]
    return value*fromunit/tounit
    

# Temperature conversion functions
#
def kelvin2celcius(K):
    """
    Convert temperature from Kelvin Scale 
    to Celcius scale
    :return: K - 273.15
    """
    return K - 273.15
    
    
def celcius2kelvin(C):
    """  
    Convert from Celcius to Kelvin Scale. 
    
    :return: K = C + 273.5
    """
    return C + 273.5
    
def fahrenheit2celcius(F):
    """ 
    It converts from Farenheit to Celcius
    
    :return: 5.0/9.0*(F-32)
    """
    return 5.0/9.0*(F-32)

def celcius2farenheit(C):
    """
    It converts from Celcius to Farenheit
    
    :return: 9.0/5.0*C + 32
    """
    return 9.0/5.0*C + 32

def fahrenheit2kelvin(F):
    return 5.0/9.0*(F+459.67)
    
def kelvin2farenheit(K):
    """
    It converts from Kelvin Scale to Farenheit scale.
    
    :return: 9.0/5.0*K - 459.67
    """
    return 9.0/5.0*K - 459.67

    
