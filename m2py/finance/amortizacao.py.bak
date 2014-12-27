#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# amortizacao.py
#
# Modulo para calcular amortizacao de emprestimos
# pelos sistemas PRICE, SAC, SAM
#
# Links: http://pessoal.sercomtel.com.br/matematica/financeira/matfin.htm
# http://profinanceira.com.br/biblioteca/sac.aspx
#
# http://www.slideshare.net/DemtrioLuizRigueteGripp/mba-executivo-em-negcios-financeiros
# http://www.gyplan.com/pt/amosink_pt.html
#
from __future__ import division
from tabulate import tabulate


def __cacula_agio(table):
    """
    Calcula o Agio em %

    :param table:
    :return:
    """
    from m2py.misc.vectorize import column

    PV = table[0][-1]
    total = sum(column(table, 1))
    premium = total/PV - 1
    return round(premium, 2)

def show_amort_table(table):
    """
    Imprime tabela de amortizações

    :param table:
    :return:
    """
    from m2py.misc.vectorize import column

    PV = table[0][-1]


    total = sum(column(table, 1))
    juros_total = total - PV
    premium = total/PV - 1



    print(tabulate(table, ['N', 'PAGAMENTO', 'JUROS', 'AMORTIZACAO', 'SALDO DEVEDOR']))

    print "\nTotal de Pagamentos $ %.2f" % total
    print "Total de Juros $ %.2f" % juros_total
    print "Ágio : %s%%" % (100*round(premium, 2))



def amort_juros_final(PV, i, n, show=True):
    """
    Sistema de Amortização com Juros ao Final, Sistema Americano

    :param PV:
    :param i:
    :param n:
    :param show:
    :return:
    """

    # Saldo Devedor Inicial
    SD = PV
    J = PV * i
    P = J
    A = 0

    table = [(0, 0, 0, 0, SD)]

    for k in range(1, n ):
        line = (k, P, J, A, SD)
        table.append(line)

    table.append((n, P + PV, J, A, 0))

    if show:
        show_amort_table(table)


    else:
        return table


def amort_price(PV, i, n, show=True):
    """
    Imprime Demonstrativo de Sistema de amortizações PRICE
    com prestações contantes

    :param PV: Valor Presente/ Valor do Emprestimo
    :param i:  Taxa de Juros decimal
    :param n:  Período de pagamento
    :param show:    Flag/ Se True - Imprime tabela, se False, retorna tabela
    :return:
    """
    # Fator PV/PMT
    x = (1 - 1 / (1 + i) ** n) / i
    # Pagamento/ PMT / Parcela
    P = PV / x

    # Saldo Devedor
    SD = PV

    table = [(0, 0, 0, 0, SD)]

    for k in range(1, n + 1):
        J = i * SD
        A = P - J
        SD = SD - A

        if SD < 1e-3:
            SD = 0
        #SD = round(SD, 2)

        line = (k, P, J, A, SD)
        table.append(line)

    if show:
        show_amort_table(table)
    else:
        return table


def amort_sac(PV, i, n, show=True):
    """
    Imprime Demonstrativo de Sistema de amortizações constante SAC

    :param PV:      Valor Presente/ Valor do Emprestimo
    :param i:       Taxa de Juros decimal
    :param n:       Período de pagamento
    :param show:    Flag/ Se True - Imprime tabela, se False, retorna tabela
    :return:


    Regras
        SD0 = PV

        Sdi = Sdi-1 - Ai
        Ji = i*SDi-1
        Pi = Ai + Ji
    """

    # Saldo Devedor
    SD = PV

    # Amortizacao
    A = PV / n

    # Pagamento/ PMT / Parcela
    P = 0

    table = [(0, 0, 0, 0, SD)]

    for k in range(1, n + 1):
        #print k

        J = i * SD
        SD = SD - A

        P = J + A

        line = (k, P, J, A, SD)
        table.append(line)

    if show:
        show_amort_table(table)
    else:
        return table
        #show_amort_table(table)


def amort_sam(PV, i, n, show=True):
    """
    Imprime Demonstrativo de Sistema de amortizações SAM/ SACRE

    :param PV: Valor Presente/ Valor do Emprestimo
    :param i:  Taxa de Juros decimal
    :param n:  Período de pagamento
    :param show:    Flag/ Se True - Imprime tabela, se False, retorna tabela
    :return:


    Sistema, adotado recentemente no Sistema Financiero da Habitação (S.F.H.),

    O devedor paga o empréstimo em prestações em que cada uma é a média aritmética dos
    valores encontrados para as prestações dos sistemas PRICE e SAC.

    Os juros, as amortizações e os saldos devedores também serão média aritmética.
    """
    SD = PV

    table_price = amort_price(PV, i, n, show=False)
    table_sac = amort_sac(PV, i, n, show=False)

    f = lambda table: map(lambda line: line[1], table)[1:]

    PMT_price = f(table_price)
    PMT_sac = f(table_sac)

    table = [(0, 0, 0, 0, SD)]

    k = 1

    for PMT, P in zip(PMT_price, PMT_sac):

        R = (PMT + P) / 2
        J = i * SD
        A = R - J
        SD = SD - A

        if SD < 1e-2:
            SD = 0

        line = (k, R, J, A, SD)
        table.append(line)
        k += 1

    if show:
        show_amort_table(table)
    else:
        return table


def amort(PV, i, n, type):
    """
    :param PV:   Valor Presente/ Valor do emprestimo
    :param i:    Taxa de Juros
    :param n:    Número de periódos
    :param type: Tipo de amortização

    Possíveis valores para type:
        'price'                 - Sistema Price
        'sac'                   - Sistema SAC
        'final' ou 'americano'  - Juros ao Final
        'sam'/ 'sacre'          - Amortizaçao Sacre/SAM

    :return:
    """
    am = amort.___amort_type___[type]
    am(PV, i, n)


amort.___amort_type___ = {
    'price': amort_price,
    'sac': amort_sac,
    'sam': amort_sam,
    'sacre': amort_sam,
    'final': amort_juros_final,
    'americano': amort_juros_final
}


def juros_price(PV, PMT, n, PV0=0):
    """
    Calcula taxa de juros de um parcelamento pela table price
    Usado comummente em cŕedito concedido ao consumidor

    :param PV:    Valor a Vista / Valor Presente
    :param PV0:   Entrada
    :param PMT:   Valor da Parcela
    :param n:     Número de parcelas
    :return:      Taxa de juros decimal usada no parcelamento
    """
    from m2py.numerical.roots import nraphson
    c = (PV - PV0) / PMT
    f = lambda i: (1 - 1 / (1 + i) ** n) / i - c
    df = lambda i: ((i + 1) ** -n - 1 * n) / i - (1 - 1 / (i + 1) ** n) / i ** 2

    root, _, _ = nraphson(f, df, 2, tol=1e-5, maxit=1000)
    return round(root, 5)

def main():

    PV = 100000.00
    i = 0.1
    n = 4

    print "Um produto tem valor a vista de  R$ 1000.000,00"
    print "foi financiado em 4 parcelas de 31547.1"
    print "econtre a taxa de juros do financiamento em %"
    print ""
    print "Solução :"
    print " >>> print  100*juros_price(100000.00, 31547.1, 4)"
    print  100*juros_price(100000.00, 31547.1, 4)

    print 50*"-"

    print "Emprestimo de R$ 1000.000,00 a 10% a.m 4 meses pelo:"

    print "\nSistema Americano\n"
    #amort_juros_final(PV, i, n)
    amort(PV, i, n, 'final')

    print "\nSistema PRICE - Parcelas Constantes\n"
    #amort_price(PV, i, n)
    amort(PV, i, n, 'price')

    print "\nSistema SAC - Amortizações Constantes\n"
    #amort_sac(PV, i, n)
    amort(PV, i, n, 'sac')

    print "\nSistema SAM/ SACRE\n"
    #amort_sam(PV, i, n)
    amort(PV, i, n, 'sam')


if __name__ == "__main__":
    pass
    main()

