#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Brazilian Bonds Calculation and Validation

"""
import dtime as dt



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


def payment_dates(settle, maturity):
    """
    Generates the payment dates between settle and maturity in brazilian markets

    :param settle:
    :param maturity:
    :return:



    """
    date_s = dt.date_dmy(settle)
    date_m = dt.date_dmy(maturity)

    ys, _, _ = dt.date2ymd(date_s)
    ym, _, _ = dt.date2ymd(date_m)
    dates = []

    for year in range(ys, ym + 1):
        # payment at 01/01/xx
        dsemester1 = dt.ymd2date(year, 1, 1)
        # payment at 01/07/xx
        dsemester2 = dt.ymd2date(year, 7, 1)
        dates.extend([dsemester1, dsemester2])

    dates = filter(lambda d: date_s < d <= date_m, dates)

    dates[0] = dt.daysadd(dates[0], -1)

    return dates


def bond_price(ytm, settle, maturity, couponRate=0.0, facevalue=1000.0, coupondates=[]):
    """
    Pre-Fixed Brazilian bonds calculations

    :param ytm:          Yield to maturity rate
    :param settle:   settle date
    :param maturity:     Maturity date
    :param couponRate:   Coupon interest compounded twice per year  [default = 0.0]
    :param facevalue:    Face Value [default: 1000.0 ]
    :return:             price

    Where:
        price : bond price
    """
    # ytm = abs(ytm)

    couponRate = (1 + couponRate) ** 0.5 - 1

    date0 = dt.date_dmy(settle)
    daten = dt.date_dmy(maturity)

    if couponRate and not coupondates:
        coupondates = payment_dates(settle, maturity)

    PV = 0

    for date in coupondates:
        # Number of business days between settle and
        # coupon payment
        N = dt.daysbus(date0, date)
        f = N / 252.0

        #print dict(N=N, f=f, date=dt.date2str_dmy(date))

        PV += round(1 / (1 + ytm) ** f, 8)

    Nm = dt.daysbus(date0, daten)
    fm = Nm / 252.0
    PV = facevalue * (couponRate * PV + round(1 / (1 + ytm) ** fm, 8))
    return round(PV, 2)


def bond_coupon(couponRate, facevalue=1000.0):
    """
    Calculates the Coupon Value

    :param couponrate: Coupon interest rate % a.a for a brazilian bond that pays twice per year.
    :param facevalue:  Face Value of one bond, default 1000.0
    :return:
    """
    couponRate = (1 + couponRate) ** 0.5 - 1
    return round(facevalue * couponRate, 2)


def bond_yield(price, couponRate, settle, maturity, facevalue=1000.0):
    """
    Calculates the Bond Yield or Internal rate of return.

    :param price:        Spot Price of the bond
    :param couponRate:   Coupon interest rate per year
    :param settle:       Settlement date
    :param maturity:     Maturity date
    :return:
    """
    couponRate = (1 + couponRate) ** 0.5 - 1

    from m2py.numerical import roots

    date0 = dt.date_dmy(settle)
    daten = dt.date_dmy(maturity)

    if couponRate:
        coupondates = payment_dates(settle, maturity)
    else:
        coupondates = []

    expoents = []
    coefficients = []
    k = couponRate

    for date in coupondates:
        # Number of business days between settle and
        # coupon payment
        N = dt.daysbus(date0, date)
        c = N / 252.0

        #print dict(c=c, N=N)

        expoents.append(c)
        coefficients.append(k)

    # Assemble Equation
    # PV: Price, FV: Face Value
    #
    # f(x) = a1.X^c1 + a2.X^c2 + .... + an.X^cn + a0
    #  f(x) = kX^c1 + kX^c2 + k.X^c3 + ... + (k+1).X^Cn - PV/FV
    #
    #  a1 = k, a2 = k, a3 = k, .... an= k+1,  a0 = -PV/FV
    #  c0 = 0
    #
    #  x = 1/(1+YMT)
    #
    coefficients[-1] = coefficients[-1] + 1
    coefficients.append(-price / facevalue)
    expoents.append(0)

    #from pprint import pprint
    #pprint(zip(coefficients, expoents))

    equation = make_expsum_function(coefficients, expoents)

    #print "result = ", equation(1 / (0.1652 + 1))

    #print stefessen(equation, 0.46, 1e-3, 200)

    #result = roots.regualfalsi(equation, 0, 1, 1e-6, 400)
    result = roots.steffenssen(equation, 1, 1e-6, 400)
    print result
    x = result[0]

    #print "x = ", x
    YTM = 1 / x - 1
    return YTM
    #print "YTM = ", YTM


def bond_quatinty(price, investment, minimum_fraction=0.1):
    """
    Computes the quantity of bonds purchased given the investment,
    bond price per unit, and the minimum fraction of a bond that
    can be purchased

    :param investment:          Amount of money that will be invested
    :param minimum_fraction:    Minimum fraction that can be purchased
    :param price:               Price of bond per unit

    :return:                    [quantity of bonds purchased, Total Value Invested, Eror%]
    """

    Qf = int(investment / (minimum_fraction * price))
    Q = Qf * minimum_fraction
    value = Q * price
    error = (investment - value) / value * 100
    return [Q, value, error]



# Rentabilidade total bruta
def bond_return(price, sellprice=1000.0):
    """
    Bond total return for a zero coupon bond

    :param price:       Price which the bond was purchased
    :param sellprice:   Price which the bond was sold
    :return:            sellprice/price - 1
    """
    return sellprice/price - 1

# Lucro total bruto
def bond_profit(price, sellprice=1000.0):
    """
    Bond total profit for a zero coupon bond

    :param price:       Price which the bond was purchased
    :param sellprice:   Price which the bond was sold
    :return:            1 - price/sellprice
    """
    return 1 - price/sellprice



def test_payment_dates_br():
    """
    Test routine: payment_dates_br(settle, maturity)
    Reference: http://www.tesouro.fazenda.gov.br/documents/10180/258262/NTN-F/1d23ed84-4921-49f4-891b-fececd3115f9

    Expected Result:
    ['01/07/2004',
     '01/01/2005',
     '01/07/2005',
     '01/01/2006',
     '01/07/2006',
     '01/01/2007',
     '01/07/2007',
     '01/01/2008']
    :return:
    """
    from pprint import pprint

    pprint(map(dt.date2str_dmy, payment_dates("9/1/2004", "1/1/2008")))


# print bond_price(ytm=0.1652, settle="09/01/2004", maturity="01/01/2008", couponRate=0.1)

#print 100*bond_yield(828.5, 0.10, "09/01/2004", "01/01/2008")


#print bond_coupon(couponRate=0.1, facevalue=1000.0)

#print bond_quatinty(828.5, 10000.0)


# http://www.tesouro.fazenda.gov.br/documents/10180/258262/LTN/a5832856-3afc-460b-9ed2-8d9db1100b8f
#print bond_price(0.1246, '20/12/2006', '01/01/2009', 0)

# print 10*"-"
# d0 = dt.date_dmy('01/01/2008')
# print d0.isoweekday()
#
# print dt.isbusday(dt.date_dmy('6/12/2014'))
# print dt.isbusday(dt.date_dmy('01/07/2007'))
# print dt.isbusday(dt.date_dmy('01/01/2008'))
# print dt.isbusday(dt.date_dmy('15/12/2014'))
#
#
# print dt.nextbusday(dt.date_dmy('06/12/2014'))