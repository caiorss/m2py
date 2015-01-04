#!/usr/bin/env python
# -*- coding: utf-8 -*-

txt = """
>>> t = [1, 2, 3, 4, 5]
>>> map(lambda x: x**2, t)
[1, 4, 9, 16, 25]
>>> t
[1, 2, 3, 4, 5]
>>> zip(t,  map(lambda x: x**2, t))
[(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]
>>>
"""


def paste_run():
    global txt

    import re
    from .utils import xclip
    #txt = xclip()
    #txt = txt.strip('\n').strip('\r')

    #print txt

    # Replace bad character
    txt = txt.replace('’', "'")

    # Remove lines non starting with >>>
    lines = [x for x in txt.splitlines() if x.startswith(">>>")]

    # Remove >>> from beginning of lines
    lines = [x.split(">>>")[1].strip() for x in lines]


    #nextxt = "\n".join(lines)
    #exec(nextxt)

    for line in lines:

        print(">>> ", line)

        if not line:
            continue

        if re.match(".*=.*", line):
            exec(line)
        else:
            print(eval(line))

paste_run()