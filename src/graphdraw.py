from calculation import *
from globalvars import *
import pandas as pd
import os


    
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




def drawrupturescirclesinplate(gr,rod=155,arqty=[1,2,3],plannum=0):  
    gm = 5 #graphic margin that allstart at this
    gblx=gr.BottomLeft[0]
    gbly=gr.BottomLeft[1]
    gw=gr.Size[0]-gm*2
    gh=gr.Size[1]-gm*2
    rpblx=gblx+gm
    rpbly=gbly+gm
    
        
    
    ratio = gw/rupturerawplateheightmm
    rpgh=int(rupturerawplatewidthmm*ratio)
    rpgw=int(rupturerawplateheightmm*ratio)
    rod=int(rod*ratio)
    r=int(rod/2)
    font = ("Courier New", 10)
    qty =arqty[0]+arqty[1]+arqty[2]
    planes =pointcircleinplane(planesize=(rpgw,rpgh),circleDiameter=rod,q=qty)
    plan = planes[len(planes)-1]
    cir=plan[0]
    upl=plan[1]
    
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
        elif crcount<=arqty[0]+arqty[1]:
            lcor = 'cyan'
            lcm=3
        elif crcount<=arqty[0]+arqty[1]+arqty[2]:
            lcor = 'magenta'
            lcm=3
        gr.draw_circle(center_location=(x,y), radius=r, fill_color='dark blue', line_color=lcor, line_width=lcm) 
        TEXT_LOCATION = (x-r/2, y-r/4)
        TEXT_COLOR = 'white'        
        gr.draw_text(f'{crcount}', TEXT_LOCATION, font='Courier', color=lcor)
        print(str(cr))
    return planes
        
def drawonrawplatenextplan(gr,rod=155,arqty=[1,2,3]):
    qty = arqty[0]+arqty[1]+arqty[2]
    plv = drawrupturescirclesinplate(gr,rod,arqty)
    pl = plv[0]
    pn = plv[1]
    if pn>= len(pl):
        pn=0
    
    plv=drawrupturescirclesinplate(gr,rod,arqty,plannum=pn)
    return plv