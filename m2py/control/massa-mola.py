#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pylab import *
ion()

#	Simulacao da resposta ao degrau um de sistema massa-mola-amortecedor 
#  usando equacoes de espacos de estados
#
#      			         ________
#  amortecedor  b.dx/dt   <-----| M     |------> F
#  mola		 k.x      <-----|_______|
#                                              ---> aceleracao
# 
#	
#	F=m.d2x/dt2+ b.dx/dt +kx
#
#       F=mx'' + bx'+ kx
#
#	x:posição
#       t:tempo
# 	
#	Estados           		Saídas
#	x1=x 	Posição                 y1=x  : Posição
#       x2=x'   Velocidade              y2=x' : Velocidade
#
#	--------------------------------
#          Equacoes de estado
#      x1'=      0x1 +      1x2    + 0
#      x2'= (-k/m)x1 + (-b/m)x2    + F/m
#
#	A=[[0, 1],[-k/m  , -b/m]]
#
#       U=[0,F/m]' (transposta)
#
# 	  Equações de saída
#      [y1]        [x1]
#      [y2]=[1 1]].[x2]
#
#
#	Função de transferência em malha aberta
#
#	X(s)/F(s)=1/(m.s^2 + b.s + k)
#
#-----------------Constantes-------------#
m=1.0 	 # kg       	Massa
k=20.0 	 # N/m      	Constante da mola
b=10    # N/(m/s)      Constante do amortecedor
F=1      # N		Entrada constante degrau unitário



#-------------- Matrizes das equacoes de estado -----------#
# 	X'=Ax+BU
#       Y=Cx

A=[[0.,1.],[-k/m,-b/m]]   # Matriz de estado
B=[0.,1.]
U=F/m		# Matriz de entrada
C=[1.,1.]
x=[0.,0.]                # Condição inicial nula


A=matrix(A)		# Cria objetos matrizes
B=matrix(B) ; B=B.transpose()
C=matrix(C) ; 
x=matrix(x) ;  x=x.transpose()

print "\n\n\n"
print "A\n",A
print "B\n",B
print "C\n",C
print "U\n",U
print "x\n",x

h=0.001 #s  segundos  Intervalo de tempo de amostragem(discretização)
tf=10  #s  segundos  Tempo final da simulação

t=arange(0,tf,h)

# Matrizes para sistema discreto
#
#	x[n+1]=Ad.x[n]+Bd.u[n] 	;;  Ad=(I+hA)
#       y[n]=C.x[n]                 Bd=hB
#

Ad=eye(2)+h*A   
Bd=h*B

xx=[[],[]] 	# Lista com valores de x

for tk in t:
	x=Ad*x+Bd*U
	xx[0].append(x.item(0))
	xx[1].append(x.item(1))


xx[0]=array(xx[0])
xx[1]=array(xx[1])

plot(t,xx[0])
plot(t,xx[1])
show()
from IPython import embed; embed()
