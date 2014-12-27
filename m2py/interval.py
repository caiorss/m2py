#!/usr/bin/env python
# -*- coding: utf-8 -*-


def signum(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def step(x):
    """
    Unit Step Function

                 x < 0 --> y = 0
    y = step(x):
                 x > 0 --> y = 1

    :param x:
    :return:
    """

    if x < 0:
        return 0
    return 1


def step_factory(c):
    """
    Return hc(x) such that

                0, if x < c
    hc(x) =     1, if x > c

    :param c:
    :return:   f(x) = step(x-c)
    """
    return lambda x: step(x - c)


def interval(c1, c2):
    def f(x):
        if x < c1:
            return 0
        elif c1 <= x <= c2:
            return 1
        else:
            return 0

    return f


def interval_step(table):
    #intervals, values = zip(*table)

    intervals = list([(x[:2]) for x in table])
    values    = list([x[2] for x in table])

    #print(intervals)

    funcs = [interval(c1, c2) for c1, c2 in intervals]

    def f(x):
        sum = 0

        for fun, value in zip(funcs, values):
            sum += value * fun(x)

        return sum

    return f


inf = 1e90


# (1) Base de cálculo mensal em R$  Alíquota (%)    
# (2) Parcela a deduzir em R$
# 
# 1710.78   -   -       (1)     (2)
# De 1710.79  2563.91   7.5     128.31
# De 2563.92  3418.59   15      320.60
# De 3418.60  4271.59   22.5    577.00
# Acima de 4271.59      27.5    790.58


ir_aliquota = interval_step(
    (
        (1710.79, 2563.91, 7.5),
        (2563.92, 3418.59, 15),
        (3418.60, 4271.59, 22.5),
        (4271.60, inf,     27.5)
    )
)


inss_aliquota = interval_step(
    (
        (0,       1247.70, 8),
        (1247.71, 2079.50, 9),
        (2079.51, 4159.0, 11),
    )
)


# aliquota_ir = interval_step([(1710.79, 2563.91), (2563.92, 3418.59), (3418.60, 4271.59), (4271.60, inf)],
# [7.5, 15.0, 22.5, 27.5])
# 
# desconto_ir = interval_step([(1710.79, 2563.91), (2563.92, 3418.59), (3418.60, 4271.59), (4271.60, inf)],
#                             [128.31, 320.60, 577.00, 790.58])



salario = 3000.0 # R$
numero_dependentes = 2
desconto_por_dependents = 171.97
base = salario

alq_inss= inss_aliquota(salario)
base = (1-alq_inss/100.0)*base - numero_dependentes*desconto_por_dependents

alq_ir = ir_aliquota(base)
imposto_renda = alq_ir/100.0 * base


print(("Aliquota Inss %", alq_inss))
print(("Aliquota IR %", alq_ir))
print(("Base de Calculo R$ ",base))
print(("Imposto de renda R$ ",imposto_renda))


def imposto_ir(basedecalculo):
    pass


# tests = [750.0, 1500.0, 1710.78, 1710.79, 2000.0, 2500.0, 2563.91, 2563.92, 3000.0, 3418.59, 3418.60, 3641.52,
#          4000.0, 4100.0, 4271.59, 4271.60, 4300.0, 5000.0]
#
# results = [(t, ir_aliquota(t)) for t in tests]
#
# from tabulate import tabulate
#
# print(tabulate(results))
