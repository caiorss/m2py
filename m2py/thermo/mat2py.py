#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def tralaste_general(text):

    text= text.replace(';', '')      # Remove semicolon end line
    text = text.replace('%', '#')    # Replace commentary symbol

    # Replace multiline comment
    text = text.replace("%}", '"""')
    text = text.replace("%{", '"""')

    # Remove endfunction statement
    text = text.replace("endfunction", "")
    text = text.replace("end", "")

    # Translate logic operators
    text = text.replace(r"||", r"or")
    text = text.replace(r"&&", r"and")
    text = text.replace(r"~=", r"!=")



    text = text.replace("(end)", "(-1)")
    #text = text.replace("end", "")

    # Translate exponential operator
    text = text.replace("^", "**")


    #text = re.sub("end", "", text)
    # Missing values; IEEE-754 floating point status flags
    text = re.sub('\bNaN\b', 'nan', text)
    text = re.sub('\bInf\b', 'inf', text)
    text = re.sub('\beps\b', 'spacing(1)', text)

    return text





txt = open("XSteam.m").read()
txt = txt.replace('\r', '\n')

#txt = re.sub(r"(?s)(.*?)function", r'"""\n\1\n\"""', txt)

txt = tralaste_general(txt)


txt = re.sub(r"function.*=\s*(.*)\)", r"def \1):", txt)

txt = re.sub(r"if(.*).", r"if \1:", txt)
txt = re.sub(r"elseif", r"elif", txt)
txt = re.sub(r"else", r"else:", txt)

forpat = re.compile(r"for\s*(.+)\s*=\s*(\d+)\s*:\s*(\d+)")
txt = forpat.sub(r"for \1 in range(\2, \3):", txt)




arrays  = ['Ji', 'J1', 'Jr', 'ni', 'n1', 'nr', 'Ii', 'I1', 'J0', 'n0']
for v in arrays:
    r1 = v + '(i)'
    r2 = v + '[i]'
    txt = txt.replace(r1, r2)


fp = open("XSteam2.py", 'w').write(txt)

# sed -i -r 's/function\.*=/def/' "$1"
# sed -i 's/endfunction//' "$1"
# sed -i 's/end//' "$1"
#
# #sed -i -r 's/for\si\s*=\s*(\d+)\s*:\s*(\d+)/for i in range(\1, \2):/'  "$1"
#
# sed -i -r 's/;//'          "$1"
# sed -i 's/\\^/**/'        "$1"
# sed -i -r 's/%/#/'         "$1"
#
# sed -i 's/Ji(i)/Ji[i]/g' "$1"
# sed -i 's/J1(i)/J1[i]/g' "$1"
# sed -i 's/Jr(i)/Jr[i]/g' "$1"
#
# sed -i 's/ni(i)/ni[i]/g' "$1"
# sed -i 's/n1(i)/n1[i]/g' "$1"
# sed -i 's/nr(i)/nr[i]/g' "$1"
#
# sed -i 's/Ii(i)/Ii[i]/' "$1"
# sed -i 's/I1(i)/I1[i]/' "$1"
# sed -i 's/J0(i)/J0[i]/' "$1"
# sed -i 's/n0(i)/n0[i]/' "$1"