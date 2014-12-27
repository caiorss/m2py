#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == "__main__":


    if len(sys.argv) < 2:
        sys.exit(0)

    if sys.argv[1] == "thermo":

        if sys.argv[2] == "update_gas":
            import m2py.thermo.make_nasa_polynomials
            print("Created nasa polynomials")



    #from . import shell
    #shell.main()

    # import shell
    # shell.main()
