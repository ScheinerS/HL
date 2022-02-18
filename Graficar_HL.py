#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Para graficar las salidas de HydroLight.
"""

import pandas as pd
import numpy as np
#from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import rcParams, cycler

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.close('all')

def Graficar(Tag, **save):
    filename = 'Outputs/Output_%s.xlsx'%Tag
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
        cmap = plt.cm.viridis #coolwarm, viridis, plasma, inferno, magma, cividis
        rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, i_max+1)))
        
        plt.figure()
        for i in range(i_max):
            if i%10==0:
                plt.plot(wavelength, DATA.iloc[i], label=r'%d'%i)
            else:
                plt.plot(wavelength, DATA.iloc[i])
    
        plt.xlabel(r'$\lambda$')
        plt.ylabel(r'%s'%sheet.split('_')[1])
        plt.title(r'%s'%sheet.replace('_', ' '))
        #plt.legend()
        plt.grid()
        plt.show()
    
        plt.savefig('Graficos/Gráficos del output/%s_%s.png'%(Tag, sheet))
        #plt.pause(1)
        
    plt.close('all')


if __name__=='__main__':
    Tag = 'Tesis_v1'
    Graficar(Tag)
