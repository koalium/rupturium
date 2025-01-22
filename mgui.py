import FreeSimpleGUI as sg

from dbmakeread import *
#from working import *
from tester import *
from handler import *

SETTINGS_PATH = '.'


mlstr=""
mainmaterialheader = 'mainmat'
mainmatlist = mylister(dbfilename,materialsheetname,mainmaterialheader)

# Create a UserSettings object. The JSON file will be saved in the same folder as this .py file
window_contents = sg.UserSettings(path='.', filename='mysettings.json')
keys_to_save = ('-COMBOTYPER-', '-INPUTRNS-', '-SPINRQTY-','-SPINHQTY-', '-COMBOMAINMATERIALR-', '-COMBOSEALMATERIALR-', '-COMBOSUBATERIALR-', '-CBSENR-','-CBBXGR-', '-COMBOTYPEH-', '-INPUTHNS-','-COMBOMAINMATERIALH-','-CBSHPR-','-CBWJLR-', '-CBWRCR-', '-CBANMR-',  '-INPUTRBT-', '-INPUTRBP-', '-CBGKTH-')
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
    
    sg.theme('DarkBlue')
   # matlist = matlister('mainmat')#['SS304', 'SS316', 'Monel', 'Inconel', 'Hastalloy', 'Nickel', 'Titanium', 'Aluminium', 'Silver','Pvc','Ptfe', 'Other']
    menu_def = [['&file', ['&New','&Open','&Save','&Save as','&Close','&Exit']],
                ['&Option', ['&WorkSpace','&Setting']],
                ['&Help', ['&Content','&License','U&pdate','&Help','&About']] ]
    right_click_menu_def = [[], ['Select','Edit','save']]
    graph_right_click_menu_def = [[], ['Erase','Clear']]

    # Table Data
    datatable = findtownearestruptures('reverse',2,5).values.tolist()
    headingstable = ["material","thickness","size","bpress","btemp","realbp","res","frmh","drw"]

    rupture_layout =  [[sg.Menu(menu_def, key='-MENU-')],
                [sg.Text('Type:'),sg.Combo(values=('Reverse', 'Forward', 'Flat'), default_value='Reverse', readonly=True, k='-COMBOTYPER-'),  sg.Text(' Nominal Size:'),sg.Input('2',key='-INPUTRNS-', size=(3,5)), sg.Text('Burst Pressure:'),sg.Input('5',key='-INPUTRBP-', size=(5,5)),sg.Text('Burst Temprature:'),sg.Input('25',key='-INPUTRBT-', size=(3,5)),sg.Stretch()], 
                [sg.HorizontalSeparator()],
                [sg.Text('Materials:'),sg.Combo(values=(mainmatlist[0:mainmatlist.__len__()-6]), default_value=mainmatlist[2], readonly=True, k='-COMBOMAINMATERIALR-'),sg.Combo(values=(mainmatlist[mainmatlist.__len__():mainmatlist.__len__()-6:-1]), default_value=mainmatlist[mainmatlist.__len__()-1], readonly=True, k='-COMBOSEALMATERIALR-'),sg.Combo(values=(mainmatlist[0:mainmatlist.__len__()]), default_value=mainmatlist[2], readonly=True, k='-COMBOSUBATERIALR-'),sg.Checkbox('material analysis', default=True, k='-CBANMR-'),sg.Stretch()],   
                [sg.Text('Qty'), sg.Spin([i for i in range(1,1001)], initial_value=1, k='-SPINRQTY-'),sg.Stretch(),sg.Checkbox('wirecut', default=True, k='-CBWRCR-'),sg.Checkbox('waterjet/laser', default=True, k='-CBWJLR-'),sg.Checkbox('Sensor', default=False, k='-CBSENR-'),sg.Checkbox('Tags', default=True, k='-CBTAGR-'),sg.Checkbox('shipping', default=True, k='-CBSHPR-'),sg.Checkbox('Boxing', default=True, k='-CBBXGR-'),sg.Stretch()],
                [sg.Button('MTO',key='-BTNMTOR-'), sg.Button('Save',key='-BTNSAVER-'),sg.Stretch(),  sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-BTNLOGOR-'),sg.Stretch()],
                [sg.HorizontalSeparator()],
                #[sg.Table(values=datatable, headings=headingstable, max_col_width=15,background_color='black',auto_size_columns=True,display_row_numbers=True,justification='right',num_rows=2,alternating_row_color='black',
                                                #key='-TABLE-',
                                                #row_height=22)]     ,   
                [sg.Graph((CW,CH), (CLBY,CLBY),(CRTX,CRTY),background_color="black", key='-GRAPH-', enable_events=True,float_values=True,
                          right_click_menu=graph_right_click_menu_def)]]

    holder_layout = [[sg.Text('Type:'),sg.Combo(values=('Reverse', 'Forward'), default_value='Reverse', readonly=True, k='-COMBOTYPEH-'),sg.Text(' Nominal Size:'),sg.Input('1',key='-INPUTHNS-', size=(3,5)),sg.Text('Materials:'),sg.Combo(values=(mainmatlist[0:mainmatlist.__len__()-6]), default_value=mainmatlist[2], readonly=True, k='-COMBOMAINMATERIALH-'),sg.Checkbox('Gasket', default=True, k='-CBGKTH-')],
               [sg.Spin([i for i in range(1,1001)], initial_value=1, k='-SPINHQTY-'), sg.Text('Qty')],
               [sg.Button('MTO',key='-BTNMTOH-'), sg.Button('Save',key='-BTNSAVEH-'), sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGOBTNH-')],   
                [sg.Graph((CW,CH), (CLBY,CLBY),(CRTX,CRTY),background_color="black", key='-HGRAPH-', enable_events=True,float_values=True,
                          right_click_menu=graph_right_click_menu_def)],
               [sg.Multiline('', size=(25,5), expand_x=True, expand_y=True, k='-MLINEH-')]]

    
    
    flamearrestor_layout= [[sg.Text("prepairing for flame arrestor")]]

    breathervalve_layout = [[sg.Text("Breather Valve")]]   
    
   
      
     
    
   # layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)]]
    layout =[[sg.TabGroup([[  sg.Tab('Rupture Disks', rupture_layout),
                               sg.Tab('Holders', holder_layout),
                               sg.Tab('FlameArrestor', flamearrestor_layout),
                               sg.Tab('BreatherValve', breathervalve_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

               ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('koalium Ltd ', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=False, finalize=True, keep_on_top=False)
    window.set_min_size(window.size)
    return window

def main():
    
    
    window = make_window(sg.theme())
    tickcounter = 0
    # This is an Event Loop 
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
        #
        if event == sg.WIN_CLOSED :
                               
            break
        if event == event == 'Exit':
            for key in keys_to_save:
                if type(values[key]) != type("a") or type(2.0) or type(1):
                    continue
                sg.user_settings_set_entry(key, values[key])   
                
            break
        
        if  len(values['-INPUTRNS-']) and values['-INPUTRNS-'][-1] not in ('0123456789'):
            window['-INPUTRNS-'].update(values['-INPUTRNS-'][:-1])
            continue
        if  len(values['-INPUTRBP-']) and values['-INPUTRBP-'][-1] not in ('0123456789'):
            window['-INPUTRBP-'].update(values['-INPUTRBP-'][:-1])     
            continue
        if  len(values['-INPUTRBT-']) and values['-INPUTRBT-'][-1] not in ('0123456789'):
            window['-INPUTRBT-'].update(values['-INPUTRBT-'][:-1])     
            continue        
            
        if event == '-BTNLOGOR-':
            notfountsizeerrorgui(rupturebtnlogo(window,values))
            
        #ppop
        elif event == '-BTNMTOR-':
            rupturebtnmto(window,values)
        #
        elif event == '-BTNSAVER-':
            notfountsizeerrorgui(rupturebtnsave(window,values))
            print("[LOG] Clicked BTNSAVER")
            for key in keys_to_save:
                sg.user_settings_set_entry(key, values[key])            
            
        #ppop        
        elif event == '-BTNMTOH-':
            print("[LOG] Clicked BTNMTOH")
            holderbtnsmto(window,values)
        #
        #
        elif event == '-BTNSAVEH-':
            holderbtnsave(window,values)
            
            
        #
        elif event == '-BTNLOGOH-':
            holderbtnlogo(window,values)
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
        elif event == 'Setting':
            
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
    
    
    
    