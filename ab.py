'''
Arma los archivos de 'a' y 'b' correspondientes a CHL y NAP.
'''

import numpy as np
import pandas as pd
import sys
import os
#from scipy.interpolate import interp1d

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

def Voss_1992(l, CHL):
    c_660= 0.314*(CHL**0.57)    # Voss 1992

    if(CHL==0):
        c_star = l*0
    else:
        if(CHL<2):
            v = 0.5*(np.log10(CHL)-0.3)
        else:
            v = 0
    
        c = c_660 * (l/660)**v
    
        c_star = c/CHL
    
    return c_star

def Morel_2002(l, CHL):
    c_660 = 0.407*(CHL**0.795)  # Morel 2002

    if(CHL==0):
        c_star = l*0
    else:
        if(CHL<2):
            v = 0.5*(np.log10(CHL)-0.3)
        else:
            v = 0
    
        c = c_660 * (l/660)**v
    
        c_star = c/CHL
    
    return c_star


def save_to_file(filename, x, y):

    DF = pd.DataFrame()
    DF[0] = x
    DF[1] = y
    
    # No quitar el encabezado. Hydrolight remueve las primeras diez líneas de datos si no encuentra encabezado en el archivo. Ver sección 7, pág. 65 de la TechDoc.
    header = '\\begin_header \end_header'
    
    DF.to_csv('DATA/' + filename + '.txt', sep='\t', index=False, header=[header, ''])
    
    return


#%%

def create_data_files(Id, CHL, NAP, CDOM, ASTAR_NAP_443, Bstar_NAP_555, S_NAP, S_CDOM, GAMMA_C_NAP):
    
    ############################    
    # CHL:
    
    midUVabs = pd.read_csv('data' + os.sep + 'AE_midUVabs.txt', sep='    ', skiprows=11)
    midUVabs.columns = ['lambda', 'A', 'E']
    midUVabs.drop(205, inplace=True)
    
    wavelength_CHL = midUVabs['lambda']
    a_CHL = midUVabs['A']*CHL**midUVabs['E']
    if CHL>0:
        a_star_CHL = a_CHL/CHL
    else:
        a_star_CHL = a_CHL

    c_star_CHL = Voss_1992(wavelength_CHL, CHL)
    
    b_star_CHL = c_star_CHL - a_star_CHL
    
    # Fin del archivo:
    a_star_CHL = np.append(a_star_CHL, -1)
    b_star_CHL = np.append(b_star_CHL, -1)
    
    ############################
    
    # NAP:
    wavelength_NAP = np.arange(300, 1002.5, 2.5)
    
    # a:
    a_443 = ASTAR_NAP_443
    a_star_NAP = a_443 * np.exp(S_NAP*(wavelength_NAP-443))
    
    # b:
    a_555 = a_443 * np.exp(S_NAP*(555-443))
    b_555 = Bstar_NAP_555 # m^2/g - Nechad et al. (2015), tabla 11.
    c_555 = a_555 + b_555
    
    c_star_NAP = c_555 * ((wavelength_NAP/555)**(GAMMA_C_NAP))
    
    b_star_NAP = c_star_NAP - a_star_NAP
    
    
    a_star_NAP = np.append(a_star_NAP, -1)
    b_star_NAP = np.append(b_star_NAP, -1)
    
    ############################
    
    # CDOM:
    
    # Comentado porque se utiliza la exponencial en HLBatchruns.py directamente:
    '''
    wavelength_CDOM = np.arange(350, 950, 2.5)
    
    a_443 = 1   # Completar. Ver Babin 2003a.
    a_star_CDOM = a_443 * np.exp(S_CDOM*(wavelength_CDOM-443))
    
    b_star_CDOM = np.zeros(len(wavelength_CDOM))
    
    a_star_CDOM = np.append(a_star_CDOM, -1)
    b_star_CDOM = np.append(b_star_CDOM, -1)
    '''
    ############################
    
    wavelength_CHL = np.append(wavelength_CHL, -1)
    wavelength_NAP = np.append(wavelength_NAP, -1)
    # wavelength_CDOM = np.append(wavelength_CDOM, -1)
    ############################
    
    filename = str(Id)
    
    save_to_file(filename + '_astar_CHL', wavelength_CHL, a_star_CHL)
    save_to_file(filename + '_bstar_CHL', wavelength_CHL, b_star_CHL)
    
    save_to_file(filename + '_astar_NAP', wavelength_NAP, a_star_NAP)
    save_to_file(filename + '_bstar_NAP', wavelength_NAP, b_star_NAP)
    
    #save_to_file(filename + '_astar_CDOM', wavelength_CDOM, a_star_CDOM)
    #save_to_file(filename + '_bstar_CDOM', wavelength_CDOM, b_star_CDOM)

#%%

if __name__ == "__main__":

    # Valores de prueba:
    # Tag = 'Prueba_tag_ab'
    Id = '12345'
    CHL = 0
    NAP = 1
    CDOM = 1
    ASTAR_NAP_443 = 0.04
    Bstar_NAP_555 = 0.51
    S_NAP = -0.0123
    S_CDOM = -0.0176
    GAMMA_C_NAP = -0.3749
    
    create_data_files(Id, CHL, NAP, CDOM, ASTAR_NAP_443, Bstar_NAP_555, S_NAP, S_CDOM, GAMMA_C_NAP)