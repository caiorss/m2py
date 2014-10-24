#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Matlab to Python Code Converter

"""


import re

#print re.sub(r"\[((\S)\s*)+\]", "\[ \2 \]", txt)

function_template = \
"""
def {functioname}({arguments}):
{code}

    return {outputs}
"""


def tralaste_general(text):

    text= text.replace(';', '')      # Remove semicolon end line
    text = text.replace('%', '#')    # Replace commentary symbol

    # Replace multiline comment
    text = text.replace("%}", '"""')
    text = text.replace("%{", '"""')

    # Remove endfunction statement
    text = text.replace("endfunction", "")

    # Translate logic operators
    text = text.replace(r"||", r"or")
    text = text.replace(r"&&", r"and")
    text = text.replace(r"~=", r"!=")



    text = text.replace("(end)", "(-1)")

    # Translate exponential operator
    text = text.replace("^", "**")



    # Missing values; IEEE-754 floating point status flags
    text = re.sub('\bNaN\b', 'nan', text)
    text = re.sub('\bInf\b', 'inf', text)

    text = re.sub('\beps\b', 'spacing(1)', text)

    return text


def translate_lists(text):
    i = re.finditer("(\[(.*?)\])", text)

    for j in i:
       rep = j.group(0)
       rep2 = re.sub(r'(\s+)', r',\1', rep)
       text = re.sub(re.escape(rep), rep2, text)


    text = re.sub('\[,', '[', text)

    return text

def translate_arange(text):
    k = re.compile("\((.*):(.*):(.*)\)'?")
    i = k.finditer(text)

    for j in i:

        rep = j.group(0)
        #print "rep = ", rep
        #print (j.group(1), j.group(2), j.group(3))
        r=j.groups()
        rep2 = "arange(%s, %s, %s)" % (r[0], r[2], r[1])
        text = re.sub(re.escape(rep), rep2, text)

    return text

def translate_builtin_functions(text):

    # disp --->  print
    text = re.sub('disp', 'print', text)
    text = re.sub('puts', 'print', text)
     #  Convert plot(x, [y1, y2, y3] to --->  plotx(x, [y1, y2, y3])
    text = re.sub('\s(plot)(\(\s*.*,\s*\[.*\]\s*\))', r'\nplotx\2', text)
    return text


def translate_function(code):
    """
    Translate the function statement of mfiles:

    {} - Curly brackets indicates optional values:

    File: functioname.m
          --------------

    %  File comment
    %
    function {[returns] =} <functioname> ({arguments})
    <source code>

    """

    text = code

    it = re.finditer(r"function\s+\[(.*)\]\s*=(.*)\((.*)\)", text, re.M)

    # dummy mark to mark expression position
    mark = "xxxxx-----"

    for i in it:
#        print pprint(i.groups())

        rep = i.group(0)
        outputs, functioname, arguments = i.groups()

        text = text.replace(rep, mark)

        # print "rep ", rep
        # print "outputs ", outputs
        # print "functioname ", functioname
        # print "arguments ", arguments


    try:
        header, code = text.split(mark)
    except ValueError:
        return code

    #print "\n\n\n\n"

    #print header

    #print "--------"
    #print code
    code = "\n".join([4*' ' + line for line in code.splitlines()])

    text =function_template.format(functioname=functioname,
                             arguments=arguments,
                             outputs=outputs,
                             code=code)
    text = header + text
    return text


def translate(text):

    # Remove trailing new-line character
    # and whitespace
    text = text.strip()
    text = text.strip('\n')

    text = tralaste_general(text)
    text = translate_arange(text)
    text = translate_lists(text)
    text = translate_builtin_functions(text)
    text = translate_function(text)

    return text


code1 = """

f = prod(1:n);

x = (0:0.2:10)';
y1 = trimf(x, [3 4 5]);
y2 = trimf(x, [2 4 7]);         % some commentary
y3 = trimf(x, [1 4 9]);
subplot(211)
plot(x, [y1 y2 y3]);%some commentary4344
y1 = trimf(x, [2 3 5]);
y2 = trimf(x, [3 4 7]);
y3 = trimf(x, [4 5 9]); % Another commentary
subplot(212)
plot(x, [y1 y2 y3]);
set(gcf, 'name', 'trimf', 'numbertitle', 'off')
"""


code2 = """
%
% this function do something else
%
function [u]=Standard_FLC(V_mu,V_m)
%Part_I :Member-ship Functions
%Creates a new Mamdani-style FIS structure
a=newfis('optipaper');

a=addvar(a,'input','relvelo',[-1.5 1.5]);
a=addmf(a,'input',1,'n','trapmf',[-1.5 -1.5 -1 0]);
a=addmf(a,'input',1,'z','trapmf',[-0.25 -0.05 0.05 0.25]);
a=addmf(a,'input',1,'p','trapmf',[0 1 1.5 1.5]);

a=addvar(a,'input','velo',[-1.5 1.5]);
a=addmf(a,'input',2,'n','trapmf',[-1.5 -1.5 -1 0]);
a=addmf(a,'input',2,'z','trapmf',[-0.25 -0.05 0.05 0.25]);
a=addmf(a,'input',2,'p','trapmf',[0 1 1.5 1.5]);

a=addvar(a,'output','damper rate',[0 10000]);
a=addmf(a,'output',1,'s','trapmf', [0 0 1800 5000]);
a=addmf(a,'output',1,'m','trimf', [2400 5000 7500]);
a=addmf(a,'output',1,'l','trapmf', [5000 10000 15000 15000]);

ruleList=[ 1 1 3 1 1 1 2 2 1 1 1 3 1 1 1 2 1 2 1 1 2 2 2 1 1 2 3 2 1 1 3 1 1 1 1 3 2 2 1 1 3 3 3 1 1 ];
a=addrule(a,ruleList);
FLC_input=[V_mu,V_m];%defining inputs to fuzzy
u=evalfis(FLC_input,a);%evaluating output a.fis
%fuzzy(a)%--- displays the FIS Editor.%
%note it will display FIS editor for %every time step so for 10 sec it will produce 1001 FIS editors.
%mfedit(a)%---- displays the Membership Function Editor.
%ruleedit(a)%--- displays the Rule Editor.
%ruleview(a)%--- displays the Rule Viewer. %surfview(a)%---- displays the Surface View
"""

text = translate(code1)

print text


# for i in it:
#
#     print i.start(1)
#     print i.group(1)
#
#
#     rep = "\b" + i.group(1)
#     rep2 = "lotx"
#     text = re.sub(rep, rep2, text)

#print text

