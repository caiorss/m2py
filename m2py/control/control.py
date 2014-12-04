#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from scipy import *
from pylab import *
from matplotlib.pyplot import draw,figure,show




" Função seno com argumento em graus"
def sind(theta_deg):
		return sin(theta_deg*pi/180)
 

" Função coseno com argumento de graus"
def cosd(theta_deg):
		return cos(theta_deg*pi/180)

" Transforma um fasor rho<theta na forma retangular " 
def	r2p(rho,theta_deg):
		z=rho*(cosd(theta_deg)+1j*sind(theta_deg));
		return z

" Extrai a fase de um número complexo em graus"
def phase(z):
	return angle(z)*180/pi

" Extrai o módulo em db e a fase correspondente"
# da função de transferência em certo ponto G(s) , s=sig+jw
def dbphase(G,s):
	z=tfeval(G,s)
	Gab=abs(z)
	Gdb=20*log10(Gab)  # Valor da tf em decibeis
	phase=angle(z)*180/pi
	if phase > 0:
		phase=phase-360
	return [Gab,Gdb,phase]




" Sistema linear invariante no tempo"
"  ==>Linear Time Invariant System<=="
class LTI:
		NUM=array([])
		DEN=array([])
		p=array([]) 
		z=array([])
		L=0
		FRESP=0		# Frequency response

		# Transfer function multiplication
		def __mul__(self,other):

			newtf=self.__class__() # Build a new transfer function

			if isinstance(other,int) or isinstance(other,float):
				newtf.NUM=polymul(other,self.NUM)
				newtf.DEN=self.DEN
				return newtf


			print "Done"		
			newtf.NUM=polymul(self.NUM,other.NUM)
			newtf.DEN=polymul(self.DEN,other.DEN)
			update(newtf)
			return newtf



		# Transfer function addition
 		def __add__(self,other):
			newtf=self.__class__() # Build a new transfer function
		
		
			if isinstance(other,int) or isinstance(other,float):
				newtf.NUM=polyadd(self.NUM,polymul(self.DEN,other))
				newtf.DEN=self.DEN
				return newtf

		
			newtf.NUM=polyadd(polymul(self.NUM,other.DEN),  \
					polymul(other.NUM,self.DEN))
			newtf.DEN=polymul(self.DEN,other.DEN)

			newtf.DEN=polymul(self.DEN,other.DEN)
			return newtf



		def __div__(self,other):
			newtf=self.__class__() # Build a new transfer function
			newtf.NUM=polymul(self.NUM,other.DEN)
			newtf.DEN=polymul(self.DEN,other.NUM)
			return newtf


		def __str__(self):
			return "\n \nNum:%s\tDen:%s\nZeros:%s\tPoles:%s" % \
				(str(self.NUM),str(self.DEN),str(self.z),str(self.p))

		__rmul__=__mul__
		__radd__=__add__


def update(G):
 	G.z=roots(G.NUM)
	G.p=roots(G.DEN)
	L=float(G.NUM[0])/float(G.DEN[0])





" Função de transferência"
def tf(NUM,DEN):
		G=LTI();
		G.NUM=NUM
		G.DEN=DEN
		L=G.NUM[0]
		G.L=L
#		G.z=roots(1/L*NUM)	## Dá erro
		G.z=roots(NUM)
		G.p=roots(DEN)
		sysout(G)
		return G

"Retorna ft em termos de pólos e zeros"
def zpk(ze,po,lead):
		G=LTI()
		G.p=po
		G.z=ze
		G.L=lead
		G.NUM=lead*poly(ze)
		G.DEN=poly(po)
		return G

" Determina o valor da tf em determinado ponto s"
def tfeval(G,s):
		B=polyval(G.DEN,s)
		if size(G.NUM)==1:
				A=G.NUM
		else:
				A=polyval(G.NUM,s)
		return A/B


def sysout(G):
		print "NUM:",G.NUM
		print "DEN:",G.DEN
		print "z;",G.z
		print "p:",G.p
		print "L:",G.L

" Plota root locus da ft de transferência"
def rlocus(G,kmin,kmax,step=0.01):
	kk=arange(kmin,kmax,step)
	x=[]
	y=[]
	clpoles=[]

	fig=figure()
	ax=fig.add_subplot(111)
	
        for k in kk:
			F=polyadd(polymul(k,G.NUM),G.DEN)   
			clrs=roots(F) 
			
			for crr in clrs:
				x=real(crr)
				y=imag(crr)
				clpoles.append(x+1j*y)


        return clpoles






 #       scatter(x,y)

#	ax.plot(real(G.p),imag(G.p),'x')
		#show()



" Computa os pontos de partida e chegada do rootlocis"
#def breakway():

def pzmap(G):
		"Polos de G"
		x1=real(G.p)
		y1=imag(G.p)
		"Zeros de G"
#		x2=real(G.z)
#		y2=imag(G.z)
		scatter(x1,y1,'X')
#		scatter(x2,y2)
		show()


"Gŕaficos de bode"
def FreqResp(G,wmin,wmax,N):

		W=logspace(log10(wmin),log10(wmax),N)		# Frequency vector
		db=[]		# Magnitude-db of F(s) , s=jw
		mag=[]			# Magnitude of TF
		phi=[]                # phi shift of F(s)
		X=[]			# Real part of TF
		Y=[]                    # Imag part of TF
#		print round(wmax)
#		print log10(wmax)
		
		for w in W:
				F=tfeval(G,1j*w)
				mag.append(abs(F))
				db.append(20*log10(abs(F)))
				PHI=phase(F)
				if PHI>0:
					PHI=PHI-360
				phi.append(PHI)
				X.append(real(F))
				Y.append(imag(F))

		w=W
		
#		print w
#		print db
#		print phi
		from scipy.interpolate import interp1d
		db_phi=zip(db,phi,w)
		db_phi.sort()
		db2,phi2,w2=zip(*db_phi)
	#	print db2
	#	print phi2
		dbXphi=interp1d(db2,phi2,kind='linear')
		dbXw=interp1d(db2,w2,kind='linear') 
		pm=dbXphi(0)+180	## phi margin
		wpm=dbXw(0)
#	print wpm
#	print PM
		phi_db=zip(db,phi,w)
		phi_db.sort()
		phi3,db3,w3=zip(*phi_db)
#	print db2
#	print phi2
		phiXdb=interp1d(db3,phi3,kind='linear')
		phiXw=interp1d(db3,w3,kind='linear')

		if  size(G.p)<=2:
			gm=inf
			wgm=inf
		else:
			gm=-1*phiXdb(-180)
			wgm=phiXw(-180)

		wgm=float(wgm)
		wpm=float(wpm)

		G.FRESP={'w':W,'db':db,'phi':phi,'x':X,'y':Y,'mag':mag,'wgm':wgm,'gm':gm,'wpm':wpm,'pm':pm,'phiXdb':phiXdb,'phiXw':phiXw,'dbXphi':dbXphi,'dbXw':dbXw,'wmin':wmin,'wmax':wmax,'N':N};


def margin(G):
	return [G.FRESP['gm'],G.FRESP['pm'],G.FRESP['wgm'],G.FRESP['wpm']];

def printmargin(G):
	[gm,pm,wgm,wpm]=margin(G);
	print "\nPhase margin:%s\nPhase Crossover Frequency:%s\nGain Margin:%s\nGain Crossover Frequency:%s" % \
					(str(pm),str(wpm),str(gm),str(wgm))
					 

def bode(G,fig=None,color='b',name="G"):
	f=figure(fig)


#	print G.FRESP['w']
	af1=f.add_subplot(211)
        semilogx(G.FRESP['w'],G.FRESP['db'],color,label=name)
	ylabel("Mag-dB")
	title("Bode Chart")
	Ymin,Ymax= ylim()
	ylim(Ymin-5,Ymax+5)
	print xticks()
#ylim(Ymax+2,Ymin-2)
	grid(True,which="majorminor",ls="-",color='0.65')
	af2=f.add_subplot(212)
	semilogx(G.FRESP['w'],G.FRESP['phi'],color)
	ylabel("Phase (deg.)")
	xlabel("Freq W (rad/s)")
	Ymin,Ymax= ylim()   
	yticks((-360,-270,-225,-180,-135,-90,-45,0,45,90,135,180,225,270,360))
	ylim(Ymin-5,Ymax+5)
	grid(True,which="majorminor",ls="-",color='0.65')
	 



def feedback(olsys,H=1):
	clsys=olsys/(1+H*olsys)
	return clsys


def serie_block(G,H):
		NUM=polymul(G.NUM,H.NUM)
		DEN=polymul(G.DEN,H.DEN)
		T=systf(NUM,DEN)
		return T

def ufeedback_block(G):
		NUM=G.NUM
		DEN=polyadd(G.NUM,G.DEN)
		T=systf(NUM,DEN)
		return T




def pointp(x,y):
		a=arange(x,x+1,1)
		b=arange(y,y+1,1)
		plot(a,b,'ro',ms=3)




def nyquist(G,wmax,N):
		ww=logspace(-4,log10(wmax),N)
		Gjw=[]   					#Vetor do mapeamento G(jw)=X(w)+kY(w)

		# w: omega de 0 a infinito
		for w in ww:
				GG1=tfeval(G,1j*w)
				print w
				Gjw.append(GG1)		#Acrescenta no fim do array Gjw o valor G(jw) calculado

		# w: omega de 0 a -infinito
		for w in ww:
				GG1=tfeval(G,-1j*w)
				print w
				Gjw.append(GG1)		#Acrescenta no fim do array Gjw o valor G(jw) calculado


#		for kk in Gjw:
#				print kk       #debug

		plot(real(Gjw),imag(Gjw))
		grid()




def nyquistpoints(G,ww):

		for w in ww:
				Q=tfeval(G,1j*w)
				X=real(Q)
				Y=imag(Q)
				annotate("w="+str(1j*w),xy=(X,Y))
				plot(X,Y,'ro',ms=6)					# Plota ponto vermelho 
													#em G(jw) em w=w0


def tfevaldbphi(G,w):
	A=tfeval(G,1j*w)
	db=20*log10(abs(A))
	phi=180/pi*angle(A)
	print A.real
	print A.imag

	if phi>0:
		phi=phi-360
	return [db,phi]



def m_circle1(Mdb):
	from scipy.interpolate import interp1d
	Q=linspace(-360,0,1000)
	QQ=pi/180*Q
	M=pow(10,Mdb/20)
	M2=M*M

	P1=[]
	P2=[]
	Qw1=[]
	Qw2=[]
	for q in QQ:
		si=sin(q)
		cs=cos(q)
		delt=1-si*si*M2
		if delt >=0:
			p1=M*(sqrt(delt)-cs*M)/(M2-1)
			p2=M*(-sqrt(delt)-cs*M)/(M2-1)
			if p1>=0:
				P1.append(p1)
				Qw1.append(q)
			if p2>=0:
				P2.append(p2)
				Qw2.append(q)


	phi1=array(Qw1)
	phi1=phi1*180/pi
	P=array(P1)
	pdb1=20*log10(P1)

#	print phi1
#	print pdb1

######################

	phi2=array(Qw2)
	phi2=phi2*180/pi
	P2=array(P2)
	pdb2=20*log10(P2)


#	print phi2
#	print pdb2

	

	if(Mdb>0):
		f1=interp1d(phi1,pdb1,kind='linear')
		annotate("%s db" % str(Mdb) ,xy=(-180,f1(-180)))
 
 	if(Mdb<=0):
		f1=interp1d(phi2,pdb2,kind='linear')
		annotate("%s db" % str(Mdb) ,xy=(0,f1(0)))
 
	plot(phi1,pdb1,color='0.75')
	plot(phi2,pdb2,color='0.75')
#plot(phi,-pdb)


def m_circles(Mdb=[-12.0,-9.0,-5.0,-4.0,-3,-6.0,-0.8,-0.4,-0.5,-0.3,-0.2,-0.1,1e-4,0.1,0.2,0.4,0.5,1.0,2.0,3.0,4,5,6,9,12]):
	figure()
	hlines(0,-360,0,color='r')
	vlines(-180,-100,100,color='r')
	for mm in Mdb:
		mm=float(mm)
		m_circle1(mm)
	xticks((-360,-300,-240,-180,-120,-60,0))
#	yticks((-100,-80,-60,-40,-20,0,20,40,60,80,100))

def nichols(G,color='r'):
	plot(G.FRESP['phi'],G.FRESP['db'],color)

# FIM DE ROOTLOCUS



def data_nychols(G):
	pt = ginput( show_clicks=True)
	db=pt[0][0]
	phi=pt[0][1]
	f=G.FRESP['dbXw']
	w=f(db)
	print db
	print phi
	print w



def specPO(PO):
	""" Calculates the control system specifications
	    based on a second order system.


	    Input: Percent Overshoot
	    Output: Damping ratio , Phase margin , Cloosed-loop peak-gain
	    Peak-Gain: MPw
	"""
	z=-log(PO/100)/sqrt((pow((PO/100),2)+pi*pi))
	PM=arctan(2*z/sqrt(sqrt(1+4*pow(z,4))-2*pow(z,2)))*180/pi
	MPw=1/(2*z*sqrt(1-z*z))
        
	return [z,PM,MPw]


def charts():
	"""
	  Control Specification charts
	  
	  Bandwith
	  Overshoot
	  Peak-Gain
	  Phase-Margin

	"""
        PO=linspace(0.01,100,200)
	z=-log(PO/100)/sqrt((pow((PO/100),2)+pi*pi))
	PM=arctan(2*z/sqrt(sqrt(1+4*pow(z,4))-2*pow(z,2)))*180/pi
	
	figure()
	plot(z,PO)
	title("Overshoot Chart");
	xlabel("Damping ration \zeta");
	ylabel("Percent Overshoot OS%");
	grid()


 	figure()
	plot(z,PM)
	title("Phase Margin Chart");
	xlabel("Damping ration");
	ylabel("Phase Margin (deg)");
	grid()


	figure()
	z=linspace(0.001,0.707,100);
	MPWdb=20*log10(1/(z*sqrt(1-z*z)))
	plot(z,MPWdb)
 	title("Peak-gain db");
	xlabel("Damping ration");
	ylabel("Peak-gain MPw (db)");
 
	grid()
 



def lead_comp(G,PMd,safety):
	[GM,PM,wcg,wcp]=margin(G)
	phim=PMd-PM+safety			# Needed phase lead to achieve the desired phase margin
	a=(1-sind(phim))/(1+sind(phim))
	m=1/a
	mdb=20*log10(m)
	halfmdb=mdb/2

	wm=G.FRESP['dbXw'](-halfmdb)         # Mean frequency(Max phase lead) calculation
	T=1/(wm*sqrt(a))

	N=G.FRESP['N']
	wmin=G.FRESP['wmin']
	wmax=G.FRESP['wmax']
	
	Gc=tf([T, 1],[a*T , 1]);  		# Lead transfer function                               
	Gw=Gc*G					# Open-loop compensed system

	FreqResp(Gc,wmin,wmax,N)                # Compensator transfer function
	FreqResp(Gw,wmin,wmax,N)                # Compensed system transfer function

	return [a,wm,T,Gc,Gcw]

	









