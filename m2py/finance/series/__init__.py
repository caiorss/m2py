#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Financial Time Series Collection similar to R datasets

For while there is only Brazilian financial time series.

"""
import m2py.utils as __utils__
import os as __os__

from m2py.finance.timeserie import plot_against

from . import ipea

__thisdir = __utils__.this_dir()
datadir = datasets_dir = __utils__.resource_path("datasets")
datafiles = __os__.listdir(datadir)
datasets = [d.split(".")[0] for d in datafiles]


def __dataset_path(dataset):
    return __os__.path.join(__os__.path.join(__thisdir, "datasets", dataset))

def metadata(serie):
    filename = serie + ".csv"
    fp = open(filename, 'rb')

    name = fp.readline().split(":")[1].strip()
    dataprovider = fp.readline().split(":")[1].strip()
    url = fp.readline().strip().split(":")[1].strip()
    description = fp.readline().strip().split(":")[1].strip()
    headers = [x.strip() for x in fp.readline().strip().split(",")]
    return dict(name=name, dataprovider=dataprovider, url=url, description=description, headers=headers)


def list_data():
    """
    :return:
    """
    print()


def update_dataset(dataset):
    import sys
    import subprocess as s
    script = __os__.path.join(__thisdir, "update_scripts", "update_" + dataset + ".py")
    p = s.Popen([sys.executable, script])
    p.communicate()


def datalist():

    print("""
    Datasets:

        selic       Selic since 1/7/2000 and VNA ( Updated Notional Value),
                    useful for Brazilian Treasury bonds calculations

        usd2brl     USD to BRL exchange Rate historical values


    """)


def data():
    """
    Similar to the function data from language R.
    it list all builtin-datasets available.

    The builtin datasets are located in:
    /m2py/finance/series/datasets

    :return:
    """
    from tabulate import tabulate
    for dataset in datasets:
        m=  metadata(__dataset_path(dataset))
        
        out= (
            ("Dataset:", dataset ),
            ("Name:", m["name"]),
            ("Description:", m["description"]),
            ("Data Provider:", m["dataprovider"]),
            ("Headers :", m["headers"]),
        )

        print("\n")

        print(tabulate(out, tablefmt="plain"))


def load(dataset):
    """
    Return a timeserie Object

    :return:
    """
    from m2py.finance.timeserie import Tserie
    return Tserie.from_csv(__dataset_path(dataset + ".csv"))


