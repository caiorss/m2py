#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Financial Toolbox
An opensource matlab-like financial toolbox.

Functions reference:    http://www.mathworks.com/help/finance/fvfix.html


https://www.wiziq.com/tutorial/753129-Fixed-income-in-Matlab-26-Apr-1800




http://www.quantcode.com/modules/mydownloads/viewcat.php?cid=9&min=120&orderby=datea&show=..
"""

from math import exp
import datetime
from m2py.numerical.roots import nraphson


__all__ = ['effrr', 'pvfix', 'fvfix', 'pvvar', 'irr', 'fvvar', 'xirr']

frequency = {
    'annulay': 1,
    'semiannualy': 2,
    'quartely': 4,
    'monthly': 12,
    'dayly': 360,
}


def moving(iterator, length, step=1):
    """
    Moving window iterator
    """
    from itertools import count, tee, islice

    ms = tee(iterator, length)
    return zip(*[islice(m, i, None, step) for m, i in zip(ms, count())])


def convert_AERtoCont(ic):
    """
    Convert annual discrete interest rate to Continuous compouning rate

    :param ic: Interest Rate Continuous, perm annum
    :return:   Interest Rate AER (Annual Equivalent Rate) per Annum

    iAER = e^ic - 1

    Reference: http://www.businessfunctions.com/index.php?pageno=9&gentop=Interest%20-%20Simple,%20Annual,%20Continous%20and%20Discount%20Factors
    """
    return exp(ic) - 1


def meanreturn(rates):
    """
    Calculates the average rate of return given a list of returns.

    [ r1, r2, r3, r4, r5 ... rn ]

    r = [(1+r1)*(1+r2)*(1+r2) .... * (1+rn)]^(1/n) - 1

    :param rates: List of interest rate
    :return: Geometric mean return

    Example:
        Suppose you have invested your savings in the stock market for five years.
        If your returns each year were 90%, 10%, 20%, 30% and -90%, what would your
        average return be during this period? Ans. -20%


    >>> import m2py.finance.finance as fin
    >>> # Return in percent
    >>> 100*fin.meanreturn([0.9, 0.10, 0.20, 0.30, -0.90])
    -20.080238920753235

    Reference: http://www.investopedia.com/ask/answers/06/geometricmean.asp
    """
    prod = 1

    for r in rates:
        prod = prod * (1 + r)

    return prod ** (1.0 / len(rates)) - 1


def eqvrate(rate, input_format, output_format='y'):
    """
    :param rate:            Interest rate in decimal format
    :param input_format:    Interest compound period
    :param output_format:   Equivalent interest rate compound period ( default 'y' yearly )
    :return:                Equivalent interest rate

    Possible values to [input_format] and [output_format]:

        m       Compounded monthly
        m/252   Compounded each        Each month has 21 business days in a 252 business-days year convention
        d       Compounded daily       30/360 days convention
     365d       Compounded daily       365 days convention
     252d       Compounded daily       252 workdays
        y or a  Compounded yearly
        y/252   Compounded yearly      252 business days convention
       2m       Compounded each 2 months
       3m       Compounded each 3 months
       4m       Compounded each 4 months
       6m       Compounded each 6 months

    Example:

    Equivalent yearly interest rate to 8% monthly interest rate

    >>> import m2py.finance.finance as fin
    >>> 100*fin.eqvrate(0.008, 'm')
    10.033869371614635
    >>> # Equivalent daily interest rate to 8%

    """
    ninput = eqvrate.formats[input_format]
    noutput = eqvrate.formats[output_format]
    yrate = (1 + rate) ** ninput - 1
    outrate = (1 + yrate) ** (1.0 / noutput) - 1
    return outrate


eqvrate.formats = {'m': 12.0,
                   'm/252' : 12,
                   'd': 360.0,
                   'y': 1.0,
                   'y/252' : 1.0,
                   'a/252' : 1.0,
                   'a': 1.0,
                   's': 2.0,
                   '252d': 252,
                   '365d': 365,
                   '2m': 6,
                   '3m': 4,
                   '4m': 3,
                   '6m': 2,
                   }


def FV(i, n, pv=0, pmt=0, fv=0):
    """
    Calculates Future Value
    :param i:   Interest rate
    :param n:   Number of periods
    :param pv:  Present Value at t=0
    :param pmt: Payment
    :param fv:  Future Value in t=end
    :return:
    """
    return fv + pv * (1 + i) ** n + pmt * ((1 + i) ** n - 1 ) / i


def PV(i, n, fv=0, pv=0, pmt=0):
    """
    Calculates Present Value
    :param i:   Interest rate
    :param n:   Number of periods
    :param fv:  Future Value in t=end
    :param pv:  Present Value at t=0   [Default: 0]
    :param pmt: Payment                [Default: 0]
    :return:
    """
    return pv + fv / (1 + i) ** n + pmt * (1 - 1 / (1 + i) ** n) / i


def ipmt(n, PV, PMT, PV0=0):
    """
    Calculates the interest rate of an installment payments

    :param n:    Number of periods
    :param PV:   Present Value/ Cash Price
    :param PMT:  Installment Payment
    :param PV0:  Payment at t=0 or Down payment [Default: 0]
    :return:     Interest rate
    """
    from m2py.numerical.roots import nraphson

    c = (PV - PV0) / PMT
    f = lambda i: (1 - 1 / (1 + i) ** n) / i - c
    df = lambda i: ((i + 1) ** -n - 1 * n) / i - (1 - 1 / (i + 1) ** n) / i ** 2
    root, _, _ = nraphson(f, df, 2, tol=1e-5, maxit=500)
    return round(root, 6)


def pmt_pv(i, n, PV, PV0=0):
    """
    Calculates the installment of a present Value.

    :param i:   Interest rate
    :param n:   Number of periods
    :param PV:  Present Value
    :param PV0: Payment at t=0/ Down Payment
    :return:
    """
    return i / (1 - 1 / (1 + i) ** n) * (PV - PV0)


def effrr(Rate, NumPeriods):
    """
    Effective rate of return
    
    Return = effrr(Rate, NumPeriods) calculates the annual effective rate of return. 
    Compounding continuously returns Return equivalent to (e^Rate-1).
    
    Return = effrr(0.09, 12)

    Return =
        0.0938  
        
    http://www.mathworks.com/help/finance/effrr.html
    """
    return (1.0 + Rate / NumPeriods) ** NumPeriods - 1


def ear(APN, N):
    """
    EAR - Effective Annual Interest Rate 
    
    Returns the EAR given the APN

     :param APN: APN Interest Rate as fraction
     :param N:   compound Frequency thats is equal to a year
     :return:    Effective annual interest rate

    Example:
        
        Consider a stated annual rate of 10%. Compounded 
        yearly, this rate will turn $1000 into $1100. 
        However, if compounding occurs monthly, $1000 would 
        grow to $1104.70 by the end of the year, rendering 
        an effective annual interest rate of 10.47%.
        
        >>> ear(0.1, 12)  # 10% compound monthly, result 10.47%
        0.10471306744129683


    """
    return (1.0 + APN / N) ** N - 1


def efi(i1, nper1, nper2):
    """
    EFI - Equivalent Frequency Interest Rate
    
    Convert an interest rate to an equivalent compound frequency
    
    :param nper1: Number of periods nper1 equal to 1 year
    :param nper2: Number of peridos nper2 equal to 1 year
    :return: i2 = (1+i1)**(nper2/nper1) - 1
    
    Example:
    
    Convert 
    
    """
    return (1 + i1) ** (nper2 / nper1) - 1


def pvfix(rate, nper, pmt):
    """
    Present value with fixed periodic payments

    PresentVal = pvfix(rate , nper, pmt )
    :param  rate: Interest rate
    :param  nper: Number of periods
    :param   pmt: Number of Payments
    :return:

    http://www.mathworks.com/help/finance/pvfix.html
    
    >> pvfix(0.06/12, 5*12, 200)
    10345.112150226414
    """

    PV = 0
    q = 1
    for i in range(nper):
        q *= 1 + rate
        PV += pmt / q

    return PV


def fvfix(Rate, NumPeriods, Payment, PresentVal=0, Due=0):
    """
    FutureVal = fvfix(Rate, NumPeriods, Payment, PresentVal, Due)
    
    Rate                    Periodic interest rate, as a decimal fraction.
    NumPeriods              Number of periods.
    Payment                 Periodic payment.
    PresentVal              (Optional) Initial value. Default = 0.
 
    Due                     "(Optional) When payments are due or made: 0 = end of
                            period  (default), or 1 = beginning of period."
    
    Example:

    This example shows how to compute the future value of a series of equal 
    payments using a savings account that has a starting balance of $1500. $200 
    is added at the end of each month for 10 years and the account pays 9% 
    interest compounded monthly.
    
    
    
    >> print "%.3E" % fvfix(0.09/12, 12*10, 200, 1500, 0)
    4.238E+04    
    
    >> print fvfix(0.05, 5, 1000, 0, 1)
    5801.9128125

    
    http://www.investopedia.com/articles/03/101503.asp
    http://www.mathworks.com/help/finance/fvfix.html
    """

    FV = 0
    q = 1

    if not Due:

        for i in range(NumPeriods):
            FV += Payment * q
            q *= 1 + Rate
    else:
        for i in range(1, NumPeriods + 1):
            FV += Payment * (1 + Rate) ** i

            # print "i = ", i

    FV = FV + PresentVal * (1 + Rate) ** NumPeriods

    return FV


def __pvvar(CashFlow, Rate, CFDates=[], format=r"%m/%d/%Y", ndays=365):
    """ Auxiliary pvvar function """

    # print format
    PV = 0
    i = Rate

    dt = lambda s: datetime.datetime.strptime(s, format)
    dates = list(map(dt, CFDates))
    # dates = [datetime.datetime.strptime(s, format) for s in CFDates]


    if not CFDates:

        for n, c in enumerate(CashFlow):
            PV = PV + c / (1 + i) ** n

    else:
        d0 = dates[0]

        for c, date in zip(CashFlow[1:], dates[1:]):
            np = (date - d0).days / ndays
            PV = PV + c * 1 / (1 + i) ** np

        PV = PV + CashFlow[0]

    # print "PV = ", PV
    return PV


def pvvar(CashFlow, Rate, CFDates=[], format=r"%m/%d/%Y", ndays=365):
    """
     Present value of varying cash flow
    
    :param CashFlow:  A list of varying cash flows.
    :param Rate:      Periodic interest rate. Enter as a decimal fraction. 
    :param CFDates:   (Optional) A vector of serial date numbers or date strings 
                      on which the cash flows occur. 
    
    CashFlow
    A vector of varying cash flows. Include the initial investment as the initial 
    cash flow value (a negative number). If CashFlow is a matrix, each column is treated as 
    a separate cash-flow stream.
    
    Rate
    Periodic interest rate. Enter as a decimal fraction. If CashFlow is a matrix, 
    a scalar Rate is allowed when the same rate applies to all cash-flow streams i
    n CashFlow. When multiple cash-flow streams require different discount rates, 
    Rate must be a vector whose length equals the number of columns in CashFlow.
     
    CFDates
    Optional) A vector of serial date numbers or date strings on which the cash flows occur. 
    Specify CFDates when there are irregular (nonperiodic) cash flows. The default assumes 
    that CashFlow contains regular (periodic) cash flows. If CashFlow is a matrix, and all 
    cash-flow streams share the same dates, CFDates can be a vector whose length matches the 
    number of rows in CashFlow. When different cash-flow streams have different payment dates, 
    specify CFDates as a matrix the same size as CashFlow.
        
    
    
    This cash flow represents the yearly income from an initial investment of $10,000. The annual interest rate is 8%.

    Example1:
    
        Year 1  $2000
        Year 2  $1500
        Year 3  $3000
        Year 4  $3800
        Year 5  $5000
        
        >> PresentVal = pvvar([-10000, 2000, 1500, 3000, 3800, 5000], 0.08 )
        PresentVal = 1715.38623116
    
    Example2:
    An investment of $10,000 returns this irregular cash flow. The original investment 
    and its date are included. The periodic interest rate is 9%. 
    
        Cash Flow   Dates
        ($10000)    January 12, 1987
        $2500       February 14, 1988
        $2000       March 3, 1988
        $3000       June 14, 1988
        $4000       December 1, 1988
        
        >> CashFlow = [-10000, 2500, 2000, 3000, 4000] ;
        >> CFDates = ['1/12/1987', '2/14/1988', '3/03/1988', '6/14/1988', '12/1/1988'] ;
        >> PresentVal = pvvar(CashFlow, 0.09, CFDates)
        PresentVal = 142.164804727
        
        >> CashFlow = [-10000, 2500, 2000, 3000, 4000] ;
        >> CFDates = ['1/12/1987', '2/14/1988', '3/03/1988', '6/14/1988', '12/1/1988'] ;
        >> PresentVal = pvvar(CashFlow, [0.07, 0.09, 0.11], CFDates)
        PresentVal = [419.0136433133739, 142.16480472687726, -122.12751414382365]
    
    Ref: http://www.mathworks.com/help/finance/pvvar.html
    """

    if isinstance(Rate, list):
        PV = lambda r: __pvvar(CashFlow, r, CFDates, format, ndays)
        pv = list(map(PV, Rate))
    else:
        pv = __pvvar(CashFlow, Rate, CFDates, format, ndays)
    return pv


def irr(CashFlow, all=False):
    """
    irr - Internal Rate of Return
    
    :param CashFlow: A list with the cash flow stream
    :return: A list containing the internal rate of return 
    
    Example:
    
        >>> irr([-100000, 10000, 20000, 30000, 40000, 50000])
        [0.12005761954196337]
    
    From: http://www.mathworks.com/help/finance/irr.html
    """
    from numpy.polynomial import Polynomial as P
    from numpy import isreal

    roots = P(CashFlow).roots()
    # roots = [float(r) for r in roots if isreal(r)]

    if not all:
        roots = [r for r in roots if isreal(r) and r > 0]
        roots = list(map(float, roots))

    r2i = lambda r: 1 / r - 1

    i = list(map(r2i, roots))

    return i


def fvvar(CashFlow, Rate, CFDates=[], format=r"%m/%d/%Y", ndays=365):
    """
    fvvar(CashFlow, Rate, CFDates)
    
    CashFlow    "A vector of varying cash flows. Include the initial investment
                as the initial cash flow value (a negative number)."
    
    Rate        Periodic interest rate. Enter as a decimal fraction.
    
    CFDates     "(Optional) For irregular (nonperiodic) cash flows, a
                vector of dates on which the cash flows occur. Enter dates as serial
                date numbers or date strings. Default assumes CashFlow contains
                regular (periodic) cash flows."
    
    
    Cash Flow   Dates
    ($10000)    January 12, 2000
    $2500       February 14, 2001
    $2000       March 3, 2001
    $3000       June 14, 2001
    $4000       December 1, 2001

    """
    # print format
    FV = 0
    i = Rate
    q = 1

    dt = lambda s: datetime.datetime.strptime(s, format)
    dates = list(map(dt, CFDates))
    # dates = [datetime.datetime.strptime(s, format) for s in CFDates]

    if not CFDates:

        CashFlow.reverse()

        for n, c in enumerate(CashFlow):
            FV += c * q
            q *= 1 + Rate

    else:

        dates.reverse()
        CashFlow.reverse()

        dend = dates[0]

        print("dend = ", dend)

        for c, date in zip(CashFlow, dates):
            dt = dend - date
            np = dt.days / ndays

            FV = FV + c * (1 + i) ** np

            print("c = ", c, " date = ", date, " dt = ", dt, "np = ", np, " FV = ", FV)

            # FV = FV + CashFlow[0]
            # np = (dates[0] - dates[-1]).days/ndays
            # FV = FV + CashFlow[0]*(1+i)**np

    # print "PV = ", PV
    return FV


# CashFlow = [-10000, 2500, 2000, 3000, 4000];
# CFDates = ['01/12/2000', '02/14/2001', '03/03/2001', '06/14/2001', '12/01/2001'];

# FutureVal = fvvar(CashFlow, 0.09, CFDates)

# print FutureVal

# FutureVal = fvvar([-10000, 2000, 1500, 3000, 3800, 5000], 0.08)
# print FutureVal


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


def xirr(CashFlow, CFDates, ndays=365, format=r"%m/%d/%Y", guess=1.0):
    """

    :param CashFlow:        A list containing the cash flow
    :param CashFlowDates:   A list containing the dates
    :param ndays:           Number of days in a year
    :param format:          Date format [default: "%m/%d/%Y"]
    :param guess:           Initial guess to Newton Raphson method (default 2)
    :return:                Internal rate of return for a schedule of nonperiodic cash flows.

    Example:
        >>> CashFlow = [-10000, 2500, 2000, 3000, 4000]
        >>> CFDates = ['01/12/2007', '02/14/2008', '03/03/2008', '06/14/2008', '12/01/2008']
        >>> Return = xirr(CashFlow, CFDates)
        >>> print 100*Return
        10.0643783426

    """

    dt = lambda s: datetime.datetime.strptime(s, format)
    dates = list(map(dt, CFDates))
    coefs = CashFlow

    d0 = dates[0]

    cashflow_exponents = []

    for d, c in zip(dates, CashFlow):
        dt = d - d0
        np = dt.days / ndays
        # print "d =", d, "c =", c, " dt = ", dt.days, "np = ", np
        cashflow_exponents.append(np)

    d_cashflow_exponents = [np - 1 for np in cashflow_exponents[1:]]
    d_coefs = [c * np for c, np in zip(coefs[1:], cashflow_exponents[1:])]

    # print "coefs ", coefs
    # print "cashflow_exponents ", cashflow_exponents
    # print "d_coefs", d_coefs
    # print "d_cashflow_exponents", d_cashflow_exponents

    f = lambda x: expsum(x, coefs, cashflow_exponents)
    df = lambda x: expsum(x, d_coefs, d_cashflow_exponents)

    x, _, _ = nraphson(f, df, guess)
    i = 1 / x - 1
    return i


def payper(Rate, NumPeriods, PresentValue, FutureValue, Due):
    """
    Periodic payment of loan or annuity

    :param Rate:            Interest rate per period. Enter as a decimal fraction.
    :param NumPeriods:      Number of payment periods in the life of the instrument.
    :param PresentValue:    Present value of the instrument.
    :param FutureValue:     (Optional) Future value or target value to be attained after NumPeriods periods.
    :param Due:             (Optional) When payments are due: 0 = end of period (default), or 1 = beginning of period.
    :return:


    This example shows how to find the monthly payment for a three-year
    loan of $9000 with an annual interest rate of 11.75%.

    Example:
        >>> Payment = payper(0.1175/12, 36, 9000, 0, 0)
        297.85528322

    """

    x = 1 / (1 + Rate)
    q = (x ** (NumPeriods + 1) - x ) / (x - 1)
    PM = -1 * (FutureValue - PresentValue) / q

    # print "PM = ", PM
    return PM


def annuterm(Rate, Payment, PresentValue, FutureValue, Due):
    """
    :param Rate:            Interest rate per period, as a decimal fraction.
    :param Payment:         Payment per period.
    :param PresentValue:    Present value.
    :param FutureValue:     FutureValue	(Optional) Future value. Default = 0.
    :param Due:             Due	"(Optional) When payments are due: 0 = end of period (default),  or 1 = beginning of period."
    :return:
    """
    i = Rate
    pmt = Payment
    pv = PresentValue
    fv = FutureValue

    fv = lambda n: pv * (1 + i) ** (n + 1) + (pmt - pv) * (1 + i) ** n - pmt
    dfv = lambda n: (n + 1) * pv * (1 + i) ** n + n * (pmt - pv) * (1 + i) ** (n - 1)

    n = nraphson(fv, dfv, 1)

    return n


    # print payper(0.1175 / 12, 36, 9000, 0, 0)

    # NumPeriods = annuterm(0.09/12, 200, 1500, 5000, 0)
    # print NumPeriods