#
import FreeSimpleGUI as sg
# import dbmakeread as mkr
# from dbmakeread import *
# from working import *
# from writer import *
from tester import *
mtoitemlist=[]
ruplayer_1=['s316',0.5]
ruplayer_2=['s316',0.1]
ruplayerseal=['ptfe',0.4]
ruplayers=[ruplayer_1,ruplayer_2,ruplayerseal]
rupturelayers=[]
ruptureprojectelementformto={
    'type':'reverse',
    'size':2,
    'bp':5,
    'bt':50,
    'layers':ruplayers,
    'qty':5,
    'sensor':False,'wirecut':False , 'analysmaterial':False, 'ship':False ,'box':False ,'tag':False, 'waterjet_layser':False
    }


def rupturesettype(rtype):
    ruptureprojectelementformto.fromkeys(rbp)
def rupturebtnmto(w,v):
    print("[LOG] Clicked BTNMTOR")
    # if not isitvalidsizeofelement(v['-INPUTRNS-']):
    #     sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True)                
    #     return False
    # erroratall=8
    # datatable = ( findtownearestruptures(v['-COMBOTYPER-'],v['-INPUTRNS-'],v['-INPUTRBP-']))
    # #w['-TABLE-'].update(values=datatable.values.tolist())
    rm=[]
    m=[]
    rm.append(str(v['-COMBOTYPER-']).lower())
    rm.append(int(v['-INPUTRNS-']))
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
      
    md = makeandwritemtoforrupture(rm) 
    
    
    print("[LOG] MTO btn on rupture tab pressed!") 
    return True
    
def rupturebtnsave(w,v):
    if not isitvalidsizeofelement(v['-INPUTRNS-']):
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True)                
        return False    
    print("[LOG] Save btn on rupture tab pressed!") 
    return True
    
def rupturebtnlogo(w,v):
    print("[LOG] logo btn on rupture tab pressed!") 
    if not isitvalidsizeofelement(v['-INPUTRNS-']):
        sg.popup('its not a valid size for ruptures, please insert valid size in size input', keep_on_top=True)                
        return False  
    s= int(str(v['-INPUTRNS-']))
    r= getdimensionbysizetype(element='rupture',etype=v['-COMBOTYPER-'],esize=s)
    print(str(r))
    print("[LOG] logo btn on rupture tab pressed!")
    drawrupturesinplate(gr=w['-GRAPH-'] ,rod=r[0],qty=v['-SPINRQTY-'])
    return True
    
def holderbtnsmto(w,v):
    w['-MLINEH-'].update(str(isitvalidsizeofelement(v['-INPUTHNS-'])))
    print("[LOG] MTO on Holder tab pressed!") 
    
def holderbtnsave(w,v):
    print("[LOG] Save btn on Holder tab pressed!") 
    print("[LOG] Clicked BTNSAVEH")
    w['-MLINEH-'].update(getholdersizes(v['-COMBOTYPEH-'].lower(),v['-INPUTHNS-']))    
    
def holderbtnlogo(w,v):
    print("[LOG] logo btn on Holder tab pressed!") 
    
def exeptioninserttoguiloop():
    
    return 3
def notfoundexeptionhandler():
    print("[LOG] exeption handler Not Founded!") 
