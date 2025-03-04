from globalvars import *
from filehandler import *
from graphdraw import *
from calculation import *
from handler import *
from mtomaker import *
mainmatlist = mylister(dbfilename, materialsheetname, mainmaterialheader)

def notfountsizeerrorgui(s):
    if s==False:
        sg.popup('incorrect and incompatible size!!!!!', keep_on_top=True)

def make_key(key):
    """
    Returns a dictionary that is used to pass parameters to an Input element.
    Another approach could be to return an Input element. The downside to that approach is
    the lack of parameters and associated docstrings when creating the layout.

    :param key:
    :return: Dict
    """
    return {'default_text':sg.user_settings_get_entry(key, ''), 'key':key}


def make_window(theme):
    CW=800
    CH=400
    CLBX=5
    CLBY=5
    CRTX=CW-5
    CRTY=CH-5
    sg.theme('DarkBlue')
   # matlist = matlister('mainmat')#['SS304', 'SS316', 'Monel', 'Inconel', 'Hastalloy', 'Nickel', 'Titanium', 'Aluminium', 'Silver','Pvc','Ptfe', 'Other']
    menu_def = [['&file', ['&New','&Open','&Save','&Save as','&Close','&Exit']],
                ['&Option', ['&Prices','&Setting']],
                ['&Help', ['&Content','&License','U&pdate','&Help','&About']] ]
    right_click_menu_def = [[], ['Select','Edit','save']]
    graph_right_click_menu_def = [[],['last','first','Clear']]

   
    headingstable = ["material","thickness","size","bpress","btemp","realbp","res","frmh","drw"]
    sizespin=[0.5,0.75,1,1.5,2,3]
    for i in range(4,64,2):
        sizespin.append(i)
    rupture_layout =  [[sg.Menu(menu_def, key='-MENU-')],
                [sg.Text('Type:', font = ('Calibri', 12, 'bold')), sg.Combo(values=('Reverse', 'Forward', 'Flat'), default_value='Reverse', readonly=True, k='-COMBOTYPER-'), sg.Text(' Nominal Size:', font = ('Calibri', 12, 'bold')),sg.Spin(sizespin, initial_value=1, k='-INPUTRNS-',size=(4,12)),  sg.Text('Burst Pressure:'), sg.Input('5', key='-INPUTRBP-', size=(5, 5)), sg.Text('Burst Temprature:'), sg.Input('25', key='-INPUTRBT-', size=(3, 5)), sg.Text('Qty', font = ('Arial', 12)), sg.Spin([i for i in range(0, 1001)], initial_value=1, k='-SPINRQTY-')],
                [sg.HorizontalSeparator()],
                [sg.Text('Materials:', font = ('Arial', 14, 'bold')), sg.Combo(values=(mainmatlist[0:mainmatlist.__len__() - 6]), default_value=mainmatlist[2], readonly=True, k='-COMBOMAINMATERIALR-'), sg.Combo(values=(mainmatlist[mainmatlist.__len__():mainmatlist.__len__() - 6:-1]), default_value=mainmatlist[mainmatlist.__len__() - 1], readonly=True, k='-COMBOSEALMATERIALR-'), sg.Combo(values=(mainmatlist[0:mainmatlist.__len__()]), default_value=mainmatlist[2], readonly=True, k='-COMBOSUBATERIALR-'), sg.Checkbox('material analysis', default=False, k='-CBANMR-'), sg.Text('-Qty', font = ('Arial', 12),k='-matextqty-'), sg.Spin([i for i in range(0, 1001)], initial_value=0, k='-SPINMAQTY-')],
                [sg.Checkbox('wirecut', font = ('bold'), default=True, k='-CBWRCR-'), sg.Checkbox('waterjet/laser', default=True, k='-CBWJLR-'), sg.Checkbox('Boxing', default=True, k='-CBBXGR-'), sg.Checkbox('shipping', default=True, k='-CBSHPR-'), sg.Checkbox('Tags', default=True, k='-CBTAGR-'), sg.Checkbox('Sensor', default=False, k='-CBSENR-'), sg.Text('Sensor Qty', k='-txtsnsr-'), sg.Spin([i for i in range(0, 1001)], initial_value=0, k='-SPINRSNSQTY-')],
                [sg.Button('MTO', button_color = ('White', 'Red'), key='-BTNMTOR-'), sg.Button('Save', key='-BTNSAVER-'), sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-BTNLOGOR-'), sg.Checkbox('Holder', font = ('Arial', 12, 'bold'), default=False, k='-CBBHLDR-'), sg.Text('Holders Qty', k='-texthldqty-'), sg.Spin([i for i in range(0, 1001)], initial_value=0, k='-SPINRHQTY-'), sg.Combo(values=(mainmatlist[0:mainmatlist.__len__() - 6]), default_value=mainmatlist[2], readonly=True, k='-COMBOMAINMATERIALRH-'), sg.Checkbox('Gasket', default=False, k='-CBGKTRH-')],
                [sg.HorizontalSeparator()],
                #[sg.Table(values=datatable, headings=headingstable, max_col_width=15,background_color='black',auto_size_columns=True,display_row_numbers=True,justification='right',num_rows=2,alternating_row_color='black',
                                                #key='-TABLE-',
                                                #row_height=22)]     ,   
                [sg.Graph((CW, CH), (CLBX, CLBY), (CRTX, CRTY), background_color="black", key='-GRAPH-', enable_events=True,
                                  right_click_menu=graph_right_click_menu_def)]]

    holder_layout = [[sg.Text('Type:'), sg.Combo(values=('Reverse', 'Forward'), default_value='Reverse', readonly=True, k='-COMBOTYPEH-'), sg.Text(' Nominal Size:'), sg.Input('1', key='-INPUTHNS-', size=(3, 5)), sg.Text('Materials:'), sg.Combo(values=(mainmatlist[0:mainmatlist.__len__() - 6]), default_value=mainmatlist[2], readonly=True, k='-COMBOMAINMATERIALH-'), sg.Checkbox('Gasket', default=True, k='-CBGKTH-')],
                     [sg.Spin([i for i in range(1, 1001)], initial_value=1, k='-SPINHQTY-'), sg.Text('Qty')],
                     [sg.Button('MTO', key='-BTNMTOH-'), sg.Button('Save', key='-BTNSAVEH-'), sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGOBTNH-')],
                     [sg.Graph((CW, CH), (CLBY, CLBY), (CRTX, CRTY), background_color="black", key='-HGRAPH-', enable_events=True, float_values=True,
                                       right_click_menu=graph_right_click_menu_def)],
                     [sg.Multiline('', size=(25, 5), expand_x=True, expand_y=True, k='-MLINEH-')]]

    
    
    flamearrestor_layout= [[sg.Text("prepairing for flame arrester")]]

    breathervalve_layout = [[sg.Text("Breather Valve")]]
    
    
    col1 = [[sg.Text("Sheets (per Kg):")],
        [sg.Stretch(), sg.Text("SS304"), sg.Input('4444000', key='-INPUTPRICESS304SHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("SS316 "), sg.Input('5422000', key='-INPUTPRICESS316SHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Monel"), sg.Input('8435000', key='-INPUTPRICEMONELSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Inconel"), sg.Input('8895000', key='-INPUTPRICEINCONELSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Hastelloy"), sg.Input('9735000', key='-INPUTPRICEHASTELLOYSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Aluminium"), sg.Input('3785000', key='-INPUTPRICEALUMINIUMSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Titanium "), sg.Input('42569000', key='-INPUTPRICETITANIUMSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Nickel "), sg.Input('10256000', key='-INPUTPRICENICKELSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Copper "), sg.Input('13685000', key='-INPUTPRICECOPERSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("CS "), sg.Input('1450000', key='-INPUTPRICECSSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("PTFE "), sg.Input('1980000', key='-INPUTPRICEPTFESHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("PVC "), sg.Input('1660000', key='-INPUTPRICEPVCSHEET-', size=(9, 8))],
            [sg.Stretch(), sg.Text("Silver"), sg.Input('485695000', key='-INPUTPRICESHEETSILVER-', size=(9, 8))]]
    col2 = [[sg.Text("Shaft (per Kg):")],
        [sg.Stretch(), sg.Text("SS304"), sg.Input('4350000', key='-INPUTPRICESHAFT304-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" SS316"), sg.Input('6500000', key='-INPUTPRICESHAFT316-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Monel"), sg.Input('8800000', key='-INPUTPRICESHAFTMONEL-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Inconel"), sg.Input('9200000', key='-INPUTPRICESHAFTINCONEL-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Hastelloy"), sg.Input('10100000', key='-INPUTPRICESHAFTHASTELLOY-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Aluminium"), sg.Input('2700000', key='-INPUTPRICESHAFTALUMINIUM-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Copper"), sg.Input('14500000', key='-INPUTPRICESHAFTCOPPER-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Titanium"), sg.Input('42000000', key='-INPUTPRICESHAFTTITANIUM-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" MO40"), sg.Input('1250000', key='-INPUTPRICESHAFTMO40-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Nickel"), sg.Input('8500000', key='-INPUTPRICESHAFTNICKEL-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Chromium"), sg.Input('8500000', key='-INPUTPRICESHAFTCHROM-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" MO60"), sg.Input('8500000', key='-INPUTPRICESHAFTMO60-', size=(9, 8))],
            [sg.Stretch(), sg.Text(" Silver"), sg.Input('598568000', key='-INPUTPRICESHAFTSILVER-', size=(9, 8))]
            ]
   
    col3 = [[sg.Stretch(),sg.Text("Others:",justification='center'),sg.Stretch()],
        [sg.Stretch(), sg.Text("Sensor"), sg.Input('18000000', key='-INPUTPRICESENSOR-', size=(9, 8))],
        [sg.Stretch(), sg.Text("Material Analysis"), sg.Input('18000000', key='-INPUTPRICESANALYSMAT-', size=(9, 8))],
                        [sg.Stretch(), sg.Text("testing burst price"), sg.Input('5000000', key='-INPUTPRICESTESTING-', size=(9, 8))],
                        [sg.Stretch(), sg.Text("marking an Tagprice"), sg.Input('2500000', key='-INPUTPRICESTAG-', size=(9, 8))],
                        [sg.Stretch(), sg.Text("cnc milling"), sg.Input('29000000', key='-INPUTPRICEMILLING-', size=(9, 8))],
                        [sg.Stretch(), sg.Text("machinery and treading"), sg.Input('27000000', key='-INPUTPRICEMACHINERY-', size=(9, 8))],
                        [sg.Stretch(), sg.Text("welding job price "), sg.Input('12000000', key='-INPUTPRICEWELDING-', size=(9, 8))],
                        [sg.Stretch(), sg.Text("polish and paint"), sg.Input('2000000', key='-INPUTPRICEPAINT-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("waterjet-laser cutting "), sg.Input('35000000', key='-INPUTPRICESWATERJET-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("wirecut price for drw"), sg.Input('280000000', key='-INPUTPRICEWIRECUT-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("boxing price"), sg.Input('5000000', key='-INPUTPRICEBOXING-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("Heat Form"), sg.Input('5000000', key='-INPUTPRICEHEATFORM-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("Heat Treatment"), sg.Input('5000000', key='-INPUTPRICEHEATTREATMENT-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("Hydoforming"), sg.Input('5000000', key='-INPUTPRICEHYDROFORM-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("Styrofoam"), sg.Input('5000000', key='-INPUTPRICEBOXING-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("gasket"), sg.Input('3350000', key='-INPUTPRICEGASKETS-', size=(9, 8))],
                           [sg.Stretch(), sg.Text("Shipping total"), sg.Input('35000000', key='-INPUTPRICESHIPPING-', size=(9, 8))] ]
                           
    insertconst_layout = [
              [sg.HorizontalSeparator()],
              
              [sg.Column(col1, key='c1', element_justification='c', expand_x=True,vertical_alignment='top'),
               sg.Column(col2, key='c2', element_justification='t', expand_x=True,vertical_alignment='top'),
               sg.Column(col3, key='c3', element_justification='t', expand_x=True,vertical_alignment='top')],
              [sg.VStretch()],
              [sg.HorizontalSeparator()],
              [sg.Button('Save', key='-BTNSAVEPRICE-'), sg.Button('Cancel', key='-BTNCANCALPRICE-'), sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGOBTNPRICE-')],
    [sg.VStretch()]]
    
      
     
    
   # layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)]]
    layout =[[sg.TabGroup([[sg.Tab('Rupture Disks', rupture_layout, key='-rupturetab-', visible=True),
                                    sg.Tab('Holders', holder_layout, key='-holdertab-', visible=False,disabled=True),
                                    sg.Tab('FlameArrestor', flamearrestor_layout, key='-flamearrestortab-',disabled=True,visible=False),
                                    sg.Tab('BreatherValve', breathervalve_layout, key='-breathervalvetab-', visible=False,disabled=True),
                                    sg.Tab('prices(rls/Kg)', insertconst_layout, key='-pricetab-', visible=False,tooltip='Real Per KG',disabled=True)]], key='-TAB GROUP-',enable_events=True,change_submits=True,focus_color='darkgreen' ,expand_x=True, expand_y=True),

              ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('koalium Ltd ', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0), use_custom_titlebar=False, finalize=True, keep_on_top=False, no_titlebar=False,  enable_window_config_events=True)
    window.set_min_size(window.size)
    
    return window

def saveallwindovalueascan(values):
    for key in keys_to_save:
        if type(values[key]) != type("a") or type(2.0) or type(1):
            continue
        sg.user_settings_set_entry(key, values[key])
def changefocustab(tabkey='-',fotab=[]):
    fotabs=[]
    fotabs.append(fotab[1])
    fotabs.append(tabkey)
    return fotabs
def main():
    Global_plane=[]
    graphdarawn=False
    gsize = (800,400)
    focus_tab=[]
    focus_tab.append('-rupturetab-')
    focus_tab.append('-rupturetab-')
    window = make_window(sg.theme())
    orig_win_size = window.current_size_accurate()
    graph = window['-GRAPH-'] 
    tickcounter = 0
    # This is an Event Loop 
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('===== Event = ', event, ' ')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
        #
        if event == sg.WIN_CLOSED :
            window.close()                     
            break
        
        
              
        if event == event == 'Exit':
            for key in keys_to_save:
                if type(values[key]) != type("a") or type(2.0) or type(1):
                    continue
                sg.user_settings_set_entry(key, values[key])
            window.close()      
            break
        
        
        if  len(values['-INPUTRBP-']) and values['-INPUTRBP-'][-1] not in ('0123456789.'):
            window['-INPUTRBP-'].update(values['-INPUTRBP-'][:-1])     
            continue
        if  len(values['-INPUTRBT-']) and values['-INPUTRBT-'][-1] not in ('0123456789.'):
            window['-INPUTRBT-'].update(values['-INPUTRBT-'][:-1])     
            continue       
            
        if event == '-BTNLOGOR-':
            graphdarawn=True
            rupturebtnlogo(window, values)
            
        #ppop
        elif event == 'last':
            
            Global_plane=rupturegraphnext(window, values)
        #   
        elif event == 'first':
            
            Global_plane=rupturegraphprev(window, values)
        #           
        elif event == '-BTNMTOR-':
            rupturebtnmto(window, values)
        #
        elif event == '-BTNSAVER-':
            notfountsizeerrorgui(rupturebtnsave(window, values))
            print("[LOG] Clicked BTNSAVER")
            for key in keys_to_save:
                sg.user_settings_set_entry(key, values[key])
            
        #ppop        
        elif event == '-BTNMTOH-':
            print("[LOG] Clicked BTNMTOH")
            holderbtnsmto(window, values)
        #
        #
        elif event == '-BTNSAVEH-':
            holderbtnsave(window, values)
            
            
        #
        elif event == '-BTNLOGOH-':
            holderbtnlogo(window, values)
            print("[LOG] Clicked BTNLOGOH!")
            
        #
        
        elif event == "Clear":
            graph = window['-GRAPH-']  
            graph.erase()   
            
            print("[LOG] Clear")
        #
        
        
        elif event == 'New':
            print("[LOG] Clicked New!")      
        #
        elif event == 'Open':
            for key in keys_to_save:
                saved_value = window_contents[key]
                window[key].update(saved_value)               
            print("[LOG] Clicked Open File!")
           
            
        #
        elif event == 'Save':
            for key in values:
                window_contents[key] = values[key]            
            
            print("[LOG] Clicked Save!")      
        #
        elif event == 'Save as':
            for key in keys_to_save:
                sg.user_settings_set_entry(key, values[key])
            
            print("[LOG] Clicked 'Save as'!")      
        #
        elif event == 'Close':
                        
            print("[LOG] Clicked Close!")      
        #
        elif event == 'Prices':
            window['-pricetab-'].update(visible=True,disabled=False)
            window['-rupturetab-'].update(visible=False,disabled=True)
            focus_tab=changefocustab('-pricetab-',focus_tab)
            print("[LOG] Clicked Setting!")      
        # 
        elif event == 'WorkSpace':
               
            print("[LOG] Clicked WorkSpace!")      
        #         
        elif event == 'Content':
            print("[LOG] Clicked Content!")      
        #  
        elif event == 'License':
            print("[LOG] Clicked License!")      
        #  
        elif event == 'Update':
            print("[LOG] Clicked Update!")      
        #  
        elif event == 'Help':
            print("[LOG] Clicked Help!")      
        #  
        elif event == 'About':
            print("[LOG] Clicked About!")
            sg.popup('koalium ltd ',
                     'rupture disk design',
                     'MTO preparation for Ruptures and Holders',
                     'Flame arrestor predesign and test handle',
                     'just put your wanted and pay our license', keep_on_top=True)
        #
        elif event == '-BTNSAVEPRICE-':
            print("[LOG] Clicked BTNSAVEPRICE!")    
            saveallwindovalueascan(values)   
            window[focus_tab[0]].update(visible=True,disabled=False)
            window['-pricetab-'].update(visible=False,disabled=True)
            
            focus_tab=changefocustab(focus_tab[0],focus_tab)
            window['-pricetab-'].update(visible=False,disabled=False)
            for key in keys_to_save:
                if type(values[key]) != type("a") or type(2.0) or type(1):
                    continue
                sg.user_settings_set_entry(key, values[key])
        # 
        elif event == '-BTNCANCALPRICE-':
            print("[LOG] Clicked BTNCANCELPRICE!")  
            window[focus_tab[0]].update(visible=True,disabled=False)
            window['-pricetab-'].update(visible=False,disabled=True)
            focus_tab=changefocustab(focus_tab[0],focus_tab)
            window['-pricetab-'].update(visible=False,disabled=False)
            
        # 
        elif event == '-LOGOBTNPRICE-':
            print("[LOG] Clicked LOGOBTNPRICE!")    
            saveallwindovalueascan(values)
            for key in keys_to_save:
                if type(values[key]) != type("a") or type(2.0) or type(1):
                    continue
                sg.user_settings_set_entry(key, values[key])
        #       
        if values['-CBBHLDR-']:
            window['-texthldqty-'].update(visible=True) 
            window['-SPINRHQTY-'].update(visible=True) 
            window['-COMBOMAINMATERIALRH-'].update(visible=True) 
            window['-CBGKTRH-'].update(visible=True)        
            
            
        else:
            window['-CBGKTRH-'].update(visible=False) 
            window['-COMBOMAINMATERIALRH-'].update(visible=False) 
            window['-SPINRHQTY-'].update(visible=False)
            window['-texthldqty-'].update(visible=False) 
            
        if values['-CBSENR-']:
            window['-txtsnsr-'].update(visible=True) 
            window['-SPINRSNSQTY-'].update(visible=True) 
                
        else:
            window['-txtsnsr-'].update(visible=False) 
            window['-SPINRSNSQTY-'].update(visible=False) 
        #
        if values['-CBANMR-']:
            window['-matextqty-'].update(visible=True) 
            window['-SPINMAQTY-'].update(visible=True) 
                
        else:
            window['-matextqty-'].update(visible=False) 
            window['-SPINMAQTY-'].update(visible=False)        
        if tickcounter== 0:
            for key in keys_to_save:
                saved_value = window_contents[key]
                window[key].update(saved_value)                      
            tickcounter=0
        else:
            firstattemp = False
            
            
        #
        tickcounter+=1
                                        
        
    window.close()
    exit(0)

if __name__ == '__main__':
    
      
    main()
    
    
    
    