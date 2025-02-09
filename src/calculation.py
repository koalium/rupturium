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
    for i in range(qty):
        col+=1
        if col >= (rprm-(row%2)):
            row+=1
            myrow+=1
            col = 0
        x=x+rad+cw+xsep+cw+rad
        if x+cw+rad+rm >= shw:
            y=y+pow(3,0.5)*0.5*(rad+cw+ysep+cw+rad)
            x=x0+(row%2)*(cw+rad+rad+cw)
            if y> shh:
                page+=1
                x=x0
                y=y0
                myrow=0
                
    rawsheetheight +=  (rrod) *ystagerratio*row
    if rawsheetheight> shh:
        rsq = int(rawsheetheight/shh)
        rsq+=1
    rawsheetheightover = rawsheetheight % shh
    rawdim = []
    rawdim.append(rawsheetwide)
    rawdim.append(int(rawsheetheight))
    rawdim.append(rsq)
    rawdim.append(int(rawsheetheightover))
    rawdim.append(page)
    rawdim.append(myrow)
    rawdim.append(x+rad+cw+rm)
    rawdim.append(y+rad+cw+tm)
    return rawdim         
                
    

def calcoverneedruptureqtyfordesign(rtype,rsize):
    rtype = rtype.lower()
    oq = 1
    if  rtype=='reverse':
        oq = oq+2
        if int(rsize)<=8:
            return 5
        else:
            return 4
    else:
        if int(rsize)>6:
            return 2
        else:
            return 3
    return 1 

def getruptureqtyrawmaterial(qty=1,rtype='flat',rsize=4):
    ar= []
    ar.append(qty)
    from filehandler import getoverqtyrupturefortest
    ar.append(getoverqtyrupturefortest(qty))
    ar.append(calcoverneedruptureqtyfordesign(rtype,rsize))
    return ar