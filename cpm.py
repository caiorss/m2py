#!/usr/bin/env python

from xclip import Xclip
from matlab2py import translate

x = Xclip()
text = x.read() # Read clipboard
code = translate(text)
x.write(code)


