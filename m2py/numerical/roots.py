#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Root finding Methods for solving nonlinear equations.


"""


class RootFindErrror(Exception):
    def __init__(self, *args, **kwarg):
        # Set some exception infomation
        self.msg = "".join(args) + " " + str(kwarg)
        print(self.msg)


def bissection(f, a, b, tol=1e-3, maxit=2000, debug=False):
    """
    Bissection root finding method
    :param f:     Function to found root
    :param a:     First value of interval where the root lies
    :param b:     Second value of interval where the root lies
    :param tol:   Tolerance f(c) < tol, to stop the iteration
    :parm maxit:  Maximum number of iterations
    :parma debug: True/False, If true prints debug message
    :return:       Equation root

    Example Find the root of  exp(-x)=3log(x):
        >>> from math import exp, log
        >>> f = lambda x: exp(-x) -3*log(x)
        >>> bissection(f, 0.1, 0.5)
        1.1154052734374997

    Reference: http://mat.iitm.ac.in/home/sryedida/public_html/caimna/transcendental/bracketing%20methods/bisection/bisection.html
    """
    it = 0

    while it < maxit:
        c = (a + b) / 2

        fc = f(c)

        if f(a) * fc < 0:
            b = c
        else:
            a = c

        if abs(fc) < tol:
            break

        it += 1

    if debug:
        print("x =", c)
        print("it =", it)
        print("fc ", fc)

    if fc > tol:
        raise RootFindErrror("Root not found ", x=c, it=it, fc=fc)

    return c


def nraphson(f, df, x0, tol=1e-3, maxit=20000):
    """
    Newto Raphson Equation Solving

    Compute Equation roots given its equation and derivate

    Xn  = Xn-1 - f(x)/f'(x)

    :param f:       Function f(x) handler
    :param df:      Derivate of f'(x) handler
    :param x0:      Inital guess
    :param maxit:   Max number of iterations
    :param tol:     Tolerance
    :return:        [ x, it, error ]
    """
    x = 0
    x_ = x0
    it = 0
    error = 0

    while it < maxit:
        it += 1
        x = x_ - f(x_) / df(x_)
        error = abs(x - x_) / abs(x_)

        if error < tol:
            break
        x_ = x

    # print "it =", it
    # print "error = ", error

    return x, it, error


def steffenssen(f, x0, tol=1e-3, maxit=20000):
    """
    Stefessen Method for Equation Solving

    Compute equation roots based on stefessen method

    :param f:       Function f(x) handler
    :param x0:      Inital guess
    :param maxit:   Max number of iterations
    :param tol:     Tolerance
    :return:        [ x, it, error ]


    y = f(Xn)
    Xn+1  = Xn -  y^2/( f(Xn+y) - y)

    Example:

    Solve  exp(x) = 3x^2

        >>> import m2py.numerical.roots as r
        >>>
        >>> from math import exp
        >>> f = lambda x: exp(x) - 3*x**2
        >>> r.steffenssen(f, 4, tol=1e-3, maxit=200)
        (3.7330790286333886, 55, 3.3912123882373635e-06)

    Reference:
    [1]J. P. Jaiswal, NEW EFFICIENT STEFFENSEN TYPE METHOD FOR SOLVING NONLINEAR EQUATIONS
    http://arxiv.org/pdf/1304.4703.pdf

    [2] http://www.cs.technion.ac.il/~asidi/Sidi_Journal_Papers/P091_JOMA2006.Vol6.pdf
    """

    x = x0
    it = 0
    error = 0

    while it < maxit:
        it += 1

        y = f(x)
        x -= y ** 2 / (f(x + y) - y)

        error = abs(y)
        if error < tol:
            break

    if error > tol:
        raise RootFindErrror("Root not found ", x=x, it=it)

    return x, it, error


def stefessen2(f, x0, tol=1e-3, maxit=20000):
    """

    :param f:
    :param x0:
    :param tol:
    :param maxit:
    :return:


    Reference: http://www.os-cfd.ru/UserFiles/File/e-library/FSI/016_lec08-2x3.pdf
    """

    x = x0
    it = 0
    error = 0

    while it < maxit:
        it += 1

        # Atikens Accelerator
        x1 = f(x0)
        x2 = f(x1)
        x = x0 - (x1 - x0) ** 2 / (x2 - 2 * x1 + x0)

        y = f(x)
        x = x - y ** 2 / (f(x + y) - y)

        error = abs(y)

        if error < tol:
            break
        x0 = x


    return x, it, error


def regualfalsi(f, x0, x1, tol=1e-3, maxit=200, debug=False):
    """
    Solve equation using the false position method
    Regula-Falsi position

    :param f:
    :param x0:
    :param x1:
    :param tol:
    :param maxit:
    :return:

    Reference: http://www.physics.arizona.edu/~restrepo/475A/Notes/sourcea-/node17.html
    """

    x = x0
    it = 0
    error = 0

    while it < maxit:
        it += 1

        y0 = f(x0)
        y1 = f(x1)
        error = abs(y1)

        #print x, it, error

        # if debug:
        #     print x0, x1, y0, y1, it, error

        # error = abs(x - x1)


        if error < tol:
            break

        if abs(y1-y0)< 1e-6:
            raise  RootFindErrror("Regula falsi can't compute root y1=y0, denominator zero ", it=str(it), error=str(error), x=str(x))

        x = x0 - y0 * (x1 - x0) / (y1 - y0)

        x0 = x
        y = f(x)

        if y0 * y > 0:
            x0 = x
        else:
            x1 = x



    if error > tol:
        raise RootFindErrror("Root not found ", x=x, it=it, error=error)

    return x, it, error

