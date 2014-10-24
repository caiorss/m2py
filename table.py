

def interpol(x, X, Y):
    """
    Interpolate over x in X, Y table.
    
    :param x: Input value 
    :param X: input column  ( List of float)
    :param Y: output column
    :return: y = (y2-y1)/(x2-x1)*(x-x1) + y1
    
    In [10]: T[:4], P[:4]
    Out[10]: ([5.0, 10.0, 15.0, 20.0], [0.8721, 1.2276, 1.705, 2.339])
    
    In [11]: interpol(6.45, T, P)
    Out[11]: 0.975195
    """
    
    for idx, xx in enumerate(X):
        if x <= xx:
            break
    
    x2 = xx         
    y2 = Y[idx]
    x1 = X[idx-1] 
    y1 = Y[idx-1]    
    y = (y2-y1)/(x2-x1)*(x-x1) + y1
    
    return y
 
def interpol2(x, X, YY):
    """
    Interpolate x in X, YY tables:
     
    :param x: Input value to be interpolated
    :param X: input column  ( List of float)
    :param YY: output columns vector ( List of List of float)
    :return: y = (y2-y1)/(x2-x1)*(x-x1) + y1 
    
    Example:
    In [6]: interpol2(100.233, T, [P, vf, vg])
    Out[6]: [102.20870000000001, 0.0010441398, 1.6610850359999998]
        
    """
     
    m =  lambda Y: interpol(x, X, Y)
    return map(m, YY)
    
 
def read_csv_table(filename, dtype="float"):
    import csv
    fp = open("saturated_water.csv", "rb")
    
    rows = csv.DictReader(fp)
    table = {}
    
    for row in rows:
        for k, v in row.iteritems():
            try:
                if dtype == "float":
                    _v = float(v)
                
                table[k].append(_v)
            except:
                table[k] = []
    
    return table
   
