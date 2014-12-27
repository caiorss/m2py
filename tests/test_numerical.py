from math import *

from m2py.numerical.numerical import bissection, RootFindErrror


f = lambda x: exp(-x) -3*log(x)

try:
    root = bissection(f, 0.1, 1)
    print(root)
except RootFindErrror as err:
    pass

print("---------------------")



print("---------------------")

try:
    root = bissection(f, 0.001, 1000, debug=True)
    print(root)
except Exception as err:
    print(err, err.msg)
