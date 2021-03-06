#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Para graficar las salidas de HydroLight.
"""

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import rcParams, cycler
import check_dir as cd

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.close('all')

def Graficar(path, Tag, theta_view, phi_view, **save):
    #filename = path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '_vaz%dvphi%d'%(theta_view, phi_view) + '.xlsx'
    # filename = path + '/Outputs/Output_v8_no_fl_vaz40vphi135_000000-000400.xlsx'
    filename = path + '/Outputs/Output_v8_vaz40vphi135_000000-000400.xlsx'
    xl = pd.ExcelFile(filename)
    xl.sheet_names # see all sheet names
    sheets = xl.sheet_names[2:]
    
    for sheet in sheets:
        #sheet = 'ALL_rhow'
        DATA = pd.read_excel(filename, engine = 'openpyxl', sheet_name=sheet)
        DATA.drop('Id', axis=1, inplace=True)
        wavelength = list(DATA.columns)
    
        i_max = len(DATA)
        
        # Colores:
        cmap = plt.cm.jet #coolwarm, viridis, plasma, inferno, magma, cividis
        rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, i_max+1)))
        
        plt.figure()
        for i in range(i_max):
            if i%10==0:
                plt.plot(wavelength, DATA.iloc[i], label=r'%d'%i)
            else:
                plt.plot(wavelength, DATA.iloc[i])
    
        plt.xlabel(r'$\lambda$')
        plt.ylabel(r'%s'%sheet.split('_')[1])
        plt.title(r'%s [%s]'%(sheet.replace('_', ' '), Tag))
        #plt.legend()
        plt.grid()
        plt.show()
        if save:
            path = os.path.dirname(os.path.realpath('__file__'))
            sys.path.append(path)
            cd.check_dir(path + os.sep + 'Graficos')
            save_path = path + os.sep + 'Graficos' + os.sep + 'RAW'
            cd.check_dir(save_path)
            plt.savefig(save_path + os.sep + '%s_%s_vaz%dvphi%d.png'%(Tag, sheet, theta_view, phi_view))
        plt.close('all')

if __name__=='__main__':
        
    path = os.path.dirname(os.path.realpath('__file__'))
    sys.path.append(path)
    
    # Tag = 'AD_CCRR'
    # Tag = 'Tesis_v7'
    Tag = 'v8'
    
    # Angles = [[0, 0], [40, 135]]
    # Angles = [[0, 0]]
    Angles = [[40, 135]]
    
    for a in Angles:
        [theta_view, phi_view] = [a[0], a[1]]
        Graficar(path, Tag, theta_view, phi_view, save=False)
