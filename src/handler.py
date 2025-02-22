#
import FreeSimpleGUI as sg

from graphdraw import *
from mtomaker import *



def rupturebtnmto(w,v):
    
    
    print("[LOG] Clicked BTNMTOR")
    if len(getdimensionbysizetype(element='rupture',etype=str(v['-COMBOTYPER-']).lower(),esize=v['-INPUTRNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return        
    notvalidsizeexeption(v['-INPUTRNS-'])
    rm=[]
    m=[]
    rm.append(str(v['-COMBOTYPER-']).lower())
    rm.append(float(v['-INPUTRNS-']))
    rm.append(int(v['-INPUTRBP-']))
    rm.append(int(v['-INPUTRBT-']))
    m.append(str(v['-COMBOMAINMATERIALR-']))
    m.append(str(v['-COMBOSUBATERIALR-']))
    m.append(str(v['-COMBOSEALMATERIALR-']))
    rm.append(m)
    rqt=[]
    overqtydes = calcoverneedruptureqtyfordesign(str(v['-COMBOTYPER-']).lower(),float(v['-INPUTRNS-']))
    rqt.append(v['-SPINRQTY-'])
    rqt.append(overqtydes)
    overqtystandard = getoverqtyrupturefortest(int(v['-SPINRQTY-']))
    rqt.append(overqtystandard)
    rawmatqty = overqtystandard + overqtydes
    rm.append(rqt)
    sens=[]
    sens.append(bool(v['-CBSENR-']))
    if sens[0]:
        sens.append(int(v['-SPINRSNSQTY-'])) 
    else:
        sens.append(0)
    rm.append(sens)
    rm.append(bool(v['-CBWRCR-']))   
    anmat=[]
    anmat.append(bool(v['-CBANMR-']))
    if anmat[0]:
        anmat.append(int(v['-SPINMAQTY-'])) 
    else:
        anmat.append(0)
    
    rm.append(anmat)
    rm.append(bool(v['-CBSHPR-']))
    rm.append(bool(v['-CBBXGR-']))
    rm.append(bool(v['-CBTAGR-']))
    rm.append(bool(v['-CBWJLR-']))
    h=[]
    h.append(str(v['-COMBOTYPER-']))  
    h.append(float(v['-INPUTRNS-']))
    h.append(str(v['-COMBOMAINMATERIALRH-']))  
    h.append(int(v['-SPINRHQTY-']))  
    h.append(bool(v['-CBGKTRH-']))  
    h.append(bool(v['-CBBHLDR-']))  
    
    rm.append(h)
    md = makeandwritemtoforrupture(rm) 
    
    
    print("[LOG] MTO btn on rupture tab pressed!") 
    return True
    
def rupturebtnsave(w,v):
     
    print("[LOG] Save btn on rupture tab pressed!") 
    if len(getdimensionbysizetype(element='rupture',etype=str(v['-COMBOTYPER-']).lower(),esize=v['-INPUTRNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    return True
    
def rupturebtnlogo(w,v):
    print("[LOG] logo btn on rupture tab pressed!") 
    if len(getdimensionbysizetype(element='rupture',etype=str(v['-COMBOTYPER-']).lower(),esize=v['-INPUTRNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    s= (v['-INPUTRNS-'])
    r= getdimensionbysizetype(element='rupture',etype=v['-COMBOTYPER-'],esize=s)
    if len(r)==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    print("[LOG] logo btn on rupture tab pressed!")
    arqt= getruptureqtyrawmaterial(qty=int(v['-SPINRQTY-']),rtype=str(v['-COMBOTYPER-']).lower(),rsize=float(v['-INPUTRNS-']))
    
    drawrupturescirclesinplate(gr=w['-GRAPH-'] ,rod=r[0],arqty=arqt)

def rupturegraphnext(w,v):
    print("[LOG] Next on graph rupture tab pressed!") 
    if len(getdimensionbysizetype(element='rupture',etype=str(v['-COMBOTYPER-']).lower(),esize=v['-INPUTRNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    s= (v['-INPUTRNS-'])
    r= getdimensionbysizetype(element='rupture',etype=v['-COMBOTYPER-'],esize=s)
    if len(r)==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    print("[LOG] logo btn on rupture tab pressed!")
    arqt= getruptureqtyrawmaterial(qty=int(v['-SPINRQTY-']),rtype=str(v['-COMBOTYPER-']).lower(),rsize=float(v['-INPUTRNS-']))
    
    drawrupturescirclesinplate(gr=w['-GRAPH-'] ,rod=r[0],arqty=arqt)
    
    

def rupturegraphprev(w,v):
    print("[LOG] Next on graph rupture tab pressed!") 
    if len(getdimensionbysizetype(element='rupture',etype=str(v['-COMBOTYPER-']).lower(),esize=v['-INPUTRNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    s= (v['-INPUTRNS-'])
    r= getdimensionbysizetype(element='rupture',etype=v['-COMBOTYPER-'],esize=s)
    if len(r)==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    print("[LOG] logo btn on rupture tab pressed!")
    arqt= getruptureqtyrawmaterial(qty=int(v['-SPINRQTY-']),rtype=str(v['-COMBOTYPER-']).lower(),rsize=float(v['-INPUTRNS-']))
    drawrupturescirclesinplate(gr=w['-GRAPH-'] ,rod=r[0],arqty=arqt,plannum=-1)

def holderbtnsmto(w,v):
    print("[LOG] mto btn on holder tab pressed!") 
    if len(getdimensionbysizetype(element='holder',etype=str(v['-COMBOTYPEH-']).lower(),esize=v['-INPUTHNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
   
    holdersprop=getuserinterholder(w,v)
    w['-MLINEH-'].update(str(makemtorowsforholders(1,holdersprop)))
    
    
    
def holderbtnsave(w,v):
    print("[LOG] save btn on holder tab pressed!") 
    if len(getdimensionbysizetype(element='holder',etype=str(v['-COMBOTYPEH-']).lower(),esize=v['-INPUTHNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    
    
    
    
def holderbtnlogo(w,v):
    print("[LOG] logo btn on holder tab pressed!") 
    if len(getdimensionbysizetype(element='holder',etype=str(v['-COMBOTYPEH-']).lower(),esize=v['-INPUTHNS-']))==0:
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True) 
        return 
    

def notvalidsizeexeption(elementsize=2,elementname='rupture',elementtype='reverse'):
    ed=getdimensionbysizetype(element=elementname.lower(),etype=elementtype.lower(),esize=elementsize)
    if len(ed)==0:
        sg.popup(f'{elementsize} not a valid size for {elementname} as {elementtype}, please insert valid size in size input', keep_on_top=True)  
        ed=[0,0,0,0,0,0,0,0]
        return False 

def getuserinterholder(w,v):
    h=[]
    h.append(str(v['-COMBOTYPEH-']))  
    h.append(float(v['-INPUTHNS-']))
    h.append(str(v['-COMBOMAINMATERIALRH-']))
    h.append(int(v['-SPINHQTY-']))  
    h.append(bool(v['-CBGKTH-']))  
    h.append(bool(v['-CBBHLDR-']))  
    return h
    
def getuserinterrupture(w,v):
    rm=[]
    m=[]
    rm.append(str(v['-COMBOTYPER-']).lower())
    rm.append(float(v['-INPUTRNS-']))
    rm.append(int(v['-INPUTRBP-']))
    rm.append(int(v['-INPUTRBT-']))
    m.append(str(v['-COMBOMAINMATERIALR-']))
    m.append(str(v['-COMBOSUBATERIALR-']))
    m.append(str(v['-COMBOSEALMATERIALR-']))
    rm.append(m)
    rm.append(int(v['-SPINRQTY-']))
    rm.append(bool(v['-CBSENR-']))
    rm.append(bool(v['-CBWRCR-']))    
    rm.append(bool(v['-CBANMR-']))
    rm.append(bool(v['-CBSHPR-']))
    rm.append(bool(v['-CBBXGR-']))
    rm.append(bool(v['-CBTAGR-']))
    rm.append(bool(v['-CBWJLR-']))
    
    rm.append(getuserinterholder(w,v))
    return rm