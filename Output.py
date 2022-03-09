#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Este módulo lee las salidas de HL y crea un único archivo con los ID de las simulaciones y los datos de interés..
"""
import pandas as pd
import numpy as np
import os
import sys
import re
from datetime import datetime
# import matplotlib.pyplot as plt

import glob
import check_dir as cd

#%%
def check_warnings(WARNINGS, Id, S):
    
    S = S.split('***** BEGIN WARNING MESSAGES FOR INPUT DATA FILES *****')[1]
    S = S.split('***** END WARNING MESSAGES FOR INPUT DATA FILES *****')[0]
    S = re.sub('\n', '', S).strip()
    
    if not (S == 'No files were read with data ranges less than the run depth and wavelength ranges.'):
        WARNINGS.loc[Id, 'Warnings'] = S
    
#%%
def create_output(path_HE60, path, path_printouts, Tag, Comment, theta_view, phi_view):
    #%%
    print('\ntheta_view = %g,\tphi_view = %g'%(theta_view, phi_view))
    cd.check_dir(path + os.sep + 'Outputs')
    
    Output_file_name = 'Output_' + Tag # Nombre para el archivo de salida.
    output_filename = path + os.sep + 'Outputs' + os.sep + Output_file_name + '_vaz%dvphi%d'%(theta_view, phi_view) + '.xlsx'
    
    # Chequeo de sobreescritura:
    # output_file = path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '.xlsx'
    is_file = os.path.isfile(output_filename)
    if is_file:
        print('\n"%s" already exists.'%output_filename)
        input('Overwrite (ENTER)?')     
    
    # files = glob.glob(path_printouts + os.sep + 'P*_' + Tag + '.txt')
    # Id_max = len(files)
    
    files = sorted(glob.glob(path_printouts + os.sep + Tag + os.sep + 'P*' + Tag + '.txt'))

    Id_min = 0
    Id_max = int(files[-1].split('.')[0].split(os.sep)[-1].split('_')[0].strip('P'))
    
    # Sheet 0:
    
    date = datetime.today().strftime('%Y-%m-%d')
    
    Sheets = {'Tag': [Tag],
              'Comment': [Comment],
              'Date': [date],
              'Sheet': ['Description'],
              'INPUTS': ['Variables used when setting up H6 input files'],
              'ALL_rhow': ['Rhow reflectance'],
              'ALL_a_nw': ['Total absorption (a_chl + a_nap + a_cdom)'],
              'ALL_a_chl': ['CHL absorption'],
              'ALL_a_cdom': ['CDOM absorption'],
              'ALL_a_nap': ['NAP absorption'],
              'ALL_b_p': ['Total scattering (b_chl + b_nap)'],
              'ALL_b_chl': ['CHL scattering'],
              'ALL_b_nap': ['NAP scattering'],
              'ALL_bb_p': ['Total backscattering (bb_chl + bb_nap)'],
              'ALL_bb_chl': ['CHL backscattering'],
              'ALL_bb_nap': ['NAP backscattering']}
    
    README = pd.DataFrame.from_dict(Sheets, orient='index')
    README.columns = ['']
    #######
    INPUTS = pd.DataFrame()    
    #######
    ALL_rhow = pd.DataFrame()
    ALL_a_nw = pd.DataFrame()
    ALL_a_chl = pd.DataFrame()
    ALL_a_cdom = pd.DataFrame()
    ALL_a_nap = pd.DataFrame()
    ALL_b_p = pd.DataFrame()
    ALL_b_chl = pd.DataFrame()
    ALL_b_nap = pd.DataFrame()
    ALL_bb_p = pd.DataFrame()
    ALL_bb_chl = pd.DataFrame()
    ALL_bb_nap = pd.DataFrame()
    #######
    
    DF = [ALL_rhow, ALL_a_nw, ALL_a_chl, ALL_a_cdom, ALL_a_nap, ALL_b_p, ALL_b_chl, ALL_b_nap, ALL_bb_p, ALL_bb_chl, ALL_bb_nap]
    
    #WAVELENGTHS = np.arange(350,952.5, 2.5)

    I = pd.read_excel(path + os.sep + 'Inputs' + os.sep + 'Id_%s.xlsx'%Tag, engine = 'openpyxl')
    print(Tag)
    
    WARNINGS = pd.DataFrame()
    RUN_TIMES = pd.DataFrame()
    
    RUN_TIMES['Id'] = None
    RUN_TIMES['Run time'] = None
    
    MISSING = []
    
    for Id in range(Id_min, Id_max):
        print('\r%4d/%4d'%(Id+1, Id_max), end='')

        # Creamos la columna 'Id':
        for df in DF:
            df.loc[Id, 'Id'] = str('%04d'%Id)
        
        ########
        
        # Sheet 1:
        
        INPUTS.loc[Id, 'Id'] = str('%04d'%Id)
        
        for var in I.columns:
            INPUTS.loc[Id, var] = I[var].at[Id]
        
        # Proot:
        FILE = path_printouts + os.sep + Tag + os.sep +'P%04d_%s.txt'%(Id, Tag)
        
        try:
            with open(FILE, "r") as file:
                S = file.read() # String con todo el contenido del TXT.
                
                # Búsqueda de warnings:
                check_warnings(WARNINGS, Id, S)
                
                run_time = float(S.split('Total (wall clock) run time =')[1].split('sec')[0].strip())
                RUN_TIMES.loc[Id, 'Id'] = Id
                RUN_TIMES.loc[Id, 'Run time'] = run_time/60
                
                # Comienzo de los bloques:
                S = S.split('Output for wavelength band') # El TXT queda dividido en bloques S[i].
                
                ########
    
                # Sheet 2:
                
                for i in range(1, len(S)):
                    # Longitud de onda del bloque i:
                    wavelength = float(S[i].split('nominal wavelength =  ')[1].split(' ')[0])
                    
                    # Tabla con reflectancias:
                    a = S[i].split('Phi = 45 represents the 135 degree viewing angle for minimizing sun glitter.]\n\n')[1].strip(' ') # desde
                    a = a.split('K-functions')[0].strip(' ') # hasta
    
                    lines = a.split('\n')
                    # Eliminación de los espacios al comienzo de cada línea:
                    for j in range(len(lines)):
                        lines[j] = lines[j].strip()
                    
                    a = '\n'.join(lines)
                    a = re.sub('total up', 'total-up', a)
                    a = re.sub(' +', ' ', a)
                    a = re.sub(' +', ';', a)
                    
                    a_df = pd.DataFrame([x.split(';') for x in a.split('\n')])
                    
                    # Header:
                    new_header = a_df.iloc[0]
                    a_df = a_df[1:]
                    a_df.columns = new_header
                    
                    # Selección de ángulos de observación:
                    
                    a_df['Theta'] = a_df['Theta'].astype(float)
                    a_df['Phi-view'] = a_df['Phi-view'].astype(float)
                    
                    a_df = a_df[a_df['Theta']==theta_view]
                    a_df = a_df[a_df['Phi-view']==phi_view]
    
                    Rrs = float(a_df['Rrs']) #float(a[4])
                    rhow = np.pi*Rrs
                    
                    # Lo guardamos en el DataFrame:
                    ALL_rhow.loc[Id, wavelength] = rhow
        except:
            MISSING.append(Id)
            continue
        # Droot:
        FILE = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'digital' + os.sep + Tag + os.sep + 'D%04d_%s.txt'%(Id, Tag)
        try:
            with open(FILE, "r") as file:
                S = file.read() # String con todo el contenido del TXT.
                
                # Comienzo de los bloques:
                S = S.split('at nominal wavelength =') # El TXT queda dividido en bloques S[i].
                for i in range(1, len(S)):
                    
                    # Wavelength:
                    
                    w = S[i].split('\n')[0].strip(' ')
                    wavelength = float(w)
                    
                    # Absorption (a):
                    
                    a_chl = S[i].split('acoef (for component  2)')[1]
                    a_chl = a_chl.split('acoef (for component  3)')[0].strip()
                    a_chl = float(a_chl)
    
                    a_cdom = S[i].split('acoef (for component  3)')[1]
                    a_cdom = a_cdom.split('acoef (for component  4)')[0].strip()
                    a_cdom = float(a_cdom)
                    
                    a_nap = S[i].split('acoef (for component  4)')[1]
                    a_nap = a_nap.split('bcoef')[0].strip()
                    a_nap = float(a_nap)
    
                    a_nw = a_chl + a_cdom + a_nap #a[7] # Total sin agua.
                    
                    # Lo guardamos en el DataFrame:
                    ALL_a_chl.loc[Id, wavelength] = a_chl
                    ALL_a_cdom.loc[Id, wavelength] = a_cdom
                    ALL_a_nap.loc[Id, wavelength] = a_nap
                    ALL_a_nw.loc[Id, wavelength] = a_nw
    
                    ########
                    
                    # Scattering (b):
                    
                    b_chl = S[i].split('bcoef (for component  2)')[1]
                    b_chl = b_chl.split('bcoef (for component  3)')[0].strip()
                    b_chl = float(b_chl)
    
                    b_cdom = S[i].split('bcoef (for component  3)')[1]
                    b_cdom = b_cdom.split('bcoef (for component  4)')[0].strip()
                    b_cdom = float(b_cdom)
                    
                    b_nap = S[i].split('bcoef (for component  4)')[1]
                    b_nap = b_nap.split('bbcoef')[0].strip()
                    b_nap = float(b_nap)
                    
                    b_p = b_chl + b_cdom + b_nap # Total sin agua.
                    
                    # Lo guardamos en el DataFrame:
                    ALL_b_chl.loc[Id, wavelength] = b_chl
                    ALL_b_nap.loc[Id, wavelength] = b_nap
                    ALL_b_p.loc[Id, wavelength] = b_p
                    
                    ########
                    
                    # Backscattering (bb):
                        
                    bb_chl = S[i].split('bbcoef (for component  2)')[1]
                    bb_chl = bb_chl.split('bbcoef (for component  3)')[0].strip()
                    bb_chl = float(bb_chl)
    
                    bb_cdom = S[i].split('bbcoef (for component  3)')[1]
                    bb_cdom = bb_cdom.split('bbcoef (for component  4)')[0].strip()
                    bb_cdom = float(bb_cdom)
                    
                    bb_nap = S[i].split('bbcoef (for component  4)')[1]
                    bb_nap = bb_nap.split('atten')[0].strip()
                    bb_nap = float(bb_nap)
                    
                    bb_p = bb_chl + bb_cdom + bb_nap # Total sin agua
           
                    # Lo guardamos en el DataFrame:
                    ALL_bb_chl.loc[Id, wavelength] = bb_chl
                    ALL_bb_nap.loc[Id, wavelength] = bb_nap
                    ALL_bb_p.loc[Id, wavelength] = bb_p
        except:
            continue
    #######
    
    RUN_TIMES.to_csv(path + os.sep + 'Outputs' + os.sep + Output_file_name + '.csv')
    

    
    # Guardamos los DataFrames en el Excel:
    
    print('\nOutput file:', output_filename)
    
    writer = pd.ExcelWriter(output_filename, engine='openpyxl')
    
    README.to_excel(writer, sheet_name='README', header=True)#, index=False)
    INPUTS.to_excel(writer, sheet_name='INPUTS', header=True, index=False)
    
    ALL_rhow.to_excel(writer, sheet_name='All_rhow', header=True, index=False)
    
    ALL_a_nw.to_excel(writer, sheet_name='ALL_a_nw', header=True, index=False)
    ALL_a_chl.to_excel(writer, sheet_name='ALL_a_chl', header=True, index=False)
    ALL_a_cdom.to_excel(writer, sheet_name='ALL_a_cdom', header=True, index=False)
    ALL_a_nap.to_excel(writer, sheet_name='ALL_a_nap', header=True, index=False)
    
    ALL_b_p.to_excel(writer, sheet_name='ALL_b_p', header=True, index=False)
    ALL_b_chl.to_excel(writer, sheet_name='ALL_b_chl', header=True, index=False)
    ALL_b_nap.to_excel(writer, sheet_name='ALL_b_nap', header=True, index=False)
    
    ALL_bb_p.to_excel(writer, sheet_name='ALL_bb_p', header=True, index=False)
    ALL_bb_chl.to_excel(writer, sheet_name='ALL_bb_chl', header=True, index=False)
    ALL_bb_nap.to_excel(writer, sheet_name='ALL_bb_nap', header=True, index=False)
    
    writer.save()
    print('\nDone.')
    
    print('WARNINGS:\n', WARNINGS)        
    print('MISSING:\n', MISSING)

#%%
if __name__=='__main__':
    
    '''
    ESTE BLOQUE SE UTILIZA DE FORMA MANUAL PARA GENERAR OTRO ARCHIVO DE
    SALIDA SIN CORRER LAS SIMULACIONES NUEVAMENTE.
    '''
    
    # para generar la salida nuevamente con otros ángulos de observación:
    Tag = 'Tesis_v7'
    # Tag = 'AD_CCRR'
    # Tag = 'PRUEBA'
    # Tag = 'v8'
    
    path = os.path.dirname(os.path.realpath('__file__'))
    sys.path.append(path)
    
    path_inputs = path + os.sep + 'Inputs'
    
    Inputs = pd.read_excel(path_inputs + os.sep + 'Input_%s.xlsx'%Tag, engine = 'openpyxl')
    
    Comment = Inputs['Comentario'][0]
    
    path_HE60 = path.split(os.sep)
    del path_HE60[len(path_HE60)-1]
    path_HE60 = os.sep.join(path_HE60) + os.sep + 'HE60'

    path_printouts = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'printout' 
    
    # Output_filename = 'Output_' + Tag # Nombre para el archivo de salida.
    
    # files = sorted(glob.glob(path_printouts + os.sep + 'P*' + Tag + '.txt'))

    # Id_min = 0
    # Id_max = int(files[-1].split('.')[0].split(os.sep)[-1].split('_')[0].strip('P'))
    
    #[theta_view, phi_view] = [40, 135] # tesis
    # [theta_view, phi_view] = [0, 0] # Nechad et al. (2010).
    # Angles = [[0, 0], [40, 135]]
    Angles = [[40, 135]]
    
    for a in Angles:
        [theta_view, phi_view] = [a[0], a[1]]
        create_output(path_HE60, path, path_printouts, Tag, Comment, theta_view, phi_view)
    