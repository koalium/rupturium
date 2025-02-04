#!/usr/bin/env python
import FreeSimpleGUI as sg
import time
import random
from json import (load as jsonload, dump as jsondump)
from pathlib import Path
import os
from os import path as pats
from tester import *
"""
    Demo program showing how to create your own "LED Indicators"
    The LEDIndicator function acts like a new Element that is directly placed in a window's layout
    After the Window is created, use the SetLED function to access the LED and set the color

"""
filpathdef = 'my_data/001.xlsx'
file_path = 'my_data/my_file.txt'
filenamedef = '1'
fileexepdef ='xlsx'



def getmyfilename(pt='my_data/',fn='1',rt='reverse',rs=4,rb=11,rq=10):
    filename=""
    if not os.path.exists(pt): 
          
        # if the demo_folder directory is not present  
        # then create it. 
        os.makedirs(pt)     
    if fn.find('__')>-1:
        filename = fn[0:fn.find('__')]
    if fn.find('.')>-1:
        filename = fn[0:fn.find('.')]
        fileexo = fn[fn.find('.'):len(fn)]
    else:
        fileexo = fileexepdef
        for f in fn :
            if f in ('0123456789'):
                filename = filename.__add__(f) 
    
                
    file_path_name = pt.__add__(filename).__add__('__type ').__add__(str(rt)).__add__('_size ').__add__(str(rs)).__add__('_BP ').__add__(str(rb)).__add__('_QTY ').__add__(str(rq)).__add__('.').__add__(fileexo)
    # Check if the file exists
    while os.path.exists(file_path_name):
        filename = str(int(filename)+1)
        file_path_name = pt.__add__(filename).__add__('__type ').__add__(str(rt)).__add__('_size ').__add__(str(rs)).__add__('_BP ').__add__(str(rb)).__add__('_QTY ').__add__(str(rq)).__add__('.').__add__(fileexo)
    return file_path_name


def settings_window():
    """
    Create and interact with a "settings window". You can a similar pair of functions to your
    code to add a "settings" feature.
    """

    _layout = [[[sg.Slider(orientation='h', key='-SKIDER-'),
                     sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-'),],                    
                    [sg.Button("Open Folder")],
                    [sg.Button("Open File")]]]  
    popup_layout  = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                               [sg.Listbox(values = sg.theme_list(), 
                                 size =(20, 12), 
                                 key ='-THEME LISTBOX-',
                                 enable_events = True)],
                                 [sg.Button("Set Theme")]]    
    output_layout = [[sg.Text("log of the doies")],
                      [sg.Multiline(size=(25,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                      
                      ]     
    window = make_window()
    current_theme = sg.theme()

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        if event == 'Save':
            # Save some of the values as user settings
            sg.user_settings_set_entry('-input-', values['-IN-'])
            sg.user_settings_set_entry('-theme-', values['-LISTBOX-'][0])
            sg.user_settings_set_entry('-option1-', values['-CB1-'])
            sg.user_settings_set_entry('-option2-', values['-CB2-'])

        # if the theme was changed, restart the window
        if values['-LISTBOX-'][0] != current_theme:
            current_theme = values['-LISTBOX-'][0]
            window.close()
            window = make_window()