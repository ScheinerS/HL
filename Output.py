#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Este módulo lee las salidas de HL y crea un único archivo con los ID de las simulaciones y los datos de interés..
"""
import pandas as pd
import numpy as np
import os
import sys
#from io import StringIO
import re
from datetime import datetime

import glob
import check_dir as cd

def create_output(path_HE60, path, path_printouts, Id_min, Id_max, Tag, Comment, Output_file_name, theta_view, phi_view):
    
    print('theta_view = %g,\tphi_view = %g'%(theta_view, phi_view))    
    cd.check_dir(path + os.sep + 'Outputs')
    
    # Sheet 0:
    #%%
    date = datetime.today().strftime('%Y-%m-%d')
    
    Sheets = {'Tag': [Tag],
              'Comment': [Comment],
              'Date': [date],
              'Sheet': ['Description'],
              'INPUTS': ['Variables used when setting up H5 input files'],
              'ALL_rhow': ['Rhow reflectance'],
              'ALL_a_nw': ['Total absorption (a_pig + a_nap + a_cdom)'],
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

    I = pd.read_excel(path + os.sep + 'Inputs/Id_%s.xlsx'%Tag, engine = 'openpyxl')
    print(Tag)
    
    for Id in range(Id_max):
        print('\r%4d/%4d'%(Id+1, Id_max), end='')

        # Creamos la columna 'Id':
        for df in DF:
            df.loc[Id, 'Id'] = str('%04d'%Id)
        
        ########
        
        # Sheet 1:
        
        INPUTS.loc[Id, 'Id'] = str('%04d'%Id)
        INPUTS.loc[Id, 'CHL'] = I['CHL'].at[Id]
        INPUTS.loc[Id, 'NAP'] = I['NAP'].at[Id]
        INPUTS.loc[Id, 'CDOM'] = I['CDOM'].at[Id]
        INPUTS.loc[Id, 'a*_NAP(443)'] = I['a*_NAP(443)'].at[Id]
        INPUTS.loc[Id, 'S_NAP'] = I['S_NAP'].at[Id]
        INPUTS.loc[Id, 'S_CDOM'] = I['S_CDOM'].at[Id]
        INPUTS.loc[Id, 'GAMMA_C_NAP'] = I['GAMMA_C_NAP'].at[Id]
        INPUTS.loc[Id, 'SPF_FF_BB_B_NAP'] = I['SPF_FF_BB_B_NAP'].at[Id]
        INPUTS.loc[Id, 'SPF_FF_BB_B_CHL'] = I['SPF_FF_BB_B_CHL'].at[Id]        
        
        # Proot:
        FILE = path_printouts + os.sep +'P%04d_%s.txt'%(Id, Tag)
        #print(FILE)
        with open(FILE, "r") as file:
            S = file.read() # String con todo el contenido del TXT.
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
                a = re.sub(' +', ' ', a)
                a = re.sub(' +', ';', a)
                
                a_df = pd.DataFrame([x.split(';') for x in a.split('\n')])
                
                # Header:
                new_header = a_df.iloc[0] #grab the first row for the header
                a_df = a_df[1:] #take the data less the header row
                a_df.columns = new_header
                
                # Selección de ángulos de observación:
                
                # theta_view = 40
                # phi_view = 135
                
                a_df['Theta'] = a_df['Theta'].astype(float)
                a_df['Phi-view'] = a_df['Phi-view'].astype(float)
                
                a_df = a_df[a_df['Theta']==theta_view]
                a_df = a_df[a_df['Phi-view']==phi_view]

                Rrs = float(a_df['Rrs']) #float(a[4])
                rhow = np.pi*Rrs
                
                # Lo guardamos en el DataFrame:
                ALL_rhow.loc[Id, wavelength] = rhow
        #%%    
        ########
        
        # Droot:
        FILE = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'digital' + os.sep + 'D%04d_%s.txt'%(Id, Tag)
        #print(FILE)
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

    #######
    
    # Guardamos los DataFrames en el Excel:
    
    output_filename = path + os.sep + 'Outputs' + os.sep + Output_file_name + '_vaz%dvphi%d'%(theta_view, phi_view) + '.xlsx'
    
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

if __name__=='__main__':
    
    '''
    ESTE BLOQUE SE UTILIZA DE FORMA MANUAL PARA GENERAR OTRO ARCHIVO DE
    SALIDA SIN CORRER LAS SIMULACIONES NUEVAMENTE.
    '''
    
    # para generar la salida nuevamente con otros ángulos de observación:
    # Tag = 'Tesis_v7'
    # Tag = 'AD_CCRR'
    Tag = 'PRUEBA'
    
    path = os.path.dirname(os.path.realpath('__file__'))
    sys.path.append(path)
    
    path_inputs = path + os.sep + 'Inputs'
    
    Inputs = pd.read_excel(path_inputs + os.sep + 'Inputs_%s.xlsx'%Tag, engine = 'openpyxl')
    
    Comment = Inputs['Comentario'][0]
    
    path_HE60 = path.split(os.sep)
    del path_HE60[len(path_HE60)-1]
    path_HE60 = os.sep.join(path_HE60) + os.sep + 'HE60'

    # path_printouts = "/home/santiago/Documents/HE60/output/HydroLight/"
    path_printouts = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'printout' 
    # path = "/home/santiago/Documents/tesis/HL/"
    
    Output_filename = 'Output_' + Tag # Nombre para el archivo de salida.
    
    files = glob.glob(path_printouts + os.sep + 'P*' + Tag + '.txt')
    
    Id_min = 0
    Id_max = len(files)
    
    # [theta_view, phi_view] = [40, 135] # tesis
    [theta_view, phi_view] = [0, 0] # Nechad et al. (2010) corregido.
    # [theta_view, phi_view] = [0, 90] # Nechad et al. (2010) no existe.    

    # ATENCIÓN: NO TODOS LOS PARES (theta_view, phi_view) SON POSIBLES.
    # LA LISTA DE LAS POSIBILIDADES ESTÁN EN LOS ARCHIVOS DE PRINTOUT.
    # theta_view = 0 # posible: 0, 10, 20, 30, 40, 50, 60, 70, 80, 87.5.
    # phi_view = 0 # posible: 0, 90 135, 180.
    
    create_output(path_HE60, path, path_printouts, Id_min, Id_max, Tag, Comment, Output_filename, theta_view, phi_view)