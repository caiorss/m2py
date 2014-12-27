#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://books.google.co.uk/books?id=91c8AwAAQBAJ&pg=PA95&lpg=PA95&dq=resistance+materials+AWG+temperature+wire+material&source=bl&ots=9F6ND733gJ&sig=OcgqEFvxV0m2s8A1f7Mpfx8peUA&hl=en&sa=X&ei=9yOWVMDCEsiuggSL7IOgBA&ved=0CDsQ6AEwBQ#v=onepage&q=resistance%20materials%20AWG%20temperature%20wire%20material&f=false

"""
from __future__ import division

from math import log


def awg2mm(AWG):
    """
    Convert AWG ( American Wire Gauge to mm diameter)

    :param awg: Wire AWG
    :return:    Wire milimitter diameter


    diameter [mm] = 0.127 * 92 ^ ((36-AWG)/39)

    Reference: http://www.reuk.co.uk/AWG-to-Square-mm-Wire-Size-Converter.htm
    """
    return round(0.127 * 92 ** ((36 - AWG) / 39), 2)


def mm2awg(diameter):
    """
    Convert the diameter to AWG ( American Wire Gauge ) number

    :param diameter: Diameter in mm
    :return:         Wire AWG number

    Reference: http://www.reuk.co.uk/AWG-to-Square-mm-Wire-Size-Converter.htm
    """
    AWG = -(log(diameter / 0.127) / (log(92) * 39) - 36)
    return AWG


# marks standard handbook for electrical engineers Table 15.1.3
#  http://www2.hcmuaf.edu.vn/data/phamducdung/thamkhao/Mark%27s%20Standard-Handbook/Electronics.pdf
#
__materials_coefficients = {
    #  resistance in 1e-8 ohm.m and coefficients in 1/°C at 20°C
    #  material - resistance  - thermal coefficient ohms/ºC
    "Aluminum": (2.828, 0.00403 ),
    "Antimony": (42.1, 0.0036 ),
    "Bismuth": (111.0, 0.004 ),
    "Brass": (6.21, 0.0015 ),
    "Copper": (1.724, 0.00393 ),
    "Gold": (2.44, 0.0034 ),
    "Lead": (22.0, 0.00387 ),
    "Nickel": (8.54, 0.0041 ),
    "Platinum": (10.72, 0.003 ),
    "Silver": (1.628, 0.0038 ),
    "Zinc": (5.97, 0.0037 ),
    "Monel metal": ( 43.5, 0.0019),
}

__awgtable = [
    # http://www.reuk.co.uk/AWG-to-Square-mm-Wire-Size-Converter.htm
    # AWG     inches mmm  mm2
    ("0000", 0.46),
    ("000", 0.40965),
    ("00", 0.3648),
    ("0", 0.32485),
    ("1", 0.2893),
    ("2", 0.25763),
    ("3", 0.22942),
    ("4", 0.20431),
    ("5", 0.18194),
    ("6", 0.16202),
    ("7", 0.14428),
    ("8", 0.12849),
    ("9", 0.11443),
    ("10", 0.10189),
    ("11", 0.09074),
    ("12", 0.0808),
    ("13", 0.07196),
    ("14", 0.06408),
    ("15", 0.05707),
    ("16", 0.05082),
    ("17", 0.04526),
    ("18", 0.0403),
    ("19", 0.03589),
    ("20", 0.03196),
    ("21", 0.02846),
    ("22", 0.02535),
    ("23", 0.02257),
    ("24", 0.0201),
    ("25", 0.0179),
    ("26", 0.01594),
    ("27", 0.0142),
    ("28", 0.01264),
    ("29", 0.01126),
    ("30", 0.01002),
    ("31", 0.00893),
    ("32", 0.00795),
    ("33", 0.00708),
    ("34", 0.0063),
    ("35", 0.00561),
    ("36", 0.005),
    ("37", 0.00445),
    ("38", 0.00396),
    ("39", 0.00353),
    ("40", 0.00314),
]

__awgdatabase = dict(__awgtable)


def awg_serie():
    return map(lambda x: x[0], __awgtable)


def awg_diam_in(awg):
    """
    :return
    :param awg:
    :return:
    """
    return __awgdatabase[str(awg)]


def awg_diam(awg):
    """
    :param awg: AWG number
    :return:    Wire diameter in mm
    """
    return 25.4 * __awgdatabase[str(awg)]


def awg_area_in2(awg):
    """
    :param awg: AWG number
    :return:    Wire cross sectional area in in2
    """
    return 3.1415926536 * awg_diam_in(str(awg)) ** 2 / 4


def awg_area(awg):
    """
    :param awg: AWG number
    :return:    Wire cross sectional area in mm2
    """
    return 3.1415926536 * awg_diam(str(awg)) ** 2 / 4


def awg_resist(awg, T=20, material="Copper"):
    """
    :param awg:       Wire AWG
    :param temp:      Temperature in °C
    :param material:  Wire material
    :return:          Resistivity at 20 C for the selected material in [Ohms/m]

    Materials: Silver Copper Gold Aluminum Iridium Brass Nickel Iron Platinum Steel Lead

    Reference:

    marks standard handbook for electrical engineers Table 15.1.3
    http://www2.hcmuaf.edu.vn/data/phamducdung/thamkhao/Mark%27s%20Standard-Handbook/Electronics.pdf
    """
    R0, alpha = __materials_coefficients[material]
    R = 1e-8 * R0 * (1 + alpha * (T - 20))
    A = 1e-6 * awg_area(awg)
    return R / A


