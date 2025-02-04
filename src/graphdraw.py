from calculation import *
from globalvars import *
import pandas as pd
import os

Global_plane=[]
Global_planeviewnum = 0

def drawrupturesinplate(gr,qty=8,rod=155,rph=1000,rawplatewide=2000):  
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
    rpgw=rptrxm-rpblx
    rpgh=rptrym-rpbly
    xsep=5
    ysep=5
    rpsm=10
    lcm=2
    halfdia=rod/2
    rad=halfdia
    rpr = int((rawplatewide -25)/(rod+10))
    screenviewWiderawplate= rptrxm-rpblx
    ratio = screenviewWiderawplate/rawplatewide
    screenviewheightrawplate = int(rph*ratio)
    rptrym=rph*ratio+gm
    rpgh=rptrym
    drr=int(rad*ratio)
    rcrad=drr+lcm
    cpfdrx = rpblx+rpsm+lcm+drr
    cpfdry=  rpbly+rpsm+lcm+drr
    usedplateblx=rpblx
    usedplatebly = rpbly
    
    cpsepx = drr+lcm+xsep+lcm+drr
    cpsepy = int(ysep+(drr+lcm+lcm+drr)*pow(3,0.5)*0.5)
    cpfrsrx= int(cpfdrx+cpsepx*0.5)
    col = 0
    row = 0
    gr.draw_rectangle((rpblx,rpbly),(rpgw,rpgh), fill_color='blue', line_color='green', line_width=1)
    usedplatetrx =usedplateblx
    usedplatetry = cpfdry*2
    
    
    
    
    
    if qty>= rpr:
        usedplatetrx = rptrxm
        upgw=rpgw
    else:
        usedplatetrx = (cpfdrx*2)+ (qty-1)*(cpsepx-rpsm)
        upgw=(cpfdrx*2)+ (qty-1)*(cpsepx-rpsm)
    if upgw> rpgw:
        usedplatetrx = rptrxm
        upgw=rpgw
        
    rowtqty=1
    stagering=1
    if  (((rpr-1)* cpsepx )+ cpfdrx*2) < rpgw:
        stagering = 0
        rowtqty = 2*rpr
    else:
        rowtqty = 2*rpr-1
    rowt= int(qty/rowtqty)
    rowqtymod = qty-(rowt*rowtqty)
    rowi=0
    if rowqtymod>=rpr:
        rowi = 2
    elif rowqtymod>0:
        rowi=1
    else:
        rowi=0
    rowu = rowt*2+rowi
    upgh= (rowu-1)*cpsepy+(cpfdry-rpsm)*2
    upgw=rpgw    
    gr.draw_rectangle((usedplateblx,usedplatebly),(upgw,upgh), fill_color='magenta', line_color='red', line_width=0)
    cpfdrx0=cpfdrx
    for i in range(qty):
        col+=1
        if col == rpr-(row%2)*stagering:
            row+=1
            col = 1
            if row%2==1:
                cpfdrx0=cpfrsrx
            else:
                cpfdrx0=cpfdrx                
            
        x= ((col -1)* cpsepx )+ cpfdrx0
        if x+drr+lcm+gm > rptrxm:
            row+=1
            col = 1
            if row%2==1:
                cpfdrx0=cpfrsrx
            else:
                cpfdrx0=cpfdrx             
            
        x= ((col -1)* cpsepx )+ cpfdrx0    
            
        
        y=row*cpsepy+cpfdry
        gr.draw_circle(center_location=(x,y), radius=drr, fill_color='red', line_color='yellow', line_width=lcm) 
        
    
def pointcircleinplane(planesize=[400,200],planemargin=(8,8,8,8),circleDiameter=10,seperation=(5,5),q=5,tip='se'):#tip se stagered even line , so odd row , inline overheades
    plans=[]
    plate=[]
    r = int(circleDiameter*0.5)
    bm =planemargin[0]
    lm = planemargin[1]
    tm = planemargin[2]
    rm = planemargin[3]
    pw = planesize[0]
    ph = planesize[1]
    xsep = seperation[0]
    ysep = seperation[1]
    
    ccpx0= lm+r
    ccpy0= bm+r
    circle=[]
    col=0
    row=0
    y0def= r+bm
    x0def = r+lm
    x0=x0def
    y0= r+bm
    y=y0
    x=x0
    usedplane=[]
    cir=[]
    cir.append(x)
    cir.append(y)
    circle.append(cir)
    upw=lm+rm+r+r
    uph=bm+tm+r+r
    uphmax=uph
    for i in range(1,q):
        usedplane=[]
        y=y+(r+r+ysep)
        if y+r+rm>=ph:
            row+=1
            y=y0def+(row%2)*(r+ysep+r)*0.5
            x+=pow(3,0.5)*0.5*(r+xsep+r)
            uphmax=ph
            if (x+r+rm)>pw:
                plate=[]
                plate.append(circle)
                plate.append(usedplane)   
                plans.append(plate)
                circle=[]
                col=0
                row=0
                y0def= r+bm
                x0def = r+lm
                x0=x0def
                y0= r+bm
                y=y0
                x=x0
                               
                
        cir=[]
        cir.append(x)
        cir.append(y)
        circle.append(cir)
        upw=x+r+rm
        uph=max(uphmax,y+r+tm)
        if (y+r+tm)>uphmax:
            uphmax = uph
        
        usedplane.append(upw)
        usedplane.append(uphmax)
        
            
    plate=[]
    plate.append(circle)
    plate.append(usedplane)   
    plans.append(plate)
    return plans




def drawrupturescirclesinplate(gr,qty=8,rod=155,rph=1000,rawplatewide=2000,arqty=[1,2,3],plannum=0):  
    gm = 5 #graphic margin that allstart at this
    gblx=gr.BottomLeft[0]
    gbly=gr.BottomLeft[1]
    gw=gr.Size[0]
    gh=gr.Size[1]
    rpblx=gblx+gm
    rpbly=gbly+gm
    
    rpgw=gw-gm*2
    ratio = rpgw/rawplatewide
    rpgh=int(rph*ratio)
    ps=[]
    rod=int(rod*ratio)
    r=int(rod/2)
    ps.append(rawplatewide)
    ps.append(rph)
    font = ("Courier New", 10)
    planes =pointcircleinplane(planesize=(rpgw,rpgh),circleDiameter=rod,q=qty)
    planeview=[]
    planeview.append(planes)
    planeview.append(plannum)
    plan = planes[len(planes)-1]
    cir=plan[0]
    upl=plan[1]
    gr.DrawText(str(cir), (20, 20), font=font,color='yellow')
    upblx=rpblx
    upbly=rpbly
    upw=upl[0]
    uph=upl[1]
    
    lcm = 2
    
    
    gr.erase()  
    gr.draw_rectangle((rpblx,rpbly),(rpgw,rpgh), fill_color='dark green', line_color='yellow', line_width=2)
    gr.draw_rectangle((upblx,upbly),(upw,uph), fill_color='dark olive green', line_color='orange', line_width=3)
    crcount=0;
    for cr in cir:
        crcount+=1
        x=cr[0]+gm
        y=cr[1]+gm    
        if crcount<=arqty[0]:
            lcor = 'yellow'
            lcm=3
        elif crcount<=arqty[1]:
            lcor = 'cyan'
            lcm=4
        elif crcount<=arqty[2]:
            lcor = 'magenta'
            lcm=3
        gr.draw_circle(center_location=(x,y), radius=r, fill_color='dark blue', line_color=lcor, line_width=lcm) 
        
        print(str(cr))
    return planeview
        
def drawonrawplatenextplan(gr,qty=8,rod=155,rph=1000,rawplatewide=2000,arqty=[1,2,3]):
    plv = drawrupturescirclesinplate(gr,qty,rod,rph,rawplatewide,arqty)
    pl = plv[0]
    pn = plv[1]
    if pn>= len(pl):
        pn=0
    
    plv=drawrupturescirclesinplate(gr,qty,rod,rph,rawplatewide,arqty,plannum=pn)
    return plv