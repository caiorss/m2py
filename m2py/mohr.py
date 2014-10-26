
def mohr2c(Sx, Sy, txy):
    """
    Computes the Center and 
    Radius of mohr circle
    
    :return: (Center, Radius)
    """
    O  = (Sx+Sy)/2
    dx = abs(Sx-O)
    R = sqrt(dx**2 + txy**2)
    return (O, R)

def mohr2p(Sx, Sy, txy):
    """
    compute mohr principal stress
    """
    O, R = mohr2c(Sx, Sy, txy)
    
    dx = Sx - O
    dy = txy
    theta1 = (180-atan2d(dy, dx))/2
    theta2 = (180-2*theta1)/2
    
    S = O + R, O - R
    S1= max(S)
    S2= min(S)
    
    print dict(S1=S1, S2=S2)
    
    return (S1, theta1), (S2, theta2)


def mohr2plot(Sx, Sy, txy):
    
    t = linspace(0, 2*pi, 100)
    O ,R = mohr2c(Sx, Sy, txy)
    
    x = O + R * cos(t)
    y = R * sin(t)
    
    #plot(x, y)
    plot((Sx,Sy), (txy, -txy))
    plot(x,y)
    grid()
    show()

O, R = mohr2c(-80, 50, 25)

#print dict(O=0, R=R)

#print mohr2p(-80, 50, 25)

#print mohr2p(20,  50, -10)


