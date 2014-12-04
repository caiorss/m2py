#! /usr/bin/env python
#encoding:UTF-8

from control import *
from matplotlib.pyplot import draw , figure , show

G1=zpk([],[0,-1,-5],5)
G2=zpk([],[0,-1,-5],10)


print G1
print G2

FreqResp(G1,0.01,100,200);
FreqResp(G2,0.01,100,200);

printmargin(G1)

printmargin(G2)

bode(G1,1,'b',"G1 k5");
bode(G2,1,'r',"G2 k=10");

m_circles()
nichols(G1,'b')
nichols(G2,'r')
axis([-360,0,-20,40]) 

savefig("bode-chart.png")

draw()
#show()

# Shell interativo para o código
#
#import code; code.interact(local=locals())




