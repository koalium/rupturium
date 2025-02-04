import pandas as pd
from string import *
from working import *
import os
from writer import *
from tester import *
mtotitle = ["MTO","IR254","kimiadaran kavir","Rupture Disk 20 inch Burst pressure = 0.4 Barg , Berst Temprature = 50 C , QTY = 2"," Vaccum Support"]
mtoheader = ["index","element","properties","qty","unit","mass of unit","price of ech","Price"]
default_dbfilename = 'mainDB_.xlsx'
dbfileparh = ''
dbfilename = dbfileparh + default_dbfilename
writefilepathdefault = './'
writefilename = 'outetfile.xlsx'
writefileexcelpath= writefilepathdefault
writefileexcel = writefileexcelpath+writefilename
dbburstpressure = 'bp'
dbbursttemprature = 'bt'
rupstr = 'rupture'
rupqtystr = 'rptrqty'
elementtypestr ='type'
reverserupturesheetname = 'reverse'
forwardrupturesheetname = 'forward'
flatrupturesheetname = 'flat'
materialsheetname = 'material'
worksheetname = 'work'
holdersheetname = 'holder'
holderelementstr = 'holder'
rawsizesheet = 'size'
testsheetname='test'
mtosheet = 'mto'
thicknessstrhedear='thickness'

ruplasermargin=5
rupturerawplatewidthmm=2000
rupturelasermargin=5
findres =[]
findsize=[]
feetres=[]
mto = []
mainto=[]
rupturemakeerrorpercentage=8

def setwritefilepath(p):
    writefileexcelpath = str(p)
def getwritefilepath():
    return writefileexcelpath

def getwritefileexcel():
    return (writefileexcelpath.__add__(writefilename))

def getdbfile():
    return (dbfileparh+default_dbfilename)


    
def getruptureodbysizetype(rtype,rsize):
    plate=[]
    hsheet = pd.read_excel(dbfilename, sheet_name =str(rawsizesheet.lower()), index_col=None, header=0)
    details = pd.DataFrame(hsheet)
    mask_var = (details['element'] == rupstr) and (details[rawsizesheet] == rsize) 
    els = details[mask_var]   
    squarwidth = float(els.iloc[0, els.columns.get_loc('od')])
    
    return squarwidth
    
def getruptureqtyfromstandard(ruptureqty):
    plate=[]
    hsheet = pd.read_excel(dbfilename, sheet_name =str(testsheetname.lower()), index_col=None, header=0)
    frpr = pd.DataFrame(hsheet)
    frpr = frpr[frpr['from']<= ruptureqty ]
    frpr = frpr[frpr['to']>= int(ruptureqty) ]
    minqty = float(frpr.iloc[0, frpr.columns.get_loc('min')])
    tqty = max(int(minqty),int(ruptureqty*frpr.iloc[0, frpr.columns.get_loc('ratio')]))
    return tqty
    
def getruptureqtyfordesign(rbp,frpr):
    nrp = nearestruptureburstpressure(rbp,frpr,1)
    if nrp[dbburstpressure] == rbp :
        return 1
    elif (nrp[dbburstpressure] - rbp).abs() <2:
        return 2
    else:
        return 3
    
def calctotalqtyruptures(rqty):
    return (getruptureqtyfromstandard(rqty)+rqty+2)

def getruptureqtystimating(rqty,epercent):
    totalqty = calctotalqtyruptures(rqty)*(1+epercent/100)
    if totalqty-int(totalqty)>=0.44:
        totalqty=int(totalqty)+1
    else : 
        totalqty = int(totalqty)
    return totalqty
        
def circarea(d):
    d = float(str(d))*0.001
    a = 3.14*d*d
    return a

def squararia(w,l):
    return w*0.001*l*0.001;

def volumeofarea(a,l):
    return a*l*0.001

def cylindrevol(od,tickness):
    return volumeofarea(circarea(od),tickness)

def centreemptycylindrevol(rod,rid,rt):
    a=circarea(rod)-circarea(rid)
    return volumeofarea(a,rt)

def massofvolumeofmaterial(vol,den):
    m = vol*den*1000
    return m

def calcpricebymass(mass,ppm):
    return mass*ppm


def getsizerawmatforelement(element,etype,esize):
    hsheet = pd.read_excel(dbfilename, sheet_name =str(rawsizesheet.lower()), index_col=None, header=0)
    details = pd.DataFrame(hsheet)
    mask_var = details['element'] == element.lower()
    els = details[mask_var]   
    mask_var = details['size'] == float(esize)
    els = els[mask_var] 
    mask_var = details['type'] == str(etype).lower()
    els = els[mask_var]     
    size=[]
    if element.find('hol')>-1:
        squarwidth = float(els.iloc[0, els.columns.get_loc('od')])
        size.append(float(els.iloc[0, els.columns.get_loc('od')]))
        size.append(float(els.iloc[0, els.columns.get_loc('len')]))
        size.append(float(els.iloc[0, els.columns.get_loc('id')]))
    elif element.find('rup')>-1:
        size.append(float(els.iloc[0, els.columns.get_loc('od')]))
    elif element.find('tag')>-1:
        size.append(float(els.iloc[0, els.columns.get_loc('width')]))
        size.append(float(els.iloc[0, els.columns.get_loc('height')]))
        size.append(float(els.iloc[0, els.columns.get_loc('thickness')]))
        
    
    return size
    
def getmaterialdensity(mat):
    mat=str(mat)
    if len(mat)>2:
        mat = mat[0:3]
    else:
        return 101
    hsheet = pd.read_excel(dbfilename, sheet_name =str(materialsheetname.lower()), index_col=None, header=0)
    df = pd.DataFrame(hsheet)
    df = df[df['mmatn'] == mat ] 
    den = float(df.iloc[0, df.columns.get_loc('density')]) 
    return den

def getmaterialpriceunit(mat):
    mat=str(mat)
    if len(mat)>2:
        mat = mat[0:3]    
    hsheet = pd.read_excel(dbfilename, sheet_name =str(materialsheetname.lower()), index_col=None, header=0)
    df = pd.DataFrame(hsheet)
    df = df[df['mmatn'] == mat ] 
    priceunit = float(df.iloc[0, df.columns.get_loc('priceunit')])
    return priceunit

def getmaterialnamefarsi(mat):
    mat=str(mat)
    mat.removeprefix(' ')
    if len(mat)>2:
        mat = mat[0:3]    
        
    hsheet = pd.read_excel(dbfilename, sheet_name =str(materialsheetname.lower()))
    df = pd.DataFrame(hsheet)
    df = df[df['mmatn'] == mat ] 
    fm='fool'
    if len(df.values.tolist())>0:
        fm = str(df.iloc[0, df.columns.get_loc('mainmatfarsi')]) 
    
    return fm
    
def isitvalidsizeofelement(esize):
    hsheet = pd.read_excel(dbfilename, sheet_name =str(rawsizesheet.lower()), index_col=None, header=0)
    details = pd.DataFrame(hsheet)
    mask_var = details['size'] == float(esize)
    els = details[mask_var]   
    if els.values.tolist().__len__() >0:
        return True
    return False

def getholdersizes(etype,esize):
    hs = getsizerawmatforelement('holder',etype,esize)
    return hs
    
def getholdermass(htype,hsize,material,qty):
    hres=[]
    hs = getsizerawmatforelement('holder',htype,hsize)
    hod = hs[0]/10
    hsl = hs[1]/10
    hid = hs[2]/10
    holderrawmatvol = cylindrevol(hod,hsl)
    holdervol = centreemptycylindrevol(hod,hid,hsl)
    dens = getmaterialdensity(material.lower())    
    rawmass = massofvolumeofmaterial(holderrawmatvol,dens)
    holmass = massofvolumeofmaterial(holdervol,dens)
    hres.append(['each holder shaft Lenght (cm)',hsl])
    hres.append(['total shaft Lenght (cm)',hsl*qty])
    hres.append(['shaft OD (cm)',hod])
    hres.append(['Each holder shaft Mass (kg)',rawmass])
    hres.append(['Each holde Mass (kg)',holmass])
    hres.append(['raw mat shaft mass Mass (kg)',rawmass*qty])
    hres.append(['holders Mass (kg)',holmass*qty])    
    return hres
    
    
def btnmtoholderpress(htype,hsize,material,qty):
    hres=[]
    hol=getholdershaftodlnid(htype,hsize)
    hres.append(['shaft Lenght (mm)',hol[1]])
    hres.append(['shaft OD (mm)',hol[0]])
    holderrawmatvol = cylindrevol(hol[0]/10,hol[1]/10)
    holdervol = centreemptycylindrevol(hol[0]/10,float(hsize)*2.54/10,hol[1]*qty/10)
    dens = getmaterialdensity(material.lower())
    hres.append(['shaft Mass (kg)',massofvolumeofmaterial(holderrawmatvol,dens)])
    hres.append(['Ring Mass (kg)',massofvolumeofmaterial(holdervol,dens)])
    return hres

def readjustthisrowsofsheetoffile(sheet,thisrowscellvalue):
    details = pd.DataFrame(sheet)    
    mask_var = details[rawsizesheet] == thisrowscellvalue
    return details[mask_var]   

def readthissheetofdbfilke(sheetname):
    return pd.read_excel(dbfilename, sheet_name =str(sheetname.lower()), index_col=None, header=0)
    
def getholdershaftodlnid(htype,hsize):

    
    els = readjustthisrowsofsheetoffile(readthissheetofdbfilke(holdersheetname),float(hsize))
    hod = 0
    hid=0
    hsl = 0
    hs=[]
    if htype.lower()==reverserupturesheetname:
        hs.append(float(els.iloc[0, els.columns.get_loc('rod')]))
        hs.append(float(els.iloc[0, els.columns.get_loc('rid')]))
        hs.append(float(els.iloc[0, els.columns.get_loc('rwst')]))
        hs.append(float(els.iloc[0, els.columns.get_loc('rwsod')]))
        
        #hod = fhldr['rod']
        #hid = fhldr['rid']
        #hsl = fhldr['rwst']
        #hsod = fhldr['rwsod']
    else:
        hs.append(float(els.iloc[0, els.columns.get_loc('fod')]))
        hs.append(float(els.iloc[0, els.columns.get_loc('fid')]))
        hs.append(float(els.iloc[0, els.columns.get_loc('fwst')]))
        hs.append(float(els.iloc[0, els.columns.get_loc('fwsod')]))        
        #hod = fhldr['fod']
        #hid = fhldr['fid']
        #hsl = fhldr['fwst']
        #hsod = fhldr['fwsod']

    
    hs.append(float(hod))
    hs.append(float(hsl))
    hs.append(float(hid))
    return hs


    
    

def getnearruptureofwanted(rsize,rtype,rbp,n):
    nearestruptureburstpressure(rbp,getrupturebysizetype(rsize,rtype),n)
    if len(nearestruptureburstpressure)==0:
        return [1,1,1,1,1,1,1,1]
    return nearestruptureburstpressure

def getrupturebysizetype(rsize,rtype):
    hsheet = pd.read_excel(dbfilename.lower(), sheet_name =str(rtype).lower(), index_col=None, header=0)
    details = pd.DataFrame(hsheet)
    mask_var = details[rawsizesheet] == float(rsize) 
    frpr = details[mask_var]  
    
    return frpr

def nearestruptureburstpressure(rbp,frpr,n):
    df_closest = frpr.iloc[(frpr[dbburstpressure]-float(rbp)).abs().argsort()[:n]]
    return df_closest
    
def getrupturematerialdimensions(rtype,rsize,rbp):
    
    return getseperatedbydashes(rtype,rsize,rbp)

def dashed(s):
    return s.find('-')

def getseperatedbydashes(rtype,rsize,rbp):
    
    rp = findtownearestruptures(rtype,rsize,rbp).values.tolist()
    if len(rp)<1:
        return
    mrp = str(rp[0][0])
    trp = str(rp[0][1])

    
    
    
    m=[]
    while True:
        
        r=[]
        mc = dashed(mrp)
        tc= dashed(trp)
        if mc>0:
            r.append(mrp[0:mc])
            mrp=mrp[mc+1:len(mrp)]
            if tc>0:
                r.append(trp[0:tc])
                trp=trp[tc+1:len(trp)]
            else:
                r.append(trp)
            m.append(r)
        elif tc>0:
            r.append(mrp)
            r.append(trp[0:tc])
            trp=trp[tc+1:len(trp)]
            m.append(r)
        else:
            r.append(mrp)
            r.append(trp)
            m.append(r)
            return m

        
    
def findtownearestruptures(rtype,rsize,rbp):
    
    rprs = getrupturebysizetype(rsize,rtype)
    nnearrup = nearestruptureburstpressure(rbp,rprs,2)
    
    return nnearrup
    
def addtobuffer(buff,element,index):
    touched = 0
    resbuff = []
    if buff.__len__() ==0:
        buff.append(element)
        return buff
    v = float(str(element[index]))
    for i in range(buff.__len__()):
        f = float(str(buff[i][index]))
        if touched==0 and (v>f):
            resbuff.append(element)
            touched=1
        
        resbuff.append(buff[i])
    
    return resbuff


            
            
        

       
#make a list of materials
def mylister(filename,sheetname,colname):
    
    sh = pd.read_excel(dbfilename.lower(), sheet_name =sheetname.lower())
    mr=[]
    for s in sh[str(colname).lower()]:
        mr.append(str(s))
    
    return mr
   

            
  
def readjustrowsofsheetoffileatcolvalues(sheet,thisrowscellvalue,colname):
    details = pd.DataFrame(sheet)    
    mask_var = details[colname] == thisrowscellvalue
    return details[mask_var]         
        
def structmakinerfromexcel(sn):
    dbfilename='mainDB_.xlsx'
    hsheet = pd.read_excel(dbfilename, sheet_name =str(sn.lower()), index_col=None, header=0)
    df = pd.DataFrame(hsheet)    
    data=[]
    r=[]
    s=[]
    for row in df.itertuples():
        r = row[1:]  # Skip the index
        data.append(r)
    return data    

def findmaterialifpredefined(mat):
    data = structmakinerfromexcel('material')
    m = str(mat).lower()
    if len(m)>3:
        m=m[0:3]
        
    
    for d in data:
        s=str(d[2]).lower()
        if len(s)>2:
            s=s[0:3]
        
        if s==m:
            return d
    ndd=[]
    ndd.append(0)
    ndd.append(str(mat))
    ndd.append(mat)
    ndd.append(mat)
    ndd.append(5)
    ndd.append(5000000)
    return ndd

def getmaterialnamefa(mat):
    mf = findmaterialifpredefined(mat)
    return str(mf[3])


def getrupturelayers(rtype):
    data = structmakinerfromexcel(rtype)
    dd=[]
    r=[]
    mr=[]
    m=[]
    for d in data:
        r=[]
        mr=[]
        for i in range(5):
            m=[]
            if not pd.isna(d[3+i*2]):
                m=[]
                m.append(d[3+i*2])
                m.append(d[3+1+i*2])
                mr.append(m)
        r.append(mr)        
        m=[]
        m.append(d[13])
        m.append(d[14])
        m.append(d[15])
        r.append(m)
        m=[]
        m.append(d[2])
        m.append(d[16])
        m.append(d[17])        
        r.append(m)
        dd.append(r)
    return dd 

        
            
    
def mtomakerofrupturedisks(rtype,rsize,rmmat,sealmat,rsmat,rbp,rbt,qty,sns,wrc,err,anm,shp,bxg,tag,wtl):
    rdfs= readthissheetofdbfilke('mto')
    rdfs = rdfs[rdfs['element']=='mtoheader']
    temple_mto_header_farsi = rdfs['itemf'].values.tolist()
    rdfs= readthissheetofdbfilke('mto')
    rdfs = rdfs[rdfs['element']=='rupture']
    rupelfarsi = rdfs['itemf'].values.tolist()
    start_price_at = rdfs['pr'].values.tolist()    
    unit_of_item =  rdfs['unitf'].values.tolist()   
    mtomainheader=[" "," "," "," "," "," "," "," "]
    df=[]
    indexconter=0
    indexes=8
    
    mat = getseperatedbydashes(rtype,rsize,rbp)
    matnum = len(mat)
    tcol=[]
    rt=[]
    for m in mat:
        indexconter+=1
        
        rrow=[]
        ename=""
        eprop=""
        prop=[]
        tcol=[]
        mmat = str(m).lower()
        if mmat.find('pt')>-1 or mmat.find('pv')>-1 or mmat.find('te')>-1 or mmat.find('fe')>-1 :
            continue
        if indexconter==1:
            mmat=rmmat
        elif indexconter==matnum:
            mmat=rsmat
        mmat3 = mmat.lower()
        if len(mmat)>3:
            mmat3 = mmat[0:3].lower()
        else:
            mmat3='s31'
        print(mmat)
        matfarsiname = getmaterialnamefarsi(mmat3)
        
        tcol.append(str(rupelfarsi[0]).__add__(" ").__add__(matfarsiname))
        ename = ename.__add__(str(rupelfarsi[0]))
        ename = ename.__add__(" ")
        ename = ename.__add__(str(matfarsiname))
        rrow.append(indexconter)
        rrow.append(ename)
        
        eprop = ename
        eprop = eprop.__add__(" , thickness: ")
        eprop = eprop.__add__(str(m[1]))
        eprop = eprop.__add__(" mm , size: ")
        rawmatsw= getsizerawmatforelement('rupture',rtype,rsize)
        rswide=1000
        rawdim = getrawsheetmatdimension(rawmatsw[0],qty,rswide)
        matthick = float(m[1])
        matwidth = float(rawdim[0])
        matlen = float(rawdim[1])
        matden = float(getmaterialdensity(mmat3))
        matmass = massofmaterialfromdimensionmm(matthick,matwidth,matlen,matden)
        
        eprop = eprop.__add__(str(int(rawdim[0])))
        eprop = eprop.__add__(" * ")
        eprop = eprop.__add__(str(int(rawdim[1])))
        eprop = eprop.__add__(" mm ")
        
        rrow.append(eprop)
        rrow.append(1)
        rrow.append(unit_of_item[1])
        rrow.append(matmass)
        matpriceunit = getmaterialpriceunit(mmat3)
        rrow.append(matpriceunit)
        
        rrow.append(matmass*matpriceunit)
        
        rt.append(rrow)
    
    indexconter+=1
    rrow=[]
    ename=""
    eprop=""
    prop=[]
    tcol=[]
    mmat3 = sealmat
    if len(mmat)>3:
        mmat3 = sealmat[0:3]
    matfarsiname = getmaterialnamefarsi(mmat3)
    ename = ename.__add__(str(matfarsiname))
    eprop = eprop.__add__(" Roll ")    
    eprop = eprop.__add__(ename)   
    eprop = eprop.__add__(", thickness: ")
    eprop = eprop.__add__(" 0.5 mm ,  ")
    rswide=1200
    eprop = eprop.__add__(str(rswide))
    
    rrawmatsw= getsizerawmatforelement('rupture',rtype,rsize)
    rawdim =  getrawsheetmatdimension(rawmatsw[0],qty,rswide)
    
    eprop = eprop.__add__(str(int(rawdim[0])))
    eprop = eprop.__add__(" * ")
    eprop = eprop.__add__(str(int(rawdim[1])))
    eprop = eprop.__add__("  mm ")
    matthick = float(0.5)
    matwidth = float(rawdim[0])
    matlen = float(rawdim[1])
    matden = float(getmaterialdensity(mmat3))
    matmass = massofmaterialfromdimensionmm(matthick,matwidth,matlen,matden)
    rrow.append(indexconter)
    rrow.append(ename)
    rrow.append(eprop)
    rrow.append(1)
    rrow.append(unit_of_item[2])
    rrow.append(matmass)
    matpriceunit = getmaterialpriceunit(mmat3)
    rrow.append(matpriceunit)
    
    rrow.append(matmass*matpriceunit)
    rt.append(rrow) 
    
    Q=1
    eprop=" "
    if wtl==True:
        indexconter+=1
        rt.append(descelementofmto(indexconter,5," ",1))
        #ename = str(rupelfarsi[5])
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[5])
        
        #rt.append(rrow) 
        
    if anm==True:
        indexconter+=1
        rt.append(descelementofmto(indexconter,3," ",1))
        #ename = str(rupelfarsi[3])
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[3])
        
        #rt.append(rrow) 
        
    if wrc==True:
        indexconter+=1
        rt.append(descelementofmto(indexconter,4," ",1))
        #ename = str(rupelfarsi[4])
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[4])
        #rt.append(rrow) 
        
    if tag==True:
        indexconter+=1
        rt.append(tagmakerformtolist(indexconter,qty))
        #rt.append(descelementofmto(indexconter,8," ",1))
    
        
    if bxg==True:
        indexconter+=1
        rt.append(descelementofmto(indexconter,11," ",1))
        indexconter+=1
        rt.append(descelementofmto(indexconter,12," ",1))
        indexconter+=1
        rt.append(descelementofmto(indexconter,13," ",1))
        #ename = ename.__add__(str(rupelfarsi[11]))
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[11])
        #rt.append(rrow) 
        
        
        #ename = ename.__add__(str(rupelfarsi[12]))
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[12])
        #rt.append(rrow) 
        
        
        #ename = ename.__add__(str(rupelfarsi[13]))
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[13])
        #rt.append(rrow) 
        
        
        
    
        #ename = ename.__add__(str(rupelfarsi[8]))
        #rrow.append(ename)      
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[8])
        #rt.append(rrow) 
    
    if shp==True:
        indexconter+=1
        rt.append(descelementofmto(indexconter,14," ",1))
        #ename = ename.__add__(str(rupelfarsi[14]))
        #rrow.append(ename)
        #rrow.append(eprop)
        #rrow.append(Q)
        #rrow.append(unit_of_item[14])
        #rt.append(rrow)   
    rt.append(["","","","","","","Total Price",'=SUM(H2:H12)'])
    df1 = pd.DataFrame(rt, columns=temple_mto_header_farsi)  
    mtoTitle = "Project ".__add__('Rupture Disks, type: ,').__add__(rtype).__add__(' , Size: ').__add__(str(rsize)).__add__(' inch ,  Burst Pressure: ').__add__(str(rbp)).__add__(' bar, Qty: ').__add__(str(qty))
    ffxn = getmyfilename(rt=rtype,rs=rsize,rb=rbp,rq=qty)
    return writedataframedstylishtofile(df1,ffxn,mtoTitle)


  
def descelementofmto(i,en,ep,qt):
    rdfs= readthissheetofdbfilke('mto')
    rdfs = rdfs[rdfs['element']=='rupture']
    rupelfarsi =       rdfs['itemf'].values.tolist()
    start_price_at =  rdfs['pr'].values.tolist()    
    unit_of_item =    rdfs['unitf'].values.tolist()     
    ow=[]
    ename = str(rupelfarsi[en])
    ow.append(i) 
    ow.append(ename)      
    ow.append(ep)
    ow.append(qt)
    ow.append(unit_of_item[en])
    
    ow.append(" ")
    ow.append(start_price_at[en])
    ow.append(int(float(start_price_at[en])*qt))
    return ow 

tag_index=8    
def tagmakerformtolist(i,qt):
    ow=[]
    rdfs= readthissheetofdbfilke('mto')
    rdfs = rdfs[rdfs['element']=='rupture']
    rupelfarsi =       rdfs['itemf'].values.tolist()
    start_price_at =  rdfs['pr'].values.tolist()    
    unit_of_item =    rdfs['unitf'].values.tolist()     
    ow=[]
    ename = 'Tag plates'    
    ow.append(i) 
    ow.append(ename)     
    ep ="sheet , material ss316 , thickness 0.5mm , 200*155 mm , QTY: ".__add__(str(qt))
    ow.append(ep)
    ow.append(1)
    ow.append(unit_of_item[2])
    matthick = float(0.5)
    matwidth = float(200)
    matlen = float(155)
    matden = float(8.22)
    matmass = massofmaterialfromdimensionmm(matthick,matwidth,matlen,matden)*qt    
    ow.append(matmass)
    matpriceunit = getmaterialpriceunit('s31')
    ow.append(matpriceunit)
    
    ow.append(matmass*matpriceunit)  
    return ow

def massofmaterialfromdimensionmm(w,l,t,d):
    return (w*0.001*l*0.001*t*d)