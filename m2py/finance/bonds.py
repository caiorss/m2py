#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log

from m2py.finance import finance


def expsum(x, coefficient, powers):
    """
    :param x:           Input variable
    :param coefficient: List of coefficients [ a0, a1, a2, a3, a4, ... an]
    :param powers:      List of expoents     [ c0, c1, c2, c3, c4, ... cn]
    :return:            a0.x^c0 + a1.x^c1 + a2.x^c2 + a3.x^c3 + ...
    """
    S = 0
    for c, p in zip(coefficient, powers):
        S += c * x ** p

    return S

def make_expsum_function(coefficents, powers):
    f = lambda x: expsum(x, coefficents, powers)
    return f




def bond_cashflow(price, couponRate, maturity, freq=1, facevalue=1000.0):

    CF = couponRate*facevalue/freq
    N = maturity*freq

    times = [1.0/freq*k for k in range(N+1)]

    cashflow = [CF for k in range(N-1)]
    cashflow.insert(0, -price)
    cashflow.append( facevalue+CF)

    return times, cashflow



def bond_yield(price, couponRate, maturity, freq=1, facevalue=1000.0):
    """
    :param price:       Bond Price
    :param couponRate:  Coupon Rate
    :param maturity:    Time to maturity ( remdemption )
    :param freq:        Frquency of coupon payment per year
    :param facevalue:   Face value of the bond ( default 1000.0 )
    :return:
    """
    from m2py.numerical import roots

    times, cashflow = bond_cashflow(price, couponRate, maturity, freq, facevalue)

    f = make_expsum_function(cashflow, times)

    result = roots.regualfalsi(f,0, 1.1, 1e-6, 500)
    #print "result = ", result
    x = result[0]
    ytm = 1.0 / x - 1

    return ytm


def bond_price(ytm, couponRate, maturity, freq=1, facevalue=1000.0):
    """

    :param ytm:
    :param couponRate:
    :param maturity:
    :param freq:
    :param facevalue:
    :return:
    """
    times, cashflow = bond_cashflow(0, couponRate, maturity, freq, facevalue)

    x = 1.0/(1+ytm)
    pv = 0

    for c, n in zip(cashflow, times):
        pv += + c * x ** n

    return pv


def bond_macaulay_duration(ytm, couponRate, maturity, freq=1, facevalue=1000.0):
    """
    :param price:       Bond Price
    :param couponRate:  Coupon Rate
    :param maturity:    Time to maturity ( remdemption )
    :param freq:        Frquency of coupon payment per year
    :param facevalue:   Face value of the bond ( default 1000.0 )
    :return:
    """
    times, cashflow = bond_cashflow(0, couponRate, maturity, freq, facevalue)
    price = bond_price(ytm, couponRate, maturity, freq, facevalue)

    x = 1.0/(1+ytm)
    D = 0

    for c, n in zip(cashflow, times):
        pv = c * x ** n
        D = D + pv*n

    #print "D = ", D

    D = D/price

    return D



if __name__ == "__main__":

    #print bond_yield(950.0, 0.10, 5, 1000.0)

    #cashflow = bond_cashflow(950.0, 0.10, 5)

    print(bond_cashflow(954.53, 0.080, 2, 2, 1000.0))

    ytm= bond_yield(954.53, 0.080, 2, 2, 1000.0)

    print("ytm = ", ytm)

    price = bond_price(ytm, 0.08, 2, 2, 1000.0)

    print("price = ", price)

    print(bond_macaulay_duration(0.06, 0.08, 4, 2, 1000.0))

    print(bond_price(0.06, 0.08, 4, 2))


    #print finance.irr(cashflow)[0]