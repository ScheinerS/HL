#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transfiere los archivos '[ID].txt' a ~/Documents/HE60/run/batch.
"""

# Directorio para los archivos:

import os
import shutil
import glob
import check_dir as cd

# def check_dir(path):

#     is_dir = os.path.isdir(path)
#     if(not is_dir):
#         os.mkdir(path)
#         print('Created:', path)


def transfer(orig_dir, dest_dir):
    
    os.chdir(orig_dir)
    files = os.listdir()
    
    for file in files:
        try:
            os.remove(dest_dir + os.sep + file)
        except:
            pass
    
    for file in files:
        shutil.move(file, dest_dir)
        
        
    return 

def transfer_PD_files(Tag, path_HE60):
    
    path_digital = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'digital' 
    path_printout = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'printout'
    
    D_files = glob.glob(path_digital + os.sep + 'D*' + Tag + '.txt')
    P_files = glob.glob(path_printout + os.sep + 'P*' + Tag + '.txt')
    
    cd.check_dir(path_digital + os.sep + Tag)
    cd.check_dir(path_printout + os.sep + Tag)
    
    for file in D_files:
        shutil.copy2(file, path_digital + os.sep + Tag)
        os.remove(file)
    
    for file in P_files:
        shutil.copy2(file, path_printout + os.sep + Tag)
        os.remove(file)
    
    return