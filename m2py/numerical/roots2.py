#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iplementation using functional programming principles

"""


def iterate_root(function):

    def solver(guess, itmax=100, tol=1e-3, debug=False):
        x = guess
        for i in range(itmax):

            x_ = x
            x = function(x)

            if x_ == 0:
                error = abs(x)
            else:
                error = abs((x - x_) / x_)

            if error < tol:

                if debug:
                    print("guess = ", guess, "x = ", x, " error = ", error, "iteratiosn = ", i)

                return x

        raise Exception("Root not found")

    return solver

def iterate_root2(function):

    def solver2(guess0, guess1, itmax=100, tol=1e-3, debug=False):
        x_ = guess0
        x = guess1

        for i in range(itmax):


            x_, x = function(x_, x)

            error = abs((x - x_) / x_)

            if error < tol:

                if debug:
                    print("guess = ", (guess0, guess1), "x = ", x, " error = ", error, "iteratiosn = ", i)

                return x

        raise Exception("Root not found")

    return solver2



def newton_solver(func, derv):
    newton_iterator = lambda x: x - func(x) / derv(x)
    solver = iterate_root(newton_iterator)
    return solver


def steff_solver(func):

    def iterator(x):
        y = func(x)
        return x - y ** 2 / (func(x + y) - y)

    solver = iterate_root(iterator)
    return solver


def regulafalsi_solver(func):

    def iterator(x0, x1):

        y0 = func(x0)
        y1 = func(x1)
        x = x0 - y0 * (x1 - x0) / (y1 - y0)

        x0 = x
        y = func(x)

        if y0 * y > 0:
            x0 = x
        else:
            x1 = x

        return x0, x1

    solver = iterate_root2(iterator)

    return solver


def bissection_solver(func):
    
    def iterator(x0, x1):
        
        x = (x0 + x1) / 2

        fx = func(x)

        if func(x0) * fx < 0:
            x1 = x
        else:
            x0 = x

        return x0, x1

    solver = iterate_root2(iterator)

    return solver


def super_solver(func):
    """
    :param func:
    :return:
    """

    def steff_iterator(x):
        y = func(x)
        return x - y ** 2 / (func(x + y) - y)

    def iterator(x0, x1):

        x = (x0 + x1) / 2

        fx = func(x)

        if func(x0) * fx < 0:
            x1 = x
        else:
            x0 = x

        x1 = steff_iterator(x1)
        x0 = steff_iterator(x0)

        return x0, x1

    solver = iterate_root2(iterator)
    return solver



def test_solvers():

    print ("""
    Example find the root of
    x^2  =  exp(x)

    f(x) = x^2 - exp(x) = 0
    df(x) = 2x - exp(x)
    """)

    from math import exp


    f = lambda x: x ** 2 - exp(x)
    df = lambda x: 2 * x - exp(x)

    guesses = [-10, -2, 0, 0.52, 2, 5]

    print("NEWTON SOLVER")

    solver1 = newton_solver(f, df)
    roots1 = list(map(lambda x: solver1(x, debug=True), guesses))
    #print(list(zip(roots, guesses)))


    print("STEFESSEN SOLVER\n\n")
    solver2 = steff_solver(f)
    roots2 = list(map(lambda x: solver2(x, debug=True), guesses))


    print("\nREGULA FALSI SOLVER")
    solver3 = regulafalsi_solver(f)
    root3 = solver3(-2, 3, debug=True)
    print(root3)



    print("\nBISSECTION SOLVER")
    solver4 = bissection_solver(f)
    root4 = solver4(-20, 13, debug=True)
    print(root4)


    print("\nENHANCED SOLVER")
    solver5 = super_solver(f)
    root5 = solver5(-20, 13, debug=True, tol=1e-4)
    print(root5)


