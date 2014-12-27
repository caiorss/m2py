#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m2py.numerical.numerical import read_table

s = read_table("superheated_steam.txt")

_pressure_tables = {}

for line in zip(*list(map(s.get, s.headers))):
    #print line

    p = line[1]
    data = (line[0],) + line[2:]
    #print data

    p_ = str(int(p))

    if p_ not in list(_pressure_tables.keys()):
        _pressure_tables[p_] = []
    else:
        _pressure_tables[p_].append(data)


_pressures = list(_pressure_tables.keys())

pressures = sorted(map(float, _pressures))
_pressures = [str(int(x)) for x in pressures]


def find_temperature_data(T, data):

    for idx, d in enumerate(data):
        t = d[0]
        if t >= T:
            break

    _data = data[idx]

    return (idx, _data)


def find_pt(P, T):

    for idx, (p, psrt) in enumerate(zip(pressures, _pressures)):
        if p > P:
            break

    _p = pressures[idx-1]
    _pstr = _pressures[idx-1]
    print(dict(idx=idx, p=p, pstr=psrt, _p=_p))

    data1 = _pressure_tables[psrt]
    idx1, x11 = find_temperature_data(T, data1)
    x12 = data1[idx1-1]



    data2 = _pressure_tables[_pstr]
    idx2, x21 = find_temperature_data(T, data2)

    print("idx2 = ", idx2)

    x22 = data2[idx2-1]

    print("x11 ", x11)
    print("x12 ", x12)
    print("x21 ", x21)
    print("x22 ", x22)


find_pt(200, 300)

