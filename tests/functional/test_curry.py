#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from math import (sin, cos, tan, exp)


def f(x, y, z):
    return x + y + z

def ftest(x, y, z, w=10):
    """ Test Documentation """
    return x + y + z + w

fun_name     = lambda fun: fun.__name__
fun_args     = lambda fun: fun.__code__.co_varnames
fun_dic      = lambda fun: fun.__dict__
fun_module   = lambda fun: fun.__module__
fun_freeargs = lambda fun: fun.__code__.co_varnames[:-len(fun.__defaults__)]
fun_defaults = lambda fun: list(zip(fun.__code__.co_varnames[-len(ftest.__defaults__):], fun.__defaults__))
fun_signature = lambda fun: (fun_freeargs(fun), fun_defaults(fun))


def signature(func):
    try:
        args, constargs = fun_signature(func)
        args = list(args)
        constargs = list(constargs)
        lst1 = list(map(lambda x: "{} = {}".format(x[0], x[1]), constargs))
        txt1 = ", ".join(args + lst1)
        #print(txt1)
        return txt1
    except Exception:
        pass


def debug_func(func):
    print("Name :", func.__name__)
    print("Varnames :", func.__code__.co_varnames)
    print("Free vars :", func.__code__.co_freevars)
    print("Defaults :", func.__defaults__)
    print("Dict :", func.__dict__)
    print("Module :", func.__module__)
    print("Signature : ", signature(func))
    print("Doc: \n", func.__doc__)
    print(10 * "-" + "\n")



def is_curried(func):
    return hasattr(func, "parent")

def curry(func, *params):
    debug_func(func)

    varnames = func.__code__.co_varnames

    if len(params) >= len(varnames):
        raise Exception("Error: Wrong number of parameters")

    if not is_curried(func):

        def curried(*args):
            argc = list(params) + list(args)
            return func(*argc)

        curried.__doc__ = func.__doc__
        curried.__name__ = func.__name__ + "_curried"
        curried.__signature__ = fun_args(func)[len(params):]
        curried.__constants__ = fun_defaults(func)

        curried.parent = func

        curried.curryargs = list(params)


    else:
        curryargs = func.curryargs

        funcp = func.parent

        def curried(*args):
            return funcp(*(curryargs + list(args)))

        curried.__doc__ = funcp.__doc__

        curried.__doc__ = func.__doc__
        curried.__name__ = func.__name__
        curried.__signature__ = func.__signature__[len(params):]
        curried.__constants__ = fun_defaults(funcp)

        curried.curryargs = func.curryargs + list(params)
        curried.parent = func.parent

    return curried


f3 = curry(ftest, 2, 4)  # x = 2, y = 20

f4 = curry(f3, 10)

print("Debug f3")
debug_func(f3)

print("Debug f4")
debug_func(f4)

print("f3(10) = ", f3(10))

print("f4(100) = ", f4(100))
print("f4(100, 30) = ", f4(100, 30))


