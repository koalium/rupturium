from globalvars import *
from filehandler import *
from calculation import *
import pandas as pd
import os

def rupturediskthicknessfinder(ruptprop=ruptomtodef):
    rtype =ruptprop[0]
    rsize=ruptprop[1]
    rbp=ruptprop[2]
    rbt=ruptprop[3]
    lm1= ruptprop[4]
    data = findneardesignedruptureperv(rtype,rsize,rbp)
    lm=[]
    lt=[]
    ll=[]
    layers=[]
    if len(data>0):
        layers=data[0]
    for l in layers:
        lm.append( l[0])
        
        lt.append( l[1])
    return layers


def makeandwritemtoforrupture(ruptomto=ruptomtodef):
       
    SHW=rupturerawplatewidthmm
    SHH =rupturerawplateheightmm
    TSHW=rupturesealrolewidthmm
    rtype =ruptomto[0]
    rsize=ruptomto[1]
    rbp=ruptomto[2]
    rbt=ruptomto[3]
    lm1= ruptomto[4]
    qtyi= ruptomto[5]
    qty=qtyi[0]+qtyi[1]+qtyi[2]
    sensor_=ruptomto[6]
    sensor=sensor_[0]
    wirecut=ruptomto[7]
    analysmat_=ruptomto[8]
    analysmat=analysmat_[0]
    ship=ruptomto[9]
    box=ruptomto[10]
    tag=ruptomto[11]
    water_laser=ruptomto[12]
    holders= ruptomto[13]
    matpricesheet=ruptomto[14]
    matpriceshaft=ruptomto[15]
    matpticeperkg=matpricesheet[0]
    holdtype = holders[0]
    holdsize = holders[1]
    holdmat = holders[2]
    holdqty =  holders[3]
    gasket = holders[4]
    holderadded=holders[5]
    mtoh = getreadmtoheader()
    mtoit = getreadmtoitemorop('rupture')
    data = findneardesignedruptureperv(rtype,rsize,rbp)
    ename = ''
    indexconter=0
    mtorows=[]
    mtro=[]
    eprppmat = ''
    if len(data)==0:
        return eprppmat
    laym=[]
    layers=data[0]
    
    seallayerfounded=False
    layercounter=0
    ruprawdia = getdimensionbysizetype('rupture',rtype,rsize)
    rawsheetmaindim = calcrawsheetforruptures(ruprawdia,qty,SHW,SHH)  
    rawsheetmsealdim = calcrawsheetforruptures(ruprawdia,qty,rawsheetwideseallayer,rawsheetheightseallayer)  
    for l in layers:
        ename=''
        eprppmat=''        
        isitseallayer=False
        lt = l[1]
        ename = ''
        en = mtoit[0]
        nn = en[0]
        rawsheetdim=rawsheetmaindim
        en = mtoit[0]
        SHW = rupturerawplatewidthmm
        SHH = rupturerawplateheightmm    
        lm = l[0]
        if lm.find('pt')>-1 or lm.find('pv')>-1 or lm.find('pl')>-1 or lm.find('tef')>-1 or lm.find('fep')>-1 :
            lm = lm1[2]
            en = mtoit[1]
            SHW = rawsheetwideseallayer
            SHH = rawsheetheightseallayer
            rawsheetdim=rawsheetmsealdim
            matpticeperkg = matpricesheet[2]
        else:
            lm = lm1[layercounter]
            matpticeperkg = matpricesheet[layercounter]
            if layercounter==0:
                layercounter=1
                  
            
        nn = en[0]       
        enameln = str(nn[1])
        ename = ename.__add__(enameln)    
        ename = ename.__add__(" ")
        ename = ename.__add__(str(getmaterialnamefa(lm)))
             
        
        eprppmat=ename
        eprppmat=eprppmat.__add__(' , Thickness: ')
        eprppmat=eprppmat.__add__(str(lt))
        eprppmat=eprppmat.__add__(' mm  , Dim: ')
        eprppmat=eprppmat.__add__(str(rawsheetdim[1]))
        eprppmat=eprppmat.__add__(' * ')
        eprppmat=eprppmat.__add__(str(rawsheetdim[0]))
        eprppmat=eprppmat.__add__(' mm ')
        
        area = squararia(rawsheetdim[0],rawsheetdim[1])*(rawsheetdim[2]+1)
        vol = volumeofarea(area,lt)
        dens = float(getdensityofmaterial(lm))
        
        
        msslayer = massofvolumeofmaterial(vol,dens)
         
        mtro=[]
        indexconter+=1
        mtro.append(indexconter)
        mtro.append(ename)
        mtro.append(eprppmat)
        mtro.append(str(rawsheetdim[2]+1))
        unitpprice = en[1]#getunitpriceformtoitem(mtoit,1)
        mtro.append(unitpprice[0])
        mtro.append(str(round(msslayer,2)))
        matpriceunit = float(matpticeperkg)#float(getpriceofmaterialkg(lm))
        mtro.append(matpriceunit)
        matprice = calcpricebymass(matpriceunit,msslayer)
        mtro.append(matprice)
        
            
        mtorows.append(mtro)       
    
    
    Q=1
    eprppmat=" "
    
    
    if holderadded==True and holders[3]>0:
        
        indexconter+=1
        mtorows.append(makemtorowsforholders(indexconter,holders)[0])
        mtorows.append(makemtorowsforholders(indexconter,holders)[1])
        if holders[4]==True:
            pass
        indexconter+=1
    
        
    if analysmat==True:
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,3,analysmat_[1],indexconter))
        
    if water_laser==True:
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,5,1,indexconter))
   
    if sensor==True:
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,15,sensor_[1],indexconter))
        
    if wirecut==True:
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,4,1,indexconter))
   
        
    #if tag==True:
        #indexconter+=1
        #mtorows.append(anotherselementofmto(mtoit,7,1,indexconter))
        
    if box==True:
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,11,1,indexconter))
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,12,1,indexconter))
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,13,1,indexconter))
       
    if ship==True:
        indexconter+=1
        mtorows.append(anotherselementofmto(mtoit,14,1,indexconter))
        
    mtorows.append(["","","","","","","Total Price",f'=SUM(H3:H{indexconter+2})'])
    df1 = pd.DataFrame(mtorows,columns=mtoh)  
    if len(holders)<3:
        holders=['reverse',2,0,'s316']
    
    mtoTitle=mtotabletitle(p='101',t=rtype,s=rsize,bp=rbp,tb=rbt,qb=qtyi[0],hq=holders[3])
    ffxn = getmyfilename(rt=rtype,rs=rsize,rb=rbp,rq=qty)
    return writedataframedstylishtofile(df1,ffxn,mtoTitle)


def mtotabletitle(p='101',t='reverse',s=4,bp=5.7,tb=35,qb=11,hq=0):
    mtil = "Project ".__add__(str(p)).__add__('.. Rupture Disks: type=').__add__(t).__add__(' , Size=').__add__(str(s)).__add__(' inches, Burst Pressure:').__add__(str(bp)).__add__(' Barg,  Burst Temorature=').__add__(str(tb)).__add__(' C, Qty=').__add__(str(qb))
    if hq >0:
        mtil.__add__(' , Holder QTY:').__add__(str(hq))     
    return mtil
   
def makerowoftableofmto(index=1,name='sheet',prp='dimension',q='1',unit='meter',mass='_',unitprice='400000',price='5000000'):
    row=[]
    row.append(name)
    row.append(prp)
    row.append(q)
    row.append(unit)
    row.append(str(round(mass,2)))
    row.append(unitprice)
    if  len(mass) and mass[-1] in ('0123456789.'):
        price = float(mass)*float(q)*float(unitprice)
    else:
        price = float(q)*float(unitprice)
    row.append(int(price))
    return row
    
    
def anotherselementofmto(mtoit,itnum=4,qty=1,i=4):
      
    ow=[]
    en = mtoit[itnum]
    nn = en[0]        
    enameln = str(nn[1])
    ow.append(i) 
    ow.append(enameln)      
    ow.append(" ")
    ow.append(str(qty))
    mm= en[1] 
    #ow.append('-')
    ow.append(mm[0])
    ow.append("-")
    ow.append(mm[1])
    tp = float(mm[1])*qty
    ow.append(str(int(tp)))
    return ow 

def makemtorowsforholder(i=1,holderprop=['reverse',2,'s316',1],side='ps'):#i=1,htype='reverse',hsize=2,qty=2,material='s316',side='ps'):
    
    
    htype=holderprop[0]
    hsize=holderprop[1]
    
    material=holderprop[2]
    qty=holderprop[3]
    htype=htype.lower()
    hdim=getdimensionbysizetype(element='holder',etype=htype,esize=hsize)
    
    psth=hdim[4]
    vsth=hdim[5]
    sod = findingneareststandardshaftforholder(htype=htype.lower(),hsize=hsize)
    if side=='vs':
        thickness=vsth
        
    else:
        thickness=psth
    harea = circarea(sod)
    hden = float(getdensityofmaterial(material)   )
    
    roundedth=roundshaftlengthformachinery(thickness)
    shaftvol = volumeofarea(harea,roundedth)
    smass = massofvolumeofmaterial(shaftvol,hden)
    
    
    matnamefa = getmaterialnamefa(material)
    
    mtoit = getreadmtoitemorop('holder')
    
    ename = ''
    
    mtorows=[]
    mtro=[]
    eprppmat = ''
    
    ename = ''
    en = mtoit[1]
    if side == 'vs':
        en=mtoit[0]
    
    nn = en[0]
    enameln = str(nn[1])
    ename = ename.__add__(enameln)    
    
    
    
    
    eprppmat=str(nn[1])
    eprppmat=eprppmat.__add__(' ')
    eprppmat=eprppmat.__add__(matnamefa)
    
    eprppmat=eprppmat.__add__(' , OD: ')
    eprppmat=eprppmat.__add__(str(sod))
    eprppmat=eprppmat.__add__(' mm  , len: ')
    
    eprppmat=eprppmat.__add__(str(roundedth))
    eprppmat=eprppmat.__add__(' mm , each mass: ')
    eprppmat=eprppmat.__add__(str(round(smass,2)))
    eprppmat=eprppmat.__add__(' Kg')
    tsmass=smass*qty
     
    mtro=[]
    
    mtro.append(i)
    mtro.append(ename)
    mtro.append(eprppmat)
    mtro.append(qty)
    #unitpprice = en#getunitpriceformtoitem(mtoit,1)
    unitpprice = en[1]
    mtro.append(unitpprice[0])
    mtro.append(str(round(smass,2)))
    matpriceunit = float(getpriceofmaterialkg(material))
    mtro.append(str(int(matpriceunit)))
    matprice = int(calcpricebymass(matpriceunit,tsmass))
    mtro.append(str(int(matprice)))
    
        
    mtorows.append(mtro)    
    return mtro



    
def makemtorowsforholders(i=1,hp=[1,'reverse',2,2,'s316']):
    holders = []
    holders.append(makemtorowsforholder(i,hp,'ps'))
    holders.append(makemtorowsforholder(i+1,hp,'vs'))
    return holders
    
