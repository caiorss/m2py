
def XSteam(fun,In1,In2):
#*Contents.
#*1 Calling functions
#*1.1
#*1.2 Temperature (T)
#*1.3 Pressure (p)
#*1.4 Enthalpy (h)
#*1.5 Specif ic Volume (v:
#*1.6 Density (rho)
#*1.7 Specif ic entropy (s:
#*1.8 Specif ic internal energy (u:
#*1.9 Specif ic isobaric heat capacity (Cp:
#*1.10 Specif ic isochoric heat capacity (Cv:
#*1.11 Speed of sound
#*1.12 Viscosity
#*1.13 Prandtl
#*1.14 Kappa
#*1.15 Surface tension
#*1.16 Heat conductivity
#*1.17 Vapour fraction
#*1.18 Vapour Volume Fraction
#
#*2 IAPWS IF 97 Calling functions
#*2.1 Functions for region 1
#*2.2 Functions for region 2
#*2.3 Functions for region 3
#*2.4 Functions for region 4
#*2.5 Functions for region 5
#
#*3 Region Selection
#*3.1 Regions as a function of pT
#*3.2 Regions as a function of ph
#*3.3 Regions as a function of ps
#*3.4 Regions as a function of hs
#
#4 Region Borders
#4.1 Boundary between region 1 and 3.
#4.2 Region 3. pSat_h and pSat_s
#4.3 Region boundary 1to3 and 3to2 as a functions of s
#
#5 Transport properties
#5.1 Viscosity (IAPWS formulation 1985)
#5.2 Thermal Conductivity (IAPWS formulation 1985)
#5.3 Surface Tension
#
#6 Units
#
#7 Verif icatio:
#7.1 Verif iy region :
#7.2 Verif iy region :
#7.3 Verif iy region :
#7.4 Verif iy region :
#7.5 Verif iy region :
#***********************************************************************************************************
#*1 Calling functions                                                                                      *
#***********************************************************************************************************
#***********************************************************************************************************
#*1.1
fun=lower(fun)
switch fun
    #***********************************************************************************************************
    #*1.2 Temperature

    
  

     
    

     
    

    
    #***********************************************************************************************************
    #*1.3 Pressure (p)

    
    
  
    

    
    
    case 'p_hrho'
    h=In1
    rho=In2
#Not valid for water or sumpercritical since water rho does not change very much with p.
#Uses iteration to find p.
  High_Bound = fromSIunit_p(100)
  Low_Bound = fromSIunit_p(0.000611657)
  ps = fromSIunit_p(10)
  rhos = 1 / XSteam('v_ph',ps, h)
  while abs(rho - rhos) > 0.0000001
    rhos = 1 / XSteam('v_ph',ps, h)
    if  rhos >= rh:
      High_Bound = ps
    else:
      Low_Bound = ps
    
    ps = (Low_Bound + High_Bound) / 2
  
    Out = ps
    #***********************************************************************************************************
    #*1.4 Enthalpy (h)
    
 

    
    

    
    

    

    

    
    #***********************************************************************************************************
    #*1.5 Specif ic Volume (v:
case {'vv_p','rhov_p'}
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_v(v2_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_v(v3_ph(p, h4V_p(p)))
        
    else:
        Out = NaN
    
    if  fun(1)=='r':
        Out=1/Out
    
    
    
case {'vl_p','rhol_p'}
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_v(v1_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_v(v3_ph(p, h4L_p(p)))
        
    else:
        Out = NaN
    
    if  fun(1)=='r':
        Out=1/Out
    
    
case {'vv_t','rhov_t'}
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_v(v2_pT(p4_T(T), T))
        else:
            Out = fromSIunit_v(v3_ph(p4_T(T), h4V_p(p4_T(T))))
        
    else:
        Out = NaN
    
    if  fun(1)=='r':
        Out=1/Out
    
    

    
    
case {'v_ps','rho_ps'}
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Out = fromSIunit_v(v1_pT(p, T1_ps(p, s)))
    case 2
        Out = fromSIunit_v(v2_pT(p, T2_ps(p, s)))
    case 3
        Out = fromSIunit_v(v3_ps(p, s))
    case 4
        xs = x4_ps(p, s)
        if  p < 16.529:
            v4v = v2_pT(p, T4_p(p))
            v4L = v1_pT(p, T4_p(p))
        else:
            v4v = v3_ph(p, h4V_p(p))
            v4L = v3_ph(p, h4L_p(p))
        
        Out = fromSIunit_v((xs * v4v + (1 - xs) * v4L))
    case 5
        Ts = T5_ps(p, s)
        Out = fromSIunit_v(v5_pT(p, Ts))
    otherwise
        Out = NaN
    
    if  fun(1)=='r':
        Out=1/Out
    
    
    #***********************************************************************************************************
    #*1.6 Density (rho)
    # Density is calculated as 1/v. Se section 1.5 Volume
    #***********************************************************************************************************
    #*1.7 Specif ic entropy (s:
    
    

    
    
case 'sl_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_s(s1_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_s(s3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
    

    
    
case 'sl_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_s(s1_pT(p4_T(T), T))
        else:
            Out = fromSIunit_s(s3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    

    
    
case 's_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case 1
        T = T1_ph(p, h)
        Out = fromSIunit_s(s1_pT(p, T))
    case 2
        T = T2_ph(p, h)
        Out = fromSIunit_s(s2_pT(p, T))
    case 3
        rhos = 1 / v3_ph(p, h)
        Ts = T3_ph(p, h)
        Out = fromSIunit_s(s3_rhoT(rhos, Ts))
    case 4
        Ts = T4_p(p)
        xs = x4_ph(p, h)
        if  p < 16.529:
            s4v = s2_pT(p, Ts)
            s4L = s1_pT(p, Ts)
        else:
            v4v = v3_ph(p, h4V_p(p))
            s4v = s3_rhoT(1 / v4v, Ts)
            v4L = v3_ph(p, h4L_p(p))
            s4L = s3_rhoT(1 / v4L, Ts)
        
        Out = fromSIunit_s((xs * s4v + (1 - xs) * s4L))
    case 5
        T = T5_ph(p, h)
        Out = fromSIunit_s(s5_pT(p, T))
    otherwise
        Out = NaN
    
    
    
    #***********************************************************************************************************
    #*1.8 Specif ic internal energy (u:

    
case 'ul_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_u(u1_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_u(u3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'uv_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_u(u2_pT(p4_T(T), T))
        else:
            Out = fromSIunit_u(u3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'ul_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_u(u1_pT(p4_T(T), T))
        else:
            Out = fromSIunit_u(u3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    

    
    
case 'u_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case 1
        Ts = T1_ph(p, h)
        Out = fromSIunit_u(u1_pT(p, Ts))
    case 2
        Ts = T2_ph(p, h)
        Out = fromSIunit_u(u2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ph(p, h)
        Ts = T3_ph(p, h)
        Out = fromSIunit_u(u3_rhoT(rhos, Ts))
    case 4
        Ts = T4_p(p)
        xs = x4_ph(p, h)
        if  p < 16.529:
            u4v = u2_pT(p, Ts)
            u4L = u1_pT(p, Ts)
        else:
            v4v = v3_ph(p, h4V_p(p))
            u4v = u3_rhoT(1 / v4v, Ts)
            v4L = v3_ph(p, h4L_p(p))
            u4L = u3_rhoT(1 / v4L, Ts)
        
        Out = fromSIunit_u((xs * u4v + (1 - xs) * u4L))
    case 5
        Ts = T5_ph(p, h)
        Out = fromSIunit_u(u5_pT(p, Ts))
    otherwise
        Out = NaN
    
    

        
        
    
    #***********************************************************************************************************
    #*1.9 Specif ic isobaric heat capacity (Cp:
case 'cpv_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_Cp(Cp2_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'cpl_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_Cp(Cp1_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'cpv_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_Cp(Cp2_pT(p4_T(T), T))
        else:
            Out = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'cpl_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_Cp(Cp1_pT(p4_T(T), T))
        else:
            Out = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'cp_pt'
    p = toSIunit_p(In1)
    T = toSIunit_T(In2)
    Region = region_pT(p, T)
    switch Region
    case 1
        Out = fromSIunit_Cp(Cp1_pT(p, T))
    case 2
        Out = fromSIunit_Cp(Cp2_pT(p, T))
    case 3
        hs = h3_pT(p, T)
        rhos = 1 / v3_ph(p, hs)
        Out = fromSIunit_Cp(Cp3_rhoT(rhos, T))
    case 4
        Out = NaN
    case 5
        Out = fromSIunit_Cp(Cp5_pT(p, T))
    otherwise
        Out = NaN
    
    
case 'cp_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case 1
        Ts = T1_ph(p, h)
        Out = fromSIunit_Cp(Cp1_pT(p, Ts))
    case 2
        Ts = T2_ph(p, h)
        Out = fromSIunit_Cp(Cp2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ph(p, h)
        Ts = T3_ph(p, h)
        Out = fromSIunit_Cp(Cp3_rhoT(rhos, Ts))
    case 4
        Out = NaN
    case 5
        Ts = T5_ph(p, h)
        Out = fromSIunit_Cp(Cp5_pT(p, Ts))
    otherwise
        Out = NaN
    
    
case 'cp_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Ts = T1_ps(p, s)
        Out = fromSIunit_Cp(Cp1_pT(p, Ts))
    case 2
        Ts = T2_ps(p, s)
        Out = fromSIunit_Cp(Cp2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ps(p, s)
        Ts = T3_ps(p, s)
        Out = fromSIunit_Cp(Cp3_rhoT(rhos, Ts))
    case 4
        Out = NaN
    case 5
        Ts = T5_ps(p, s)
        Out = fromSIunit_Cp(Cp5_pT(p, Ts))
    otherwise
        Out = NaN
    
    
    #***********************************************************************************************************
    #*1.10 Specif ic isochoric heat capacity (Cv:
case 'cvv_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_Cv(Cv2_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'cvl_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_Cv(Cv1_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'cvv_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_Cv(Cv2_pT(p4_T(T), T))
        else:
            Out = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'cvl_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_Cv(Cv1_pT(p4_T(T), T))
        else:
            Out = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'cv_pt'
    p = toSIunit_p(In1)
    T = toSIunit_T(In2)
    Region = region_pT(p, T)
    switch Region
    case 1
        Out = fromSIunit_Cv(Cv1_pT(p, T))
    case 2
        Out = fromSIunit_Cv(Cv2_pT(p, T))
    case 3
        hs = h3_pT(p, T)
        rhos = 1 / v3_ph(p, hs)
        Out = fromSIunit_Cv(Cv3_rhoT(rhos, T))
    case 4
        Out = NaN
    case 5
        Out = fromSIunit_Cv(Cv5_pT(p, T))
    otherwise
        Out = NaN
    
    
case 'cv_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case 1
        Ts = T1_ph(p, h)
        Out = fromSIunit_Cv(Cv1_pT(p, Ts))
    case 2
        Ts = T2_ph(p, h)
        Out = fromSIunit_Cv(Cv2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ph(p, h)
        Ts = T3_ph(p, h)
        Out = fromSIunit_Cv(Cv3_rhoT(rhos, Ts))
    case 4
        Out = NaN
    case 5
        Ts = T5_ph(p, h)
        Out = fromSIunit_Cv(Cv5_pT(p, Ts))
    otherwise
        Out = NaN
    
    
    
case 'cv_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Ts = T1_ps(p, s)
        Out = fromSIunit_Cv(Cv1_pT(p, Ts))
    case 2
        Ts = T2_ps(p, s)
        Out = fromSIunit_Cv(Cv2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ps(p, s)
        Ts = T3_ps(p, s)
        Out = fromSIunit_Cv(Cv3_rhoT(rhos, Ts))
    case 4
        Out = NaN  #(xs * CvVp + (1 - xs) * CvLp) / Cv_scale - Cv_offset
    case 5
        Ts = T5_ps(p, s)
        Out = fromSIunit_Cv(Cv5_pT(p, Ts))
    otherwise
        Out = CVErr(xlErrValue)
    
    
    
    #***********************************************************************************************************
    #*1.11 Speed of sound
case 'wv_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_w(w2_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_w(w3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'wl_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_w(w1_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_w(w3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
case 'wv_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_w(w2_pT(p4_T(T), T))
        else:
            Out = fromSIunit_w(w3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'wl_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_w(w1_pT(p4_T(T), T))
        else:
            Out = fromSIunit_w(w3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
        
    else:
        Out = NaN
    
    
case 'w_pt'
    p = toSIunit_p(In1)
    T = toSIunit_T(In2)
    Region = region_pT(p, T)
    switch Region
    case 1
        Out = fromSIunit_w(w1_pT(p, T))
    case 2
        Out = fromSIunit_w(w2_pT(p, T))
    case 3
        hs = h3_pT(p, T)
        rhos = 1 / v3_ph(p, hs)
        Out = fromSIunit_w(w3_rhoT(rhos, T))
    case 4
        Out = NaN
    case 5
        Out = fromSIunit_w(w5_pT(p, T))
    otherwise
        Out = NaN
    
    
    
case 'w_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case 1
        Ts = T1_ph(p, h)
        Out = fromSIunit_w(w1_pT(p, Ts))
    case 2
        Ts = T2_ph(p, h)
        Out = fromSIunit_w(w2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ph(p, h)
        Ts = T3_ph(p, h)
        Out = fromSIunit_w(w3_rhoT(rhos, Ts))
    case 4
        Out = NaN
    case 5
        Ts = T5_ph(p, h)
        Out = fromSIunit_w(w5_pT(p, Ts))
    otherwise
        Out = NaN
    
    
case 'w_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Ts = T1_ps(p, s)
        Out = fromSIunit_w(w1_pT(p, Ts))
    case 2
        Ts = T2_ps(p, s)
        Out = fromSIunit_w(w2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ps(p, s)
        Ts = T3_ps(p, s)
        Out = fromSIunit_w(w3_rhoT(rhos, Ts))
    case 4
        Out = NaN #(xs * wVp + (1 - xs) * wLp) / w_scale - w_offset
    case 5
        Ts = T5_ps(p, s)
        Out = fromSIunit_w(w5_pT(p, Ts))
    otherwise
        Out = NaN
    
    #***********************************************************************************************************
    #*1.12 Viscosity
case 'my_pt'
    p = toSIunit_p(In1)
    T = toSIunit_T(In2)
    Region = region_pT(p, T)
    switch Region
    case 4
        Out = NaN
    case {1, 2, 3, 5}
        Out = fromSIunit_my(my_AllRegions_pT(p, T))
    otherwise
        Out = NaN
    
    
case {'my_ph'}
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case {1, 2, 3, 5}
        Out = fromSIunit_my(my_AllRegions_ph(p, h))
    case {4}
        Out = NaN  
    otherwise
        Out = NaN
    
    
case 'my_ps'
    h = XSteam('h_ps',In1, In2)
    Out = XSteam('my_ph',In1, h)
    
    #***********************************************************************************************************
    #*1.13 Prandtl
    case 'pr_pt'
  Cp = toSIunit_Cp(XSteam('Cp_pT',In1, In2))
  my = toSIunit_my(XSteam('my_pT',In1,In2))
  tc = toSIunit_tc(XSteam('tc_pT',In1,In2))
  Out = Cp * 1000 * my / tc
    case 'pr_ph'
  Cp = toSIunit_Cp(XSteam('Cp_ph',In1, In2))
  my = toSIunit_my(XSteam('my_ph',In1,In2))
  tc = toSIunit_tc(XSteam('tc_ph',In1,In2))
  Out = Cp * 1000 * my / tc
    #***********************************************************************************************************
    #*1.14 Kappa
    #***********************************************************************************************************
    #***********************************************************************************************************
    #*1.15 Surface tension
case 'st_t'
    T = toSIunit_T(In1)
    Out = fromSIunit_st(Surface_Tension_T(T))
    
case 'st_p'
    T = XSteam('Tsat_p',In1)
    T = toSIunit_T(T)
    Out = fromSIunit_st(Surface_Tension_T(T))
    
    #***********************************************************************************************************

    
    
case 'tcv_p'
    ps = In1
    T = XSteam('Tsat_p',ps)
    v = XSteam('vV_p',ps)
    p = toSIunit_p(In1)
    T = toSIunit_T(T)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    
case 'tcl_t'
    Ts = In1
    p = XSteam('psat_T',Ts)
    v = XSteam('vL_T',Ts)
    p = toSIunit_p(p)
    T = toSIunit_T(Ts)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    
case 'tcv_t'
    Ts = In1
    p = XSteam('psat_T',Ts)
    v = XSteam('vV_T',Ts)
    p = toSIunit_p(p)
    T = toSIunit_T(Ts)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    
case 'tc_pt'
    Ts = In2
    ps = In1
    v = XSteam('v_pT',ps, Ts)
    p = toSIunit_p(ps)
    T = toSIunit_T(Ts)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    
case 'tc_ph'
    hs = In2
    ps = In1
    v = XSteam('v_ph',ps, hs)
    T = XSteam('T_ph',ps, hs)
    p = toSIunit_p(ps)
    T = toSIunit_T(T)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    
case 'tc_hs'
    hs = In1
    p = XSteam('p_hs',hs, In2)
    ps = p
    v = XSteam('v_ph',ps, hs)
    T = XSteam('T_ph',ps, hs)
    p = toSIunit_p(p)
    T = toSIunit_T(T)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    #***********************************************************************************************************
    #*1.17 Vapour fraction
    

    

    
    
    #***********************************************************************************************************
    #*1.18 Vapour Volume Fraction


    

    
 
 case 'check'
   err=check()
    
otherwise
    error(['Unknown calling function to XSteam, ',fun, ' See help XSteam for valid calling functions'])
#***********************************************************************************************************
#*2.2 functions for region 2

def w2_pT(p, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#6 Equations for Region 2, Section. 6.1 Basic Equation
#Table 11 and 12, Page 14 and 15
J0 = [0, 1, -5, -4, -3, -2, -1, 2, 3]
n0 = [-9.6927686500217, 10.086655968018, -0.005608791128302, 0.071452738081455, -0.40710498223928, 1.4240819171444, -4.383951131945, -0.28408632460772, 0.021268463753307]
Ir = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 10, 10, 10, 16, 16, 18, 20, 20, 20, 21, 22, 23, 24, 24, 24]
Jr = [0, 1, 2, 3, 6, 1, 2, 4, 7, 36, 0, 1, 3, 6, 35, 1, 2, 3, 7, 3, 16, 35, 0, 11, 25, 8, 36, 13, 4, 10, 14, 29, 50, 57, 20, 35, 48, 21, 53, 39, 26, 40, 58]
nr = [-1.7731742473213E-03, -0.017834862292358, -0.045996013696365, -0.057581259083432, -0.05032527872793, -3.3032641670203E-05, -1.8948987516315E-04, -3.9392777243355E-03, -0.043797295650573, -2.6674547914087E-05, 2.0481737692309E-08, 4.3870667284435E-07, -3.227767723857E-05, -1.5033924542148E-03, -0.040668253562649, -7.8847309559367E-10, 1.2790717852285E-08, 4.8225372718507E-07, 2.2922076337661E-06, -1.6714766451061E-11, -2.1171472321355E-03, -23.895741934104, -5.905956432427E-18, -1.2621808899101E-06, -0.038946842435739, 1.1256211360459E-11, -8.2311340897998, 1.9809712802088E-08, 1.0406965210174E-19, -1.0234747095929E-13, -1.0018179379511E-09, -8.0882908646985E-11, 0.10693031879409, -0.33662250574171, 8.9185845355421E-25, 3.0629316876232E-13, -4.2002467698208E-06, -5.9056029685639E-26, 3.7826947613457E-06, -1.2768608934681E-15, 7.3087610595061E-29, 5.5414715350778E-17, -9.436970724121E-07]
R = 0.461526 #kJ/(kg K)
Pi = p
tau = 540 / T
g0_tautau = 0
for i  in range(1, 9):
    g0_tautau = g0_tautau + n0[i] * J0[i] * (J0[i] - 1) * tau ** (J0[i] - 2)
gr_pi = 0
gr_pitau = 0
gr_pipi = 0
gr_tautau = 0
for i  in range(1, 43):
    gr_pi = gr_pi + nr[i] * Ir[i] * Pi ** (Ir[i] - 1) * (tau - 0.5) ** Jr[i]
    gr_pipi = gr_pipi + nr[i] * Ir[i] * (Ir[i] - 1) * Pi ** (Ir[i] - 2) * (tau - 0.5) ** Jr[i]
    gr_pitau = gr_pitau + nr[i] * Ir[i] * Pi ** (Ir[i] - 1) * Jr[i] * (tau - 0.5) ** (Jr[i] - 1)
    gr_tautau = gr_tautau + nr[i] * Pi ** Ir[i] * Jr[i] * (Jr[i] - 1) * (tau - 0.5) ** (Jr[i] - 2)
w2_pT = (1000 * R * T * (1 + 2 * Pi * gr_pi + Pi ** 2 * gr_pi ** 2) / ((1 - Pi ** 2 * gr_pipi) + (1 + Pi * gr_pi - tau * Pi * gr_pitau) ** 2 / (tau ** 2 * (g0_tautau + gr_tautau)))) ** 0.5
#***********************************************************************************************************
#*2.3 functions for region 3









def Cp3_rhoT(rho, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Table 30 and 31, Page 30 and 31
Ii = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11]
Ji = [0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26]
ni = [1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05]
R = 0.461526 #kJ/(KgK)
tc = 647.096 #K
pc = 22.064 #MPa
rhoc = 322 #kg/m3
delta = rho / rhoc
tau = tc / T
fitautau = 0
fidelta = 0
fideltatau = 0
fideltadelta = 0
for i  in range(2, 40):
    fitautau = fitautau + ni[i] * delta ** Ii[i] * Ji[i] * (Ji[i] - 1) * tau ** (Ji[i] - 2)
    fidelta = fidelta + ni[i] * Ii[i] * delta ** (Ii[i] - 1) * tau ** Ji[i]
    fideltatau = fideltatau + ni[i] * Ii[i] * delta ** (Ii[i] - 1) * Ji[i] * tau ** (Ji[i] - 1)
    fideltadelta = fideltadelta + ni[i] * Ii[i] * (Ii[i] - 1) * delta ** (Ii[i] - 2) * tau ** Ji[i]
fidelta = fidelta + ni(1) / delta
fideltadelta = fideltadelta - ni(1) / (delta ** 2)
Cp3_rhoT = R * (-tau ** 2 * fitautau + (delta * fidelta - delta * tau * fideltatau) ** 2 / (2 * delta * fidelta + delta ** 2 * fideltadelta))

def Cv3_rhoT(rho, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Table 30 and 31, Page 30 and 31
Ii = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11]
Ji = [0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26]
ni = [1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05]
R = 0.461526 #kJ/(KgK)
tc = 647.096 #K
pc = 22.064 #MPa
rhoc = 322 #kg/m3
delta = rho / rhoc
tau = tc / T
fitautau = 0
for i  in range(1, 40):
    fitautau = fitautau + ni[i] * delta ** Ii[i] * Ji[i] * (Ji[i] - 1) * tau ** (Ji[i] - 2)
Cv3_rhoT = R * -(tau * tau * fitautau)

def w3_rhoT(rho, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Table 30 and 31, Page 30 and 31
Ii = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11]
Ji = [0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26]
ni = [1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05]
R = 0.461526 #kJ/(KgK)
tc = 647.096 #K
pc = 22.064 #MPa
rhoc = 322 #kg/m3
delta = rho / rhoc
tau = tc / T
fitautau = 0
fidelta = 0
fideltatau = 0
fideltadelta = 0
for i  in range(2, 40):
    fitautau = fitautau + ni[i] * delta ** Ii[i] * Ji[i] * (Ji[i] - 1) * tau ** (Ji[i] - 2)
    fidelta = fidelta + ni[i] * Ii[i] * delta ** (Ii[i] - 1) * tau ** Ji[i]
    fideltatau = fideltatau + ni[i] * Ii[i] * delta ** (Ii[i] - 1) * Ji[i] * tau ** (Ji[i] - 1)
    fideltadelta = fideltadelta + ni[i] * Ii[i] * (Ii[i] - 1) * delta ** (Ii[i] - 2) * tau ** Ji[i]
fidelta = fidelta + ni(1) / delta
fideltadelta = fideltadelta - ni(1) / (delta ** 2)
w3_rhoT = (1000 * R * T * (2 * delta * fidelta + delta ** 2 * fideltadelta - (delta * fidelta - delta * tau * fideltatau) ** 2 / (tau ** 2 * fitautau))) ** 0.5







 
    

def Cp5_pT(p, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Basic Equation for Region 5
#Eq 32,33, Page 36, Tables 37-41
Ji0 = [0, 1, -3, -2, -1, 2]
ni0 = [-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917]
Iir = [1, 1, 1, 2, 3]
Jir = [0, 1, 3, 9, 3]
nir = [-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07]
R = 0.461526 #kJ/(kg K)
tau = 1000 / T
Pi = p
gamma0_tautau = 0
for i  in range(1, 6):
    gamma0_tautau = gamma0_tautau + ni0[i] * Ji0[i] * (Ji0[i] - 1) * tau ** (Ji0[i] - 2)
gammar_tautau = 0
for i  in range(1, 5):
    gammar_tautau = gammar_tautau + nIr[i] * Pi ** IIr[i] * JIr[i] * (JIr[i] - 1) * tau ** (JIr[i] - 2)
Cp5_pT = -R * tau ** 2 * (gamma0_tautau + gammar_tautau)



def Cv5_pT(p, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Basic Equation for Region 5
#Eq 32,33, Page 36, Tables 37-41
Ji0 = [0, 1, -3, -2, -1, 2]
ni0 = [-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917]
Iir = [1, 1, 1, 2, 3]
Jir = [0, 1, 3, 9, 3]
nir = [-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07]
R = 0.461526 #kJ/(kg K)
tau = 1000 / T
Pi = p
gamma0_tautau = 0

for i  in range(1, 6):
    gamma0_tautau = gamma0_tautau + ni0[i] * (Ji0[i] - 1) * Ji0[i] * tau ** (Ji0[i] - 2)

gammar_pi = 0
gammar_pitau = 0
gammar_pipi = 0
gammar_tautau = 0

for i  in range(1, 5):
    gammar_pi = gammar_pi + nIr[i] * IIr[i] * Pi ** (IIr[i] - 1) * tau ** JIr[i]
    gammar_pitau = gammar_pitau + nIr[i] * IIr[i] * Pi ** (IIr[i] - 1) * JIr[i] * tau ** (JIr[i] - 1)
    gammar_pipi = gammar_pipi + nIr[i] * IIr[i] * (IIr[i] - 1) * Pi ** (IIr[i] - 2) * tau ** JIr[i]
    gammar_tautau = gammar_tautau + nIr[i] * Pi ** IIr[i] * JIr[i] * (JIr[i] - 1) * tau ** (JIr[i] - 2)
Cv5_pT = R * (-(tau ** 2 *(gamma0_tautau + gammar_tautau)) - (1 + Pi * gammar_pi - tau * Pi * gammar_pitau)**2 / (1 - Pi ** 2 * gammar_pipi))



def w5_pT(p, T):
#Release on the IAPWS Industrial formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Basic Equation for Region 5
#Eq 32,33, Page 36, Tables 37-41
Ji0 = [0, 1, -3, -2, -1, 2]
ni0 = [-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917]
Iir = [1, 1, 1, 2, 3]
Jir = [0, 1, 3, 9, 3]
nir = [-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07]
R = 0.461526 #kJ/(kg K)
tau = 1000 / T
Pi = p
gamma0_tautau = 0
for i  in range(1, 6):
    gamma0_tautau = gamma0_tautau + ni0[i] * (Ji0[i] - 1) * Ji0[i] * tau ** (Ji0[i] - 2)
gammar_pi = 0
gammar_pitau = 0
gammar_pipi = 0
gammar_tautau = 0
for i  in range(1, 5):
    gammar_pi = gammar_pi + nIr[i] * IIr[i] * Pi ** (IIr[i] - 1) * tau ** JIr[i]
    gammar_pitau = gammar_pitau + nIr[i] * IIr[i] * Pi ** (IIr[i] - 1) * JIr[i] * tau ** (JIr[i] - 1)
    gammar_pipi = gammar_pipi + nIr[i] * IIr[i] * (IIr[i] - 1) * Pi ** (IIr[i] - 2) * tau ** JIr[i]
    gammar_tautau = gammar_tautau + nIr[i] * Pi ** IIr[i] * JIr[i] * (JIr[i] - 1) * tau ** (JIr[i] - 2)
w5_pT = (1000 * R * T * (1 + 2 * Pi * gammar_pi + Pi ** 2 * gammar_pi ** 2) / ((1 - Pi ** 2 * gammar_pipi) + (1 + Pi * gammar_pi - tau * Pi * gammar_pitau) ** 2 / (tau ** 2 * (gamma0_tautau + gammar_tautau)))) ** 0.5






#***********************************************************************************************************
#*3 Region Selection
#***********************************************************************************************************
#*3.1 Regions as a function of pT






#***********************************************************************************************************
#*3.3 Regions as a function of ps



#***********************************************************************************************************
#*3.4 Regions as a function of hs






#***********************************************************************************************************
#*5 Transport properties
#***********************************************************************************************************
#*5.1 Viscosity (IAPWS formulation 1985, Revised 2003)
#***********************************************************************************************************

def my_AllRegions_pT(  p,   T):
h0 = [0.5132047, 0.3205656, 0, 0, -0.7782567, 0.1885447]
h1 = [0.2151778, 0.7317883, 1.241044, 1.476783, 0, 0]
h2 = [-0.2818107, -1.070786, -1.263184, 0, 0, 0]
h3 = [0.1778064, 0.460504, 0.2340379, -0.4924179, 0, 0]
h4 = [-0.0417661, 0, 0, 0.1600435, 0, 0]
h5 = [0, -0.01578386, 0, 0, 0, 0]
h6 = [0, 0, 0, -0.003629481, 0, 0]
#Calcualte density.
switch region_pT(p, T)
case 1
    rho = 1 / v1_pT(p, T)
case 2
    rho = 1 / v2_pT(p, T)
case 3
    hs = h3_pT(p, T)
    rho = 1 / v3_ph(p, hs)
case 4
    rho = NaN
case 5
    rho = 1 / v5_pT(p, T)
otherwise
    my_AllRegions_pT = NaN
    return
rhos = rho / 317.763
Ts = T / 647.226
ps = p / 22.115
#Check valid area
if  T > 900 + 273.15 or (T > 600 + 273.15  and p > 300) or (T > 150 + 273.15  and p > 350) or p > 500:
    my_AllRegions_pT = NaN
    return
my0 = Ts ** 0.5 / (1 + 0.978197 / Ts + 0.579829 / (Ts ** 2) - 0.202354 / (Ts ** 3))
Sum = 0
for i  in range(0, 5):
    Sum = Sum + h0(i+1) * (1 / Ts - 1) ** i + h1(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 1 + h2(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 2 + h3(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 3 + h4(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 4 + h5(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 5 + h6(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 6
my1 = exp(rhos * Sum)
mys = my0 * my1
my_AllRegions_pT = mys * 0.000055071

def my_AllRegions_ph(  p,   h):
h0 = [0.5132047, 0.3205656, 0, 0, -0.7782567, 0.1885447]
h1 = [0.2151778, 0.7317883, 1.241044, 1.476783, 0, 0]
h2 = [-0.2818107, -1.070786, -1.263184, 0, 0, 0]
h3 = [0.1778064, 0.460504, 0.2340379, -0.4924179, 0, 0]
h4 = [-0.0417661, 0, 0, 0.1600435, 0, 0]
h5 = [0, -0.01578386, 0, 0, 0, 0]
h6 = [0, 0, 0, -0.003629481, 0, 0]
#Calcualte density.
switch region_ph(p, h)
case 1
    Ts = T1_ph(p, h)
    T = Ts
    rho = 1 / v1_pT(p, Ts)
case 2
    Ts = T2_ph(p, h)
    T = Ts
    rho = 1 / v2_pT(p, Ts)
case 3
    rho = 1 / v3_ph(p, h)
    T = T3_ph(p, h)
case 4
    xs = x4_ph(p, h)
    if  p < 16.529:
        v4v = v2_pT(p, T4_p(p))
        v4L = v1_pT(p, T4_p(p))
    else:
        v4v = v3_ph(p, h4V_p(p))
        v4L = v3_ph(p, h4L_p(p))
    
    rho = 1 / (xs * v4v + (1 - xs) * v4L)
    T = T4_p(p)
case 5
    Ts = T5_ph(p, h)
    T = Ts
    rho = 1 / v5_pT(p, Ts)
otherwise
    my_AllRegions_ph = NaN
    return
rhos = rho / 317.763
Ts = T / 647.226
ps = p / 22.115
#Check valid area
if  T > 900 + 273.15 or (T > 600 + 273.15  and p > 300) or (T > 150 + 273.15  and p > 350) or p > 500:
    my_AllRegions_ph = NaN
    return
my0 = Ts ** 0.5 / (1 + 0.978197 / Ts + 0.579829 / (Ts ** 2) - 0.202354 / (Ts ** 3))
Sum = 0
for i  in range(0, 5):
    Sum = Sum + h0(i+1) * (1 / Ts - 1) ** i + h1(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 1 + h2(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 2 + h3(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 3 + h4(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 4 + h5(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 5 + h6(i+1) * (1 / Ts - 1) ** i * (rhos - 1) ** 6
my1 = exp(rhos * Sum)
mys = my0 * my1
my_AllRegions_ph = mys * 0.000055071

#***********************************************************************************************************
#*5.2 Thermal Conductivity (IAPWS formulation 1985)

def tc_ptrho(  p,   T,   rho):
#Revised release on the IAPWS formulation 1985 for the Thermal Conductivity of ordinary water
#IAPWS September 1998
#Page 8
#ver2.6 Start corrected bug
 if  T < 273.1:
   tc_ptrho = NaN #Out of range of validity (para. B4)
   return
 elif  T < 500 + 273.1:
   if  p > 10:
     tc_ptrho = NaN #Out of range of validity (para. B4)
     return
   
 elif  T <= 650 + 273.1:
   if  p > 7:
     tc_ptrho = NaN #Out of range of validity (para. B4)
     return
   
 else: T <= 800 + 273.15
   if  p > 4:
      tc_ptrho = NaN #Out of range of validity (para. B4)
      return
   
 
#ver2.6 End corrected bug
T = T / 647.26
rho = rho / 317.7
tc0 = T ** 0.5 * (0.0102811 + 0.0299621 * T + 0.0156146 * T ** 2 - 0.00422464 * T ** 3)
tc1 = -0.39707 + 0.400302 * rho + 1.06 * exp(-0.171587 * (rho + 2.39219) ** 2)
dT = abs(T - 1) + 0.00308976
Q = 2 + 0.0822994 / dT ** (3 / 5)
if  T >= 1:
    s = 1 / dT
else:
    s = 10.0932 / dT ** (3 / 5)
tc2 = (0.0701309 / T ** 10 + 0.011852) * rho ** (9 / 5) * exp(0.642857 * (1 - rho ** (14 / 5))) + 0.00169937 * s * rho ** Q * exp((Q / (1 + Q)) * (1 - rho ** (1 + Q))) - 1.02 * exp(-4.11717 * T ** (3 / 2) - 6.17937 / rho ** 5)
tc_ptrho = tc0 + tc1 + tc2
#***********************************************************************************************************
#5.3 Surface Tension

def Surface_Tension_T(  T):
#IAPWS Release on Surface Tension of Ordinary Water Substance,
#September 1994
tc = 647.096 #K
B = 0.2358    #N/m
bb = -0.625
my = 1.256
if  T < 0.01 or T > tc:
    Surface_Tension_T = NaN #"Out of valid region"
    return
tau = 1 - T / tc
Surface_Tension_T = B * tau ** my * (1 + bb * tau)

