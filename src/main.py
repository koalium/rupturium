from globalvars import *
from filehandler import *
from graphdraw import *
from calculation import *
from handler import *
from mtomaker import *
import FreeSimpleGUI as sg
import pandas as pd
import os

import mgui as mg

if __name__ == '__main__':
    
    readresorcemakesource(filename=dbfilename) 
    mg.main()