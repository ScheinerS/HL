#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transfiere los archivos '[ID].txt' a ~/Documents/HE60/run/batch.
"""

# Directorio para los archivos:

import os
import shutil
#import glob


def check_dir(path):

    is_dir = os.path.isdir(path)
    if(not is_dir):
        os.mkdir(path)
        print('Created:', path)


def transfer(orig_dir, dest_dir):
    print('\nMoving files...')
    
    #current_dir = os.getcwd()
    
    os.chdir(orig_dir)
    files = os.listdir()
    
    #dest_dir = '/home/santiago/Documents/HE60/run/batch'
    
    for file in files:
        try:
            os.remove(dest_dir + os.sep + file)
        except:
            pass
    
    for file in files:
        shutil.move(file, dest_dir)
        
        
    print('Done.\n')
    
    return 


def transfer_data_files():
    print('\nMoving data files...')
    
    current_dir = os.getcwd()
    orig_dir = current_dir + '/DATA/'
    
    os.chdir(orig_dir)
    files = os.listdir()
    
    dest_dir = '/home/santiago/Documents/HE60/data/DATA_SS'
    
    for file in files:
        try:
            os.remove(dest_dir + os.sep + file)
        except:
            pass
    
    for file in files:
        shutil.move(file, dest_dir)
    
    print('Done.\n')
    
    return 