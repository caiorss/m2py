
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

    
  
case 't_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    Region = region_ph(p, h)
    switch Region
    case 1
        Out = fromSIunit_T(T1_ph(p, h))
    case 2
        Out = fromSIunit_T(T2_ph(p, h))
    case 3
        Out = fromSIunit_T(T3_ph(p, h))
    case 4
        Out = fromSIunit_T(T4_p(p))
    case 5
        Out = fromSIunit_T(T5_ph(p, h))
    otherwise
        Out = NaN
    
case 't_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Out = fromSIunit_T(T1_ps(p, s))
    case 2
        Out = fromSIunit_T(T2_ps(p, s))
    case 3
        Out = fromSIunit_T(T3_ps(p, s))
    case 4
        Out = fromSIunit_T(T4_p(p))
    case 5
        Out = fromSIunit_T(T5_ps(p, s))
    otherwise
        Out = NaN
     
    
case 't_hs'
    h = toSIunit_h(In1)
    s = toSIunit_s(In2)
    Region = region_hs(h, s)
    switch Region
    case 1
        p1 = p1_hs(h, s)
        Out = fromSIunit_T(T1_ph(p1, h))
    case 2
        p2 = p2_hs(h, s)
        Out = fromSIunit_T(T2_ph(p2, h))
    case 3
        p3 = p3_hs(h, s)
        Out = fromSIunit_T(T3_ph(p3, h))
    case 4
        Out = fromSIunit_T(T4_hs(h, s))
    case 5
        error('functions of hs is not avlaible in region 5')
    otherwise
        Out = NaN
    
    #***********************************************************************************************************
    #*1.3 Pressure (p)

    
    
  
    
case 'p_hs'
    h = toSIunit_h(In1)
    s = toSIunit_s(In2)
    Region = region_hs(h, s)
    switch Region
    case 1
        Out = fromSIunit_p(p1_hs(h, s))
    case 2
        Out = fromSIunit_p(p2_hs(h, s))
    case 3
        Out = fromSIunit_p(p3_hs(h, s))
    case 4
        tSat = T4_hs(h, s)
        Out = fromSIunit_p(p4_T(tSat))
    case 5
        error('functions of hs is not avlaible in region 5')
    otherwise
        Out = NaN
    
    
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
case 'hv_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657 and p < 22.06395:
        Out = fromSIunit_h(h4V_p(p))
    else:
        Out = NaN
    
    
case 'hl_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657 and p < 22.06395:
        Out = fromSIunit_h(h4L_p(p))
    else:
        Out = NaN
    
    

    
    
case 'hl_t'
    T = toSIunit_T(In1)
    if  T > 273.15 and T < 647.096:
        p = p4_T(T)
        Out = fromSIunit_h(h4L_p(p))
    else:
        Out = NaN
    
    
    

    
    
case 'h_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Out = fromSIunit_h(h1_pT(p, T1_ps(p, s)))
    case 2
        Out = fromSIunit_h(h2_pT(p, T2_ps(p, s)))
    case 3
        Out = fromSIunit_h(h3_rhoT(1 / v3_ps(p, s), T3_ps(p, s)))
    case 4
        xs = x4_ps(p, s)
        Out = fromSIunit_h(xs * h4V_p(p) + (1 - xs) * h4L_p(p))
    case 5
        Out = fromSIunit_h(h5_pT(p, T5_ps(p, s)))
    otherwise
        Out = NaN
    
    

    
case 'h_prho'
    p = toSIunit_p(In1)
    rho = 1 / toSIunit_v(1 / In2)
    Region = Region_prho(p, rho)
    switch Region
        case 1
            Out = fromSIunit_h(h1_pT(p, T1_prho(p, rho)))
        case 2
            Out = fromSIunit_h(h2_pT(p, T2_prho(p, rho)))
        case 3
            Out = fromSIunit_h(h3_rhoT(rho, T3_prho(p, rho)))
        case 4
            if  p < 16.52:
                vV = v2_pT(p, T4_p(p))
                vL = v1_pT(p, T4_p(p))
            else:
                vV = v3_ph(p, h4V_p(p))
                vL = v3_ph(p, h4L_p(p))
            
            hV = h4V_p(p)
            hL = h4L_p(p)
            x = (1 / rho - vL) / (vV - vL)
            Out = fromSIunit_h((1 - x) * hL + x * hV)
        case 5
            Out = fromSIunit_h(h5_pT(p, T5_prho(p, rho)))
        otherwise
            Out = NaN
    

    
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
    
    
    
case 'sv_t'
    T = toSIunit_T(In1)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = fromSIunit_s(s2_pT(p4_T(T), T))
        else:
            Out = fromSIunit_s(s3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
        
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
case 'uv_p'
    p = toSIunit_p(In1)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_u(u2_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_u(u3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
        
    else:
        Out = NaN
    
    
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
    
    
case 'u_pt'
    p = toSIunit_p(In1)
    T = toSIunit_T(In2)
    Region = region_pT(p, T)
    switch Region
    case 1
        Out = fromSIunit_u(u1_pT(p, T))
    case 2
        Out = fromSIunit_u(u2_pT(p, T))
    case 3
        hs = h3_pT(p, T)
        rhos = 1 / v3_ph(p, hs)
        Out = fromSIunit_u(u3_rhoT(rhos, T))
    case 4
        Out = NaN
    case 5
        Out = fromSIunit_u(u5_pT(p, T))
    otherwise
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
    
    
case 'u_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    Region = region_ps(p, s)
    switch Region
    case 1
        Ts = T1_ps(p, s)
        Out = fromSIunit_u(u1_pT(p, Ts))
    case 2
        Ts = T2_ps(p, s)
        Out = fromSIunit_u(u2_pT(p, Ts))
    case 3
        rhos = 1 / v3_ps(p, s)
        Ts = T3_ps(p, s)
        Out = fromSIunit_u(u3_rhoT(rhos, Ts))
    case 4
        if  p < 16.529:
            uLp = u1_pT(p, T4_p(p))
            uVp = u2_pT(p, T4_p(p))
        else:
            uLp = u3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p))
            uVp = u3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p))
        
        xs = x4_ps(p, s)
        Out = fromSIunit_u((xs * uVp + (1 - xs) * uLp))
    case 5
        Ts = T5_ps(p, s)
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
    #*1.16 Thermal conductivity
case 'tcl_p'
    T = XSteam('Tsat_p',In1)
    v = XSteam('vL_p',In1)
    p = toSIunit_p(In1)
    T = toSIunit_T(T)
    v = toSIunit_v(v)
    rho = 1 / v
    Out = fromSIunit_tc(tc_ptrho(p, T, rho))
    
    
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
    

    
case 'x_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    if  p > 0.000611657  and p < 22.06395:
        Out = fromSIunit_x(x4_ps(p, s))
    else:
        Out = NaN
    
    
    #***********************************************************************************************************
    #*1.18 Vapour Volume Fraction
case 'vx_ph'
    p = toSIunit_p(In1)
    h = toSIunit_h(In2)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            vL = v1_pT(p, T4_p(p))
            vV = v2_pT(p, T4_p(p))
        else:
            vL = v3_ph(p, h4L_p(p))
            vV = v3_ph(p, h4V_p(p))
        
        xs = x4_ph(p, h)
        Out = fromSIunit_vx((xs * vV / (xs * vV + (1 - xs) * vL)))
    else:
        Out = NaN
    
    
case 'vx_ps'
    p = toSIunit_p(In1)
    s = toSIunit_s(In2)
    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            vL = v1_pT(p, T4_p(p))
            vV = v2_pT(p, T4_p(p))
        else:
            vL = v3_ph(p, h4L_p(p))
            vV = v3_ph(p, h4V_p(p))
        
        xs = x4_ps(p, s)
        Out = fromSIunit_vx((xs * vV / (xs * vV + (1 - xs) * vL)))
    else:
        Out = NaN
    
 
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





def u3_rhoT(rho, T):
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
fitau = 0
for i  in range(2, 40):
    fitau = fitau + ni[i] * delta ** Ii[i] * Ji[i] * tau ** (Ji[i] - 1)
u3_rhoT = R * T * (tau * fitau)



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







def T4_hs(h, s):
#Supplementary Release on Backward Equations ( ) , p h s for Region 3,
#Chapter 5.3 page 30.
#The if  97 function is only valid for part of region4. Use iteration outsida:
Ii = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 8, 10, 10, 12, 14, 14, 16, 16, 18, 18, 18, 20, 28]
Ji = [0, 3, 12, 0, 1, 2, 5, 0, 5, 8, 0, 2, 3, 4, 0, 1, 1, 2, 4, 16, 6, 8, 22, 1, 20, 36, 24, 1, 28, 12, 32, 14, 22, 36, 24, 36]
ni = [0.179882673606601, -0.267507455199603, 1.162767226126, 0.147545428713616, -0.512871635973248, 0.421333567697984, 0.56374952218987, 0.429274443819153, -3.3570455214214, 10.8890916499278, -0.248483390456012, 0.30415322190639, -0.494819763939905, 1.07551674933261, 7.33888415457688E-02, 1.40170545411085E-02, -0.106110975998808, 1.68324361811875E-02, 1.25028363714877, 1013.16840309509, -1.51791558000712, 52.4277865990866, 23049.5545563912, 2.49459806365456E-02, 2107964.67412137, 366836848.613065, -144814105.365163, -1.7927637300359E-03, 4899556021.00459, 471.262212070518, -82929439019.8652, -1715.45662263191, 3557776.82973575, 586062760258.436, -12988763.5078195, 31724744937.1057]
if  (s > 5.210887825 & s < 9.15546555571324)==:
    Sigma = s / 9.2
    eta = h / 2800
    teta = 0
    for i  in range(1, 36):
        teta = teta + ni[i] * (eta - 0.119) ** Ii[i] * (Sigma - 1.07) ** Ji[i]
    
    T4_hs = teta * 550
else:
    #function psat_h
    if  (s > -0.0001545495919 and s <= 3.77828134)==:
        Low_Bound = 0.000611
        High_Bound = 165.291642526045
        hL=-1000
        while abs(hL - h) > 0.00001 and abs(High_Bound - Low_Bound) > 0.0001
            PL = (Low_Bound + High_Bound) / 2
            Ts = T4_p(PL)
            hL = h1_pT(PL, Ts)
            if  hL > h:
                High_Bound = PL
            else:
                Low_Bound = PL
            
        
    elif  s > 3.77828134 and s <= 4.41202148223476:
        PL = p3sat_h(h)
    elif  s > 4.41202148223476 and s <= 5.210887663:
        PL = p3sat_h(h)
    
    Low_Bound = 0.000611
    High_Bound = PL
    sss=-1000
    while (abs(s - sss) > 0.000001 & abs(High_Bound - Low_Bound) > 0.0000001)==1
        p = (Low_Bound + High_Bound) / 2
        #Calculate s4_ph
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
        
        sss = (xs * s4v + (1 - xs) * s4L)
        
        if  sss < s:
            High_Bound = p
        else:
            Low_Bound = p
        
    
    T4_hs = T4_p(p)
    
    

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

def T5_ph(p, h):
#Solve with half interval method
Low_Bound = 1073.15
High_Bound = 2273.15
hs=h-1
while abs(h - hs) > 0.00001
    Ts = (Low_Bound + High_Bound) / 2
    hs = h5_pT(p, Ts)
    if  hs > h:
        High_Bound = Ts
    else:
        Low_Bound = Ts
    
T5_ph = Ts

def T5_ps(p, s):
#Solve with half interval method
Low_Bound = 1073.15
High_Bound = 2273.15
ss=s-1
while abs(s - ss) > 0.00001
    Ts = (Low_Bound + High_Bound) / 2
    ss = s5_pT(p, Ts)
    if  ss > s:
        High_Bound = Ts
    else:
        Low_Bound = Ts
    
T5_ps = Ts
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


#***********************************************************************************************************
#*6 Units                                                                                      *
#***********************************************************************************************************



#***********************************************************************************************************
#*7 Verif ication                                                                                      :
#***********************************************************************************************************

def check():
err=0
#*********************************************************************************************************
#* 7.1 Verif iy region :
#IF-97 Table 5, Page 9
p=[30/10,800/10,30/10]
T=[300,300,500]
Fun={'v1_pT','h1_pT','u1_pT','s1_pT','Cp1_pT','w1_pT'}
IF97=[0.00100215168,0.000971180894,0.001202418...
        115.331273,184.142828,975.542239...
        112.324818,106.448356,971.934985...
        0.392294792,0.368563852,2.58041912...
        4.17301218,4.01008987,4.65580682...
        1507.73921,1634.69054,1240.71337]
R1=zeros(6,3)
for i in range(1, 3):
    for j in range(1, 6):
        R1(j,i)=eval([char(Fun(j)),'(',num2str(p(i)),',',num2str(T(i)),')'])
    
Region1_error=abs((R1-IF97)./IF97)
err=err+sum(sum(Region1_error>1E-8))
#IF-97 Table 7, Page 11
p=[30/10,800/10,800/10]
h=[500,500,1500]
IF97=[391.798509,378.108626,611.041229]
R1=zeros(1,3)
for i in range(1, 3):
    R1(i)=T1_ph(p(i),h(i))
T1_ph_error=abs((R1-IF97)./IF97)
err=err+sum(sum(T1_ph_error>1E-8))
#IF-97 Table 9, Page 12
p=[30/10,800/10,800/10]
s=[0.5,0.5,3]
IF97=[307.842258,309.979785,565.899909]
R1=zeros(1,3)
for i in range(1, 3):
    R1(i)=T1_ps(p(i),s(i))
T1_ps_error=abs((R1-IF97)./IF97)
err=err+sum(sum(T1_ps_error>1E-8))
#Supplementary Release on Backward Equations 
#for Pressure as a Function of Enthalpy and Entropy p(h,s) 
#Table 3, Page 6
h=[0.001,90,1500]
s=[0,0,3.4]
IF97=[0.0009800980612,91.929547272,58.68294423]
R1=zeros(1,3)
for i in range(1, 3):
    R1(i)=p1_hs(h(i),s(i))
p1_hs_error=abs((R1-IF97)./IF97)
err=err+sum(sum(p1_hs_error>1E-8))
#*********************************************************************************************************
#* 7.2 Verif iy region :
# IF-97 Table 15, Page 17
p=[0.035/10,0.035/10,300/10]
T=[300,700,700]
Fun={'v2_pT','h2_pT','u2_pT','s2_pT','Cp2_pT','w2_pT'}
IF97=[39.4913866,92.3015898,0.00542946619...
        2549.91145,3335.68375,2631.49474...
        2411.6916,3012.62819,2468.61076...
        8.52238967,10.1749996,5.17540298...
        1.91300162,2.08141274,10.3505092...
        427.920172,644.289068,480.386523]
R2=zeros(6,3)
for i in range(1, 3):
    for j in range(1, 6):
        R2(j,i)=eval([char(Fun(j)),'(',num2str(p(i)),',',num2str(T(i)),')'])
    
Region2_error=abs((R2-IF97)./IF97)
err=err+sum(sum(Region2_error>1E-8))
#IF-97 Table 24, Page 25
p=[0.01/10,30/10,30/10,50/10,50/10,250/10,400/10,600/10,600/10]
h=[3000,3000,4000,3500,4000,3500,2700,2700,3200]
IF97=[534.433241,575.37337,1010.77577,801.299102,1015.31583,875.279054,743.056411,791.137067,882.75686]
R2=zeros(1,9)
for i in range(1, 9):
    R2(i)=T2_ph(p(i),h(i))
T2_ph_error=abs((R2-IF97)./IF97)
err=err+sum(sum(T2_ph_error>1E-8))
#IF-97 Table 29, Page 29
p=[1/10,1/10,25/10,80/10,80/10,900/10,200/10,800/10,800/10]
s=[7.5,8,8,6,7.5,6,5.75,5.25,5.75]
IF97=[399.517097,514.127081,1039.84917,600.48404,1064.95556,1038.01126,697.992849,854.011484,949.017998]
R2=zeros(1,9)
for i in range(1, 9):
    R2(i)=T2_ps(p(i),s(i))
T2_ps_error=abs((R2-IF97)./IF97)
err=err+sum(sum(T2_ps_error>1E-8))
#Supplementary Release on Backward Equations for Pressure as a Function of Enthalpy and Entropy p(h,s) 
#Table 3, Page 6
h=[2800,2800,4100,2800,3600,3600,2800,2800,3400]
s=[6.5,9.5,9.5,6,6,7,5.1,5.8,5.8]
IF97=[1.371012767,0.001879743844,0.1024788997,4.793911442,83.95519209,7.527161441,94.3920206,8.414574124,83.76903879]
R2=zeros(1,9)
for i in range(1, 9):
    R2(i)=p2_hs(h(i),s(i))
p2_hs_error=abs((R2-IF97)./IF97)
err=err+sum(sum(p2_hs_error>1E-8))
#*********************************************************************************************************
#* 7.3 Verif iy region :
# IF-97 Table 33, Page 32
T=[650,650,750]
rho=[500,200,500]
Fun={'p3_rhoT','h3_rhoT','u3_rhoT','s3_rhoT','Cp3_rhoT','w3_rhoT'}
IF97=[25.5837018,22.2930643,78.3095639...
        1863.43019,2375.12401,2258.68845...
        1812.26279,2263.65868,2102.06932...
        4.05427273,4.85438792,4.46971906...
        13.8935717,44.6579342,6.34165359...
        502.005554,383.444594,760.696041]
R3=zeros(6,3)
for i in range(1, 3):
    for j in range(1, 6):
        R3(j,i)=eval([char(Fun(j)),'(',num2str(rho(i)),',',num2str(T(i)),')'])
    
Region3_error=abs((R3-IF97)./IF97)
err=err+sum(sum(Region3_error>1E-8))
#T3_ph
p=[200/10,500/10,1000/10,200/10,500/10,1000/10]
h=[1700,2000,2100,2500,2400,2700]
IF97=[629.3083892,690.5718338,733.6163014,641.8418053,735.1848618,842.0460876]
R3=zeros(1,6)
for i in range(1, 6):
    R3(i)=T3_ph(p(i),h(i))
T3_ph_error=abs((R3-IF97)./IF97)
err=err+sum(sum(T3_ph_error>1E-8))
#v3_ph
p=[200/10,500/10,1000/10,200/10,500/10,1000/10]
h=[1700,2000,2100,2500,2400,2700]
IF97=[0.001749903962,0.001908139035,0.001676229776,0.006670547043,0.0028012445,0.002404234998]
R3=zeros(1,6)
for i in range(1, 6):
    R3(i)=v3_ph(p(i),h(i))
v3_ph_error=abs((R3-IF97)./IF97)
err=err+sum(sum(v3_ph_error>1E-7))
#T3_ps
p=[200/10,500/10,1000/10,200/10,500/10,1000/10]
s=[3.7,3.5,4,5,4.5,5]
IF97=[620.8841563,618.1549029,705.6880237,640.1176443,716.3687517,847.4332825]
R3=zeros(1,6)
for i in range(1, 6):
    R3(i)=T3_ps(p(i),s(i))
T3_ps_error=abs((R3-IF97)./IF97)
err=err+sum(sum(T3_ps_error>1E-8))
#v3_ps
p=[200/10,500/10,1000/10,200/10,500/10,1000/10]
s=[3.7,3.5,4,5,4.5,5]
IF97=[0.001639890984,0.001423030205,0.001555893131,0.006262101987,0.002332634294,0.002449610757]
R3=zeros(1,6)
for i in range(1, 6):
    R3(i)=v3_ps(p(i),s(i))
v3_ps_error=abs((R3-IF97)./IF97)
err=err+sum(sum(v3_ps_error>1E-8))
#p3_hs
h=[1700,2000,2100,2500,2400,2700]
s=[3.8,4.2,4.3,5.1,4.7,5]
IF97=[25.55703246,45.40873468,60.7812334,17.20612413,63.63924887,88.39043281]
R3=zeros(1,6)
for i in range(1, 6):
    R3(i)=p3_hs(h(i),s(i))
p3_hs_error=abs((R3-IF97)./IF97)
err=err+sum(sum(p3_hs_error>1E-8))
#h3_pT (Iteration)
p=[255.83702,222.93064,783.09564]./10
T=[650,650,750]
IF97=[1863.271389,2375.696155,2258.626582]
R3=zeros(1,3)
for i in range(1, 3):
    R3(i)=h3_pT(p(i),T(i))
h3_pT_error=abs((R3-IF97)./IF97)
err=err+sum(sum(h3_pT_error>1E-6)) #Decimals in IF97
#*********************************************************************************************************
#* 7.4 Verif iy region :
#Saturation pressure, If97, Table 35, Page 34
T=[300,500,600]
IF97=[0.0353658941, 26.3889776, 123.443146]/10
R3=zeros(1,3)
for i in range(1, 3):
    R4(i)=p4_T(T(i))
p4_t_error=abs((R4-IF97)./IF97)
err=err+sum(sum( p4_t_error>1E-7))
T=[1,10,100]/10
IF97=[372.755919,453.035632,584.149488]
R3=zeros(1,3)
for i in range(1, 3):
    R4(i)=T4_p(T(i))
T4_p_error=abs((R4-IF97)./IF97)
err=err+sum(sum( T4_p_error>1E-7))
s=[1,2,3,3.8,4,4.2,7,8,9,5.5,5,4.5]
IF97=[308.5509647,700.6304472,1198.359754,1685.025565,1816.891476,1949.352563,2723.729985,2599.04721,2511.861477,2687.69385,2451.623609,2144.360448]
R3=zeros(1,12)
for i in range(1, 12):
    R4(i)=h4_s(s(i))
h4_s_error=abs((R4-IF97)./IF97)
err=err+sum(sum( h4_s_error>1E-7)) 
#*********************************************************************************************************
#* 7.5 Verif iy region :
# IF-97 Table 42, Page 39
T=[1500,1500,2000]
p=[5,80,80]/10
Fun={'v5_pT','h5_pT','u5_pT','s5_pT','Cp5_pT','w5_pT'}
IF97=[1.38455354,0.0865156616,0.115743146...
        5219.76332,5206.09634,6583.80291...
        4527.48654,4513.97105,5657.85774...
        9.65408431,8.36546724,9.15671044...
        2.61610228,2.64453866,2.8530675...
        917.071933,919.708859,1054.35806]
R5=zeros(6,3)
for i in range(1, 3):
    for j in range(1, 6):
        R5(j,i)=eval([char(Fun(j)),'(',num2str(p(i)),',',num2str(T(i)),')'])
    
Region5_error=abs((R5-IF97)./IF97)
err=err+sum(sum(Region5_error>1E-8))
#T5_ph (Iteration)
p=[0.5,8,8]
h=[5219.76331549428,5206.09634477373,6583.80290533381]
IF97=[1500,1500,2000]
R5=zeros(1,3)
for i in range(1, 3):
    R5(i)=T5_ph(p(i),h(i))
T5_ph_error=abs((R5-IF97)./IF97)
err=err+sum(sum(T5_ph_error>1E-7)) #Decimals in IF97
#T5_ps (Iteration)
p=[0.5,8,8]
s=[9.65408430982588,8.36546724495503,9.15671044273249]
IF97=[1500,1500,2000]
R5=zeros(1,3)
for i in range(1, 3):
    R5(i)=T5_ps(p(i),s(i))
T5_ps_error=abs((R5-IF97)./IF97)
err=err+sum(sum(T5_ps_error>1E-4)) #Decimals in IF97
#*********************************************************************************************************
#* 7.6 Verif iy calling funtion:
fun={'Tsat_p','T_ph','T_ps','T_hs','psat_T','p_hs','hV_p','hL_p','hV_T','hL_T','h_pT','h_ps','h_px','h_prho','h_Tx','vV_p','vL_p','vV_T','vL_T','v_pT','v_ph','v_ps','rhoV_p','rhoL_p','rhoV_T','rhoL_T','rho_pT','rho_ph','rho_ps','sV_p','sL_p','sV_T','sL_T','s_pT','s_ph','uV_p','uL_p','uV_T','uL_T','u_pT','u_ph','u_ps','CpV_p','CpL_p','CpV_T','CpL_T','Cp_pT','Cp_ph','Cp_ps','CvV_p','CvL_p','CvV_T','CvL_T','Cv_pT','Cv_ph','Cv_ps','wV_p','wL_p','wV_T','wL_T','w_pT','w_ph','w_ps','my_pT','my_ph','my_ps','tcL_p','tcV_p','tcL_T','tcV_T','tc_pT','tc_ph','tc_hs','st_T','st_p','x_ph','x_ps','vx_ph','vx_ps'}
In1={'1','1','1','100','100','84','1','1','100','100','1','1','1','1','100','1','1','100','100','1','1','1','1','1','100','100','1','1','1','0.006117','0.0061171','0.0001','100','1','1','1','1','100','100','1','1','1','1','1','100','100','1','1','1','1','1','100','100','1','1','1','1','1','100','100','1','1','1','1','1','1','1','1','25','25','1','1','100','100','1','1','1','1','1'}
In2={'0','100','1','0.2','0','0.296','0','0','0','0','20','1','0.5','2','0.5','0','0','0','0','100','1000','5','0','0','0','0','100','1000','1','0','0','0','0','20','84.01181117','0','0','0','0','100','1000','1','0','0','0','0','100','200','1','0','0','0','0','100','200','1','0','0','0','0','100','200','1','100','100','1','0','0','0','0','25','100','0.34','0','0','1000','4','418','4'}
Control={'99.60591861','23.84481908','73.70859421','13.84933511','1.014179779','2.295498269','2674.949641','417.4364858','2675.572029','419.099155','84.01181117','308.6107171','1546.193063','1082.773391','1547.33559210927','1.694022523','0.001043148','1.671860601','0.001043455','1.695959407','0.437925658','1.03463539','0.590310924','958.6368897','0.598135993','958.3542773','0.589636754','2.283492601','975.6236788','9.155465556','1.8359E-05','9.155756716','1.307014328','0.296482921','0.296813845','2505.547389','417.332171','2506.015308','418.9933299','2506.171426','956.2074342','308.5082185','2.075938025','4.216149431','2.077491868','4.216645119','2.074108555','4.17913573168802','4.190607038','1.552696979','3.769699683','1.553698696','3.76770022','1.551397249','4.035176364','3.902919468','472.0541571','1545.451948','472.2559492','1545.092249','472.3375235','1542.682475','1557.8585','1.22704E-05','0.000914003770302108','0.000384222','0.677593822','0.024753668','0.607458162','0.018326723','0.607509806','0.605710062','0.606283124','0.0589118685876641','0.058987784','0.258055424','0.445397961','0.288493093','0.999233827'}
for i=1:length(fun)
    
    T=['XSteam(''',char(fun(i)),''',',char(In1[i]),',',char(In2(i)),')']
    Res=eval(T)
    Error=(Res-(str2num(char(Control(i)))))/str2num(char(Control(i)))
    Check=[T,'=',num2str(Res),' - (Control)',char(Control(i)),'=',num2str(Error)]
    if  Error>1E-:
        err=err+1
        error('To large error')
       
