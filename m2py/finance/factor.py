#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example:

Finding Future Value

    A person deposits $5000 into an account which pays interest at a rate of 8% per year.
    What is the amount in the account after 10 years ?

    Solution:

    5000*(F/P, 8%, 10)
    >>> 5000*factor('F/P', 0.08, 10)
    10794.6249864

Finding Present Value

    A small company wants to make a single deposit now so it will have enough money to
    purchase a backhoe costing $50,000 five years from now.  If the account will earn
    interest of 10% per year, the amount that must be deposited now is nearest to:

    >>> 50000*factor('P/F', 0.10, 5)
    31046.066153

Uniform Series Involving P/A

    A chemical engineer believes that by  modifying the structure of a certain water
    treatment polymer, his company would earn an extra $5000 per year. At an interest
    rate of 10% per year, how much could the company afford to spend now to just
    break even over a 5 year project period?

    Cash Flow:

            A = $ 5000
    ____|___|___|___|___|
    |0  1   2   3   4   5
    |
    -P

    Solution:
    >>> 5000*factor('P/A', 0.10, 5)
    18953.933847

Uniform Series Involving F/A
    An industrial engineer made a modification to a chip manufacturing process that
    will save her company $10,000 per year. At an interest rate of 8% per year, how
    much will the savings amount to in 7 years?

    Cash Flow:


                              F = ?
                              |
                              |
    0    1    2   3  ...  6   7
    ---------------------------
         |    |   |       |   |
        A = 10,000.00

    Solution:

    >>> 10000*factor('F/A', 0.08, 7)
    89228.0335974



 Reference: http://ocw.mit.edu/courses/nuclear-engineering/22-812j-managing-nuclear-technology-spring-2004/lecture-notes/lec03slides.pdf
 Reference: http://www.webpages.uidaho.edu/~mlowry/Teaching/EngineeringEconomy/Supplemental/Engineering_Economics_Excerpt_from_FE_Reference.pdf

"""

__all__ = ['factor']

def __discount_FP(i, n):
    """
    Future worth factor (compound amount f actor)

    Factor:  (F/P, i, N)
    Formula: F=P(1+i^N

    :param i:
    :param n:
    :return:

    Cash Flow:
                 F
                 |
                 |
    --------------
    |
    P

    """
    return (1 + i) ** n


def __discount_PF(i, n):
    """
    Present worth factor

    Factor:  (P/F, i, N)
    Formula: P = F(1+i)^N

    :param i:
    :param n:
    :return:

    Cash Flow:
                 F
                 |
                 |
    --------------
    |
    P
    """
    return (1 + i) ** (-n)


def __discount_AF(i, n):
    """
    Sinking fund factor

    Factor:  (A/F, i, N)
    Formula: A = F.[i / ((1 + i)^n - 1)]

    :param i:
    :param n:
    :return:

    Cash Flow:
                   F
                   |
                   |
                   |
    -----------------
    |    |    |    |
    |    |    |    |
    A    A    A    A
    """
    f = (1 + i) ** n
    return i / (f - 1)


def __discount_PA(i, n):
    """
    Present worth of an annuity factor

    Factor: (P/A, i, N)


    :param i:
    :param n:
    :return:


    Cash Flow


    """
    f = (i + 1) ** n
    return (f - 1) / (i * f)


def __discount_FA(i, n):
    """
    Uniform series compound amount factor (aka future- worth-of-an- annuity factor)
     
    :param i: 
    :param n: 
    :return:
    
    Cash Flow:
                   F
                   |
                   |
                   |
    -----------------
    |    |    |    |
    |    |    |    |
    A    A    A    A
    """
    f = (1+i)**n
    return (f-1)/i


def __discount_AP(i, n):
    """
    Capital recovery factor
    (A/P, i, N)

    :param i:
    :param n:
    :return:

    Cash Flow

         A    A    A    A
         |    |    |    |
    -----|----|----|----|
    |
    |
    |
    P
    """
    f = (i + 1) ** n
    return i * f / (f - 1)


def factor(name, i, n):
    """
    Engineering Economic Factors

    :param name: Factor name
    :param i:    Interest Rate
    :param n:    Number of periods
    :return:     Economic factor
    :type name:  str
    :type i:     float/int
    :type n:     float/int
    :rtype:      float

    Possible values of [name]:


        Single Payment
        -----------------------------------
        Value  Entry          Converts

        'P/F'  (P/F, i, n)    to P given F  present worth factor
        'F/P'  (F/P, i, n)    to F given P  capital recovery facto

        Uniform Series Sinking Funds
        -----------------------------------
        Value  Entry          Converts

        'A/F'  (A/F, i, n)    to A given F  compound amount factor
        'F/A'  (F/A, i, n)    to F given A  sinking fund factor

        Uniform Series Present Worth
        -----------------------------------
        Value  Entry          Converts
        
        'P/A'  (P/A, i, n)    to P given A  present worth factor
        'A/P'  (A/P, i, n)    to A given P  capital recovery factor
        
    
    """
    f = factor.__dispatch__[name]
    return f(i, n)


factor.__dispatch__ = {
    'F/P': __discount_FP,
    'P/F': __discount_PF,
    
    'F/A': __discount_FA,
    'A/F': __discount_AF,
    
    'P/A': __discount_PA,
    'A/P': __discount_AP,
}


def main():
    f = factor

    print("""
Example:

Finding Future Value
    A person deposits $5000 into an account which pays interest at a rate of 8% per year.
    What is the amount in the account after 10 years ?

    Solution:

    5000*(F/P, 8%, 10)
    >>> 5000*factor('F/P', 0.08, 10)
    """)
    print(5000*factor('F/P', 0.08, 10))


    print("""
Finding Present Value
    A small company wants to make a single deposit now so it will have enough money to
    purchase a backhoe costing $50,000 five years from now.  If the account will earn
    interest of 10% per year, the amount that must be deposited now is nearest to:

    >>> 50000*factor('P/F', 0.10, 5)
    """)
    print(50000*factor('P/F', 0.10, 5))


    print("""
Uniform Series Involving P/A
    A chemical engineer believes that by  modifying the structure of a certain water
    treatment polymer, his company would earn an extra $5000 per year. At an interest
    rate of 10% per year, how much could the company afford to spend now to just
    break even over a 5 year project period?

    Cash Flow:

            A = $ 5000
    ____|___|___|___|___|
    |0  1   2   3   4   5
    |
    -P

    Solution:
    >>> 5000*factor('P/A', 0.10, 5)
    """)
    print(5000*factor('P/A', 0.10, 5))

    print("""
Uniform Series Involving F/A
    An industrial engineer made a modification to a chip manufacturing process that
    will save her company $10,000 per year. At an interest rate of 8% per year, how
    much will the savings amount to in 7 years?

    Cash Flow:


                              F = ?
                              |
                              |
    0    1    2   3  ...  6   7
    ---------------------------
         |    |   |       |   |
        A = 10,000.00

    Solution:

    >>> 10000*factor('F/A', 0.08, 7)

    """)
    print(10000*factor('F/A', 0.08, 7))

if __name__ == "__main__":
    main()