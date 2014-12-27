#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from .__init__ import sys

import os

line_separator = 25*"- "

print(line_separator)
print("\nThermodynamic module\n")
from . import test_thermo


print(line_separator)
print("\nUnit conversion submodule")
from . import test_units