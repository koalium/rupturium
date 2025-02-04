#
#
#
import pandas as pd
import FreeSimpleGUI as sg
from string import *
from dbmakeread import *
from tester import *
from openpyxl import load_workbook

#
rawplatelen=2000
rawplatewidth=1000
RAWSHEETW=2000
RAWSHEETH=1000
Lmargin=5
CanvasW = 630
CanvasH = 400
CRM=5
CLM=5
CTM=5
CBM=5
CLBX=CLM
CLBY=CBM
CRTX=CanvasW-CRM
CRTY=CanvasH-CTM
LASERM=5
sheetleftm=5
rupleftm=5
sheetm=5
rupm=5
LINEWIDTH=2
XSEP=LASERM+LINEWIDTH*2
YSEP=pow(3,0.5)*LASERM+LINEWIDTH*2/2
CW=CanvasW
CH=CanvasH
sheetleftbootomx=CLBX+sheetm
sheetleftbootomy=CLBY+sheetm
sheetrightxmax=CRTX-sheetm
sheettopymax=CRTY-sheetm


SHEETLEN = 2000
SHEETWID = 1000
SLM = 8
SRM = 7
STM=8
SBM=7
LDM=5
LCW=1


    
    
def getrawsheetmatdimension(rod,qty,rawswide):
    raww=int(rod)+int(STM)+int(SBM)+int(LDM)+2*int(LCW)
    maxrupperrawlen= (rawswide-SLM-SRM-2*LDM)/(rod+LCW+XSEP)
    rawh=rod
    if qty>=maxrupperrawlen:
        rawh=rawswide
        qtcont=qty
        colperrow = maxrupperrawlen
        while qtcont>0:
            qtcont-=colperrow
            if colperrow== maxrupperrawlen:
                colperrow=maxrupperrawlen-1
            else :
                colperrow= maxrupperrawlen
            raww+=pow(3,0.5)*0.5*(rod+YSEP+2*LCW+LDM)
    else:
        rawh=qty*(rod+LCW+XSEP)+(SLM+SRM+2*LDM)
    raw=[]
    raw.append(rawh)
    raw.append(raww)
    return raw
        
        
        


ruplinewidth=2
def redrawratio():
    ratio = CW/RAWSHEETW
    return ratio

    
def getnextrupturedraw(r,frc):
    
    rx=r[0]
    ry=r[1]    
    rd=r[2]
    rw=r[3]
    rn=r[4]+1
    rr=r[5]
    rc=r[6]+1
    rps=(RAWSHEETW/(rd*2+XSEP))-(rr%2)
    if rc<rps:
        rx=r[0]+rd*2+XSEP
    else:
        rr+=1
        rc=0
        ry += pow(3,0.5)*0.5*(2*rr)+YSEP
        if rr%2==0:
            rx=frc
        else:
            rx = (frc + 2*rr+XSEP)*0.5
    r=[]        
    r.append(rx)
    r.append(ry)
    r.append(rd)
    r.append(rw)
    r.append(rn)  
    r.append(rr)
    r.append(rc)
    return r
 
def drawrupturesinplate(gr,qty=8,rod=108,rph=1000,rawplatewide=2000):  
    gm = 5 #graphic margin that allstart at this
    gblx=gr.BottomLeft[0]
    gbly=gr.BottomLeft[1]
    gw=gr.Size[0]
    gh=gr.Size[1]
    gtrx=gblx+gw
    gtry=gbly+gh
    rpblx=gblx+gm
    rpbly=gbly+gm
    rptrym=gtry-gm
    rptrxm=gtrx-gm
    xsep=5
    ysep=5
    rpsm=10
    lcm=2
    halfdia=rod/2
    rad=halfdia
    rpr = int((rpsw -25)/(rod+10))
    screenviewWiderawplate= rptrxm-rpblx
    ratio = screenviewWiderawplate/rawplatewide
    screenviewheightrawplate = int(rph*ratio)
    
    drr=int(rad*ratio)
    rcrad=drr+lcm
    cpfdrx = rpblx+rpsm+lcm+drr
    cpfdry=  rpbly+rpsm+lcm+drr
    usedplateblx=rpblx
    usedplatebly = rpbly
    
    cpsepx = drr+lcm+xsep+lcm+drr
    cpsepy = int(ysep+(drr+lcm+lcm+drr)*pow(30.5)*0.5)
    cpfrsrx= int(cpfdrx+cpsepx*0.5)
    col = 0
    row = 0
    gr.draw_rectangle((rplbx,rplby),(rptrx,rptry), fill_color='blue', line_color='green', line_width=1)
    usedplatetrx =usedplateblx
    usedplatetry = cpfdry*2
    rowt= int(qty/(rpr*2-1))
    rowi = int((qty%(rpr*2-1))/rpr)
    rowu = rowt*2+rowi
    usedplatetry= rowu*cpsepy+cpfdry*2
    if qty>= rpr:
        usedplatetrx = rptrx
    else:
        usedplatetrx = (cpfdrx*2)+ (qty-1)*cpsepx
        
    gr.draw_rectangle((usedplateblx,usedplatebly),(usedplatetrx,usedplatetry), fill_color='cyan', line_color='red', line_width=0)
    for i in range(qty):
        col+=1
        if col >= rpr-(row%2):
            roe+=1
            col = 0
            
            
            
        x= col * cpsepx + cpfdrx
        y=row*cpsepy+cpfdry
        gr.draw_circle(center_location=(x,y), radius=drr, fill_color='red', line_color='yellow', line_width=lcm) 
    
    
    

def drawruptures(gr,rqty,rod,rawplatelen):
    
    
    rpcenter=[firstrupturecenterx,firstrupturecentery]
    thisrup=[firstrupturecenterx,firstrupturecentery,ruprad,ruplinewidth]
    
    linewidth = 1
    edgemargin=2
    leftmargin=2
    rightmargin =1
    topmargin=5
    bottommargin=5
    xseperation  = Lmargin+2*linewidth
    yseperation = xseperation*pow(3,0.5)   /2
    rcpr=int((rawplatelen-2*Lmargin)/(rod+xseperation))
    canvratio= (CanvasW/rawplatelen)
    if ((xseperation+rod)*(rqty))>(CanvasW*0.95):
        rod *=canvratio
        xseperation*=canvratio
        yseperation*=canvratio
    rad = (rod/2)
    gr.erase()   
    
    col = 0
    row = 0
    x0d=(rad+leftmargin+linewidth)
    y0d= rad+bottommargin+linewidth
    x0=x0d
    y0=y0d
    
    dx=int(2*(rad+xseperation))
    dy=int(pow(3,0.5)*(rad+yseperation))
    rc=0
    platepoint = mainpatedrawpositions(rqty,xseperation,yseperation,rcpr,rad,rad,Lmargin)
    gr.draw_rectangle((platepoint[0],platepoint[1]),(platepoint[2],platepoint[3]), fill_color='blue', line_color='green', line_width=linewidth)
    #gr.draw_rectangle((2,min(395,(1+(rqty/rcpr))*(rod+xmargin)+2*Lmargin)), bottom_right=(min(rcpr,rqty)*(rod+xmargin+2)+Lmargin*2+5,5), fill_color='blue', line_color='green', line_width=1)
    for i in range(rqty):
        x=rc*dx+x0
        y=row*dy+y0
        center=(x,y)
        gr.draw_circle(center_location=center, radius=rad, fill_color='red', line_color='yellow', line_width=linewidth) 
        rc+=1
        if rc >= rcpr:
            rc=0 
            row+=1
            if row%2==0:
                rcpr+=1
                x0=x0d
            else:
                rcpr-=1
                x0=x0d+rad+xseperation
    
def calcplatearea(rod,qty):
    rod=float(rod)
    hmargin=5
    vmargin = 5
    rawplatelen=2000
    xseperation  = Lmargin+2
    yseperation = xseperation*pow(3,0.5)/2
    rcpr=1
    rcpr=int((rawplatelen-2*Lmargin)/(rod+Lmargin)) 
    rawplatelen=min(qty,rcpr)*(rod+Lmargin)*2+hmargin  
    if qty>=rcpr:
        rawplatelen = rawplatelen
    
    rows=int(qty/rcpr)
    rawplatewidth = rod+Lmargin+2*vmargin+(rows-1)*(pow(3,0.5)*(rod+Lmargin))/2
    dim=[]
    dim.append(rawplatelen)
    dim.append(rawplatewidth)
    return dim
                   
def mainpatedrawpositions(qty,xsep,ysep,rpr,rad,linewidth,lmargin):
    blx=5
    bly=5
    col = min(qty,rpr)
    trx=(col-1)*xsep+col*(2*(rad+linewidth))+lmargin*2+blx
    rows=int(qty/rpr)
    toprighty = (rows-1)*ysep+2*(rad+linewidth)+lmargin*2+bly+(rows-1)*(pow(3,0.5)*(rad+ysep))/2
    p=[]
    p.append(blx)
    p.append(bly)
    p.append(trx)
    p.append(toprighty)
    return p
    
        
        
    
        

def clearcanvas(gr):
    gr.Erase()
    



def makemtoframe(element):
    hsheet = pd.read_excel(dbfilename, sheet_name =str(mtoheader.lower()), index_col=None, header=0)
    details = pd.DataFrame(hsheet)
    mask_var = details['element'] == element  
    details = details[mask_var]   
    return details

def makemtoframeruptures(rtype):
    rf = makemtoframe('rupture')
    if(str(rtype).lower()=='flat'):
        rf = rf[rf['type']==1]
    return rf

def listofdetofrup(rtype):
    rd = makemtoframeruptures(rtype)
    
