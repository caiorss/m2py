#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys

__all__ = ["__stable__", "mixture_volume", "vapor_quality",
           "phase", "p_satT", "vf_satT", "Vg_sat", "T_sat"]

this = os.path.dirname(os.path.abspath(__file__))
path_dir = os.path.join(this, "../..")
sys.path.append(path_dir)

from m2py.numerical.numerical import interpol, read_table
from m2py.utils import resource_path


__saturation_table__ = resource_path("saturated_steam.txt")
__saturation__ = read_table(__saturation_table__)

tol = 1e-1


def __stable__(value, _input, params):
    """
    Calculate the Saturated water thermodynamic properties 
    table from Steam table properties, given the temperature T.
    
    Source:          
        Apendix B, Page 775 - Table B1.1
        Fundamentals of Thermodynamics, 
        SI Units Thermodynamic Tables. 8th edition
        BORGNAKKE and SONNTAG

    :param T:       Temperature at ºC
    :param params:  List of properties to be calculated
    :param _input:   Type of input parameter. Possible values
    :return:        List of calculated properties
    
    Possible Values of input: ['T', 'P']
    
    Possible values of param:
    
    T, P, Vf, Vfg, Vg, Uf, Ufg, Ug, Hf, Hfg, Hg, Sf, Sfg, Sg
    
    T       Temperature                 ºC
    P       Pressure                    kPa
    Vf      Sat Liquid Specific Volume  m3/kg
    Vfg     Vg-Vf                       m3/kg
    Vg      Sat Vapor                   m3/kg
    Uf      Sat Liquid Internal Energy  kJ/kg
    Ufg     Ug-Uf                       kJ/kg
    Ug      Sat Vapor Internal Energy   kJ/kg
    Hg      Sat Liquid Entalphy         kJ/kg
    Hfg     Vf-Vg Entalphy              kJ/kg
    Hg      Sat Vapor Entalphy          kJ/kg
    Sf      Sat Liquid Entropy          kj/Kg-K
    Sfg     Vf-Vg Entropy               kj/Kg-K
    Sg      Sat Vapor Entropy           kj/Kg-K
        
    Example:
        >>> import m2py.thermo.steam
        >>> m2py.thermo.steam.sattable(232, 'T', ['P', 'Vf', 'Vg', 'Uf' ])
        [2900.98, 0.001213, 0.069092, 995.984]


        >>> s.__stable__(500, 'P', ['T', 'Vf', 'Vg', 'Uf' ])
        [151.79315476190476,
         0.0010921517857142857,
         0.3762758035714286,
         639.3956696428571]  
    """
    s = __saturation__
    result = []

    input_column = s[_input]

    for p in params:
        y = interpol(value, input_column, s[p])
        result.append(y)

    return result


def psat_t(T):
    """
    :param T: Saturation temperature in °C
    :return:  Water steam saturation pressure in kPa
    """
    return __stable__(T, 'T', ['P'])[0]


def tsat_p(P):
    """
    Saturation Temperature

    :param P: Saturation Pressure in kPa
    :return:  Saturation temperature in °C
    """
    return __stable__(P, 'P', ['T'])[0]


def vsat_xt(x, T):
    """
    Saturation Volume as function of Steam Quality and Temperature
    :param T:
    :param x:
    :return:
    """
    if x < 0 or x > 1:
        raise ValueError("Steam quality must be in 0 < x < 1")

    vf, vg = __stable__(T, 'T', ['vf', 'vg'])
    v = (1 - x) * vf + x * vg
    return v

def hsat_xt(x, T):
    """
    :param x:
    :param T:
    :return:
    """
    if x < 0 or x > 1:
        raise ValueError("Steam quality must be in 0 < x < 1")

    hf, hg = __stable__(T, 'T', ['hf', 'hg'])
    h = (1 - x) * hf + x * hg
    return h
    
def usat_xt(x, T):
    """
    Saturation Volume as function of Steam Quality and Temperature
    :param T:
    :param x:
    :return:
    """
    if x < 0 or x > 1:
        raise ValueError("Steam quality must be in 0 < x < 1")

    uf, ug = __stable__(T, 'T', ['uf', 'ug'])
    u = (1 - x) * uf + x * ug
    return u
    
def ssat_xt(x, T):
    """
    Saturation Volume as function of Steam Quality and Temperature
    :param T:
    :param x:
    :return:
    """
    if x < 0 or x > 1:
        raise ValueError("Steam quality must be in 0 < x < 1")

    sf, sg = __stable__(T, 'T', ['sf', 'sg'])
    s = (1 - x) * sf + x * sg
    return s
    





def mixture_volume(x, value, _input='T'):
    """
    Calculates the average specific volume 
    given the the vapor quality x (Mvap/M)
    and parameters value, _input:
    
    :param x: Vapor quality 0 < x < 1
    :param value: Value of Temperature or pressure
    :pram _input: Input type "P" for pressure, "T" for temperatur
    :return: Average Specific volume
    
    v = (1-x)*vf + x*vg 
    
    Example: 
    
    Calculate the specific volume m3/kg for 4 Mpa
    and quality x = 90% 
    
    >>> mixture_volume( 0.9, 4000, 'P')
    0.04495115454545455
           
    """

    vfsat, vgsat = __stable__(value, _input, ['vf', 'vg'])
    v = (1 - x) * vfsat + x * vgsat
    return v


def vapor_quality(v, value, _input='T'):
    """
    Calculates the vapor quality given
    v, vf and vg
    
    :return: (v-vf)/(vg-vf)
    """
    vfsat, vgsat = __stable__(value, _input, ['vf', 'vg'])
    return (v - vfsat) / (vgsat - vfsat)


def phase(T, P=None, v=None, debug=False):
    """
    Determine the phase of saturated steam. 
    Given its temperature or Specific Volume
    """

    # Only T and P is known
    if P is not None:

        Tsat, vfsat, vgsat = __stable__(P, 'P', ['T', 'vf', 'vg'])

        if debug:
            print dict(Tsat=Tsat, vfsat=vfsat, vgsat=vgsat)

        if T < Tsat:
            return "Supercooled liquid"
        elif abs(T - Tsat) < tol:
            return "Two mixed phase mixture liquid and vapor"
        else:
            return "Vapor"

    if v is not None:

        Psat, vfsat, vgsat = __stable__(T, 'T', ['P', 'vf', 'vg'])

        if debug:
            print dict(Psat=Psat, vfsat=vfsat, vgsat=vgsat)

        if v < vfsat:
            return "Liquid"
        elif vfsat < v < vgsat:
            return "Two mixed phase mixture liquid and vapor"
        elif v > vgsat:
            return "Super Heated Vapor"


