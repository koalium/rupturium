from globalvars import *

import pandas as pd
import os


def squararia(w,l):
    return w*0.001*l*0.001;

def volumeofarea(a,l):
    return a*l*0.001

def circarea(d):
    d = d*0.001
    a = 3.14*d*d*0.25
    return a

def cylindrevol(od,tickness):
    return volumeofarea(circarea(od),tickness)



def massofvolumeofmaterial(vol,den):
    m = vol*den*1000
    return m

def calcpricebymass(mass,ppm):
    return mass*ppm

                
def calcrawsheetforruptures(rodl=118,qty=5,shw=rupturerawplatewidthmm,shh=rupturerawplateheightmm):
    tm=bm=rm=lm=rupturelasermetalsheetedgemargins
    cw=rupturelasermetalsheetcutwidth
    xsep=rupturelasermetalsheetcutmargins
    ysep=rupturelasermetalsheetcutmargins
    rod=rodl[0]
    lsm=rupturelasermetalsheetedgemargins
    lcm =rupturelasermetalsheetcutwidth
    xsepm=rupturelasermetalsheetcutmargins
    rsq=1
    rsw = shw - lsm*2
    rsh= shh -2*lsm       
    rrod = rod + lcm*2
    rawsheetwide = (rrod+xsepm)*qty+2*lsm
    rawsheetheight = rrod +lsm*2
    page=1
    myrow=0    
    rawdim = []
    rad=rod*0.5
    rawdim.append(int(rawsheetwide))
    rawdim.append(int(rawsheetheight))
    rawdim.append(rsq)
    rawdim.append(page)
    rawdim.append(myrow)
    rawdim.append(rawsheetwide)
    rawdim.append(rawsheetheight)    
     
    rprm = int(rsw/(rrod+xsepm))
    if qty < rprm:
        return rawdim  
    rawdim = []
    rawsheetwide=shw
    ystagerratio = pow(3,0.5)*0.5
    
    
    
    rprn = rprm-1
    col=0
    row=0
    
    x0=lm+cw+rad
    y0=bm+cw+rad
    x=x0
    y=y0
    page=1
    myrow=0
    circount=0
    rp=[]
    crp=[]
    crp.append(x)
    crp.append(y)
    crp.append(circount)
    rp.append(crp)
    crocont=0
    shcont=0
    for i in range(qty):
        x=x+rad+cw+xsep+cw+rad
        if x+rad+cw+rm >= shw:
            
            row+=1
            x=x0+(rad+cw+xsep+cw+rad)*0.5*(row%2)
            y=y+pow(3,0.5)*0.5*(rad+cw+ysep+cw+rad)
            if y+rad+cw+tm>=shh:
                shcont+=1
                x=x0
                y=y0
                row=0


    rawdim = []
    rawdim.append(shw)
    rawdim.append(shh)
    rawdim.append(shcont)
    return rawdim         
                
    

def calcoverneedruptureqtyfordesign(rtype,rsize):
    rtype = rtype.lower()
    oq = 1
    if  rtype=='reverse':
        oq+=2
        if rsize<=4:
            oq+=6
        elif int(rsize)<=8:
            oq+=5
        else:
            oq+=4
    else:
        if int(rsize)>6:
            oq+=2
        else:
            oq+=3
    return oq

def getruptureqtyrawmaterial(qty=1,rtype='flat',rsize=4):
    ar= []
    ar.append(qty)
    from filehandler import getoverqtyrupturefortest
    ar.append(getoverqtyrupturefortest(qty))
    ar.append(calcoverneedruptureqtyfordesign(rtype,rsize))
    return ar