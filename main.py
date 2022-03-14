import numpy as np
import pandas as pd
import sys
import os
import shutil
import itertools

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

#%%
import ab
import HLbatchruns as hlb
import transfer_files as tf
import Output as op
import check_dir as cd
import Graficar_HL as ghl

#%%

# Flags:
CREATE_BATCHRUN_FILES = 0
RUN = 1
CREATE_OUTPUT = 0
PLOT = 0

#%%
# Verificación del directorio HE60:
path_HE60 = path.split(os.sep)
del path_HE60[len(path_HE60)-1]
path_HE60 = os.sep.join(path_HE60) + os.sep + 'HE60'

cd.check_dir_HE60(path_HE60)
cd.check_dir(path_HE60 + os.sep + 'data' + os.sep + 'DATA_SS')

#%%
Inputs = pd.read_excel('Input.xlsx', engine = 'openpyxl')

Tag = Inputs['Etiqueta'][0]
Comment = Inputs['Comentario'][0]

# Id inicial:
Id_start = Inputs['Id_start'][0]

# Límites para las simulaciones:
Id_min_run = Inputs['Id_min_run'][0]
Id_max_run = Inputs['Id_max_run'][0]

# Back up del Input:
path_inputs = path + os.sep + 'Inputs'
cd.check_dir(path_inputs)
shutil.copyfile('Input.xlsx', path_inputs + os.sep + 'Input_%s.xlsx'%Tag)

def geometric_progression(start, stop, factor):
    # Geometric progression starting at from 'start' to 'stop' where a(i+1)=factor*a(i).
    N = int(np.log(stop/start)/np.log(factor))+1 # cantidad necesaria de valores.
    u = np.empty(N+1,)
    u[0] = start
    u[1:] = factor
    gp = np.cumprod(u)
    gp = np.append(0,gp)
    return gp
    
# Bloque para reconocer pasos no regulares en el barrido:

CHL_steps = str(Inputs['CHL_factor'][0]).split(',')
if len(CHL_steps)>1:
    # Conversion a float:
    for i in range(0, len(CHL_steps)):
        CHL_steps[i] = float(CHL_steps[i])
    # Asignación del vector:
    CHL = CHL_steps
else:
    CHL = geometric_progression(Inputs['CHL_min'][0], Inputs['CHL_max'][0], Inputs['CHL_factor'][0])


NAP_steps = str(Inputs['NAP_factor'][0]).split(',')
if len(NAP_steps)>1:
    # Conversion a float:
    for i in range(0, len(NAP_steps)):
        NAP_steps[i] = float(NAP_steps[i])
    # Asignación del vector:
    NAP = NAP_steps
else:
    NAP = geometric_progression(Inputs['NAP_min'][0], Inputs['NAP_max'][0], Inputs['NAP_factor'][0])


CDOM_steps = str(Inputs['CDOM443_factor'][0]).split(',')
if len(CDOM_steps)>1:
    # Conversion a float:
    for i in range(0, len(CDOM_steps)):
        CDOM_steps[i] = float(CDOM_steps[i])
    # Asignación del vector:
    CDOM = CDOM_steps
else:
    CDOM = geometric_progression(Inputs['CDOM443_min'][0], Inputs['CDOM443_max'][0], Inputs['CDOM443_factor'][0])
        
#%%
A_c_star_660 = [Inputs['A_c_phy_star_660'][0]]
E_c_star_660 = [Inputs['E_c_phy_star_660'][0]]
Astar_NAP_443 = [Inputs['Astar_NAP_443'][0]]
Astar_NAP_offset = [float(i) for i in str(Inputs['Astar_NAP_offset'][0]).split(',')]
Bstar_NAP_555 = [Inputs['Bstar_NAP_555'][0]]
S_NAP = [Inputs['S_NAP'][0]]
GAMMA_C_NAP = [Inputs['GAMMA_C_NAP'][0]]
S_CDOM = [Inputs['S_CDOM'][0]]
SPF_FF_BB_B_NAP = [float(i) for i in str(Inputs['SPF_FF_BB_B_NAP'][0]).split(',')]
SPF_FF_BB_B_CHL = [float(i) for i in str(Inputs['SPF_FF_BB_B_CHL'][0]).split(',')]

suntheta = [Inputs['suntheta'][0]]
sunphi = [Inputs['sunphi'][0]]

theta_view = [Inputs['theta_view'][0]]
phi_view = [Inputs['phi_view'][0]]

cloud = [Inputs['cloud'][0]]
windspeed = [Inputs['windspeed'][0]]

fluorescence = [Inputs['fluorescence'][0]]

# Conversión a float:
def values_to_float(LIST):
    LIST = LIST[0].split(',')
    for i in range(0, len(LIST)):
        LIST[i] = float(LIST[i])

    return LIST


if type(S_CDOM[0])==str:
    S_CDOM = values_to_float(S_CDOM)

# S_CDOM_steps = str(Inputs['CDOM443_factor'][0]).split(',')


#%%

combination = list(itertools.product(CHL, NAP, CDOM, A_c_star_660, E_c_star_660, Astar_NAP_443, Astar_NAP_offset, Bstar_NAP_555, S_NAP, GAMMA_C_NAP, S_CDOM, SPF_FF_BB_B_NAP, SPF_FF_BB_B_CHL, suntheta, sunphi, cloud, windspeed, fluorescence))

Id_start = int(Id_start)

Id_max = Id_start + len(combination)

if pd.isna(Id_start):
    Id_start = 0

if pd.isna(Id_min_run):
    Id_min_run = 0

if pd.isna(Id_max_run):
    Id_max_run = Id_max

Id_min_run = int(Id_min_run)
Id_max_run = int(Id_max_run)

# Corrección en caso de que Id_max_run>Id_max:
Id_max_run = min(Id_max_run, Id_max)

#%%

# Printout de los valores para verificar la configuración:
print(50*'-')

print('CREATE_BATCHRUN_FILES:\t', CREATE_BATCHRUN_FILES)
print('RUN:\t', RUN)
print('CREATE_OUTPUT:\t', CREATE_OUTPUT)
print('PLOT:\t', PLOT)

print(50*'-')

print('Tag:\t', Tag)
print('Comment:\t', Comment)

print(50*'-')

print('Id_min_run:\t%6d'%Id_min_run)
print('Id_max_run:\t%6d'%Id_max_run)

print(50*'-')

print('\nCHL (%d values):\t'%len(CHL), CHL)
print('\nCDOM (%d values):\t'%len(CDOM), CDOM)
print('\nNAP (%d values):\t'%len(NAP), NAP)

print(50*'-')

print('\Astar_NAP_443:\t', Astar_NAP_443)
print('\nAstar_NAP_offset:\t', Astar_NAP_offset)
print('\nBstar_NAP_555:\t', Bstar_NAP_555)
print('\nS_NAP:\t', S_NAP)
print('\nGAMMA_C_NAP:\t', GAMMA_C_NAP)
print('\nS_CDOM:\t', S_CDOM)

print(50*'-')

print('\nSPF_FF_BB_B_NAP:\t', SPF_FF_BB_B_NAP)
print('\nSPF_FF_BB_B_CHL:\t', SPF_FF_BB_B_CHL)

print(50*'-')

print('\n(suntheta, sunphi):\t', suntheta, sunphi)
print('\n(theta_view, phi_view):\t', theta_view, phi_view)
print('\ncloud:\t', cloud)
print('\nwindspeed:\t', windspeed)

print(50*'-')

print('\nfluorescence:\t', fluorescence)

print(50*'-')

def continuar():
    X = input('Continue (y/n)?')
    if X == 'y':
        print()
    elif X == 'n':
        sys.exit()
    else:
        continuar()

continuar()
#%%

DF = pd.DataFrame()

DF['Id'] = None
DF['CHL'] = None
DF['NAP'] = None
DF['CDOM'] = None
DF['A_c_phy_star_660'] = None
DF['E_c_phy_star_660'] = None
DF['a*_NAP(443)'] = None
DF['Astar_NAP_offset'] = None
DF['Bstar_NAP_555'] = None
DF['S_NAP'] = None
DF['GAMMA_C_NAP'] = None
DF['S_CDOM'] = None
DF['SPF_FF_BB_B_NAP'] = None
DF['SPF_FF_BB_B_CHL'] = None
DF['suntheta'] = None
DF['sunphi'] = None
DF['cloud'] = None
DF['windspeed'] = None
DF['fluorescence'] = None

#%%
# Creamos los archivos de a y b para cada componente (CHL, NAP, CDOM):

if CREATE_BATCHRUN_FILES:
    for Id in range(Id_start, Id_max):

        print('\r%4d'%(Id+1), end='')
        
        line = [str('%06d'%Id)]
        line.extend(list(combination[Id-Id_start]))
        
        DF.at[Id] = line
        
        chl = line[1]
        nap = line[2]
        cdom = line[3]
        a_c_star_660 = line[4]
        e_c_star_660 = line[5]
        astar_nap_443 = line[6]
        astar_nap_offset = line[7]
        bstar_nap_555= line[8]
        s_nap = line[9]
        gamma_c_nap = line[10]
        s_cdom = line[11]
        spf_ff_bb_b_nap = line[12]
        spf_ff_bb_b_chl = line[13]
        suntheta = line[14]
        sunphi = line[15]
        cloud = line[16]
        windspeed = line[17]
        fluorescence = line[18]
        
        ab.create_data_files(str('%06d'%Id), chl, nap, cdom, a_c_star_660, e_c_star_660, astar_nap_443, astar_nap_offset, bstar_nap_555, s_nap, s_cdom, gamma_c_nap)
        
        hlb.create_batchrun_file(path_HE60, Id, Tag, Comment, chl, cdom, nap, s_cdom, spf_ff_bb_b_nap, spf_ff_bb_b_chl, suntheta, sunphi, cloud, windspeed, fluorescence)
    
    # Archivo de Id:
    cd.check_dir(path + os.sep + 'Inputs')
    DF.to_excel(path + os.sep + 'Inputs' + os.sep + 'Id_%s.xlsx'%Tag, index = False)
#%%

# Transferencia de los archivos:
    
# Batchruns:
path_batchruns = path + os.sep + 'batchruns'
cd.check_dir(path_batchruns)
tf.transfer(path_batchruns, path_HE60 + os.sep + 'run/batch')

# Datos de a y b:
#path_ab = path + os.sep +'/DATA'
#cd.check_dir(path_ab)
tf.transfer(path + os.sep + 'DATA', path_HE60 + os.sep + 'data/DATA_SS')


#%%

if RUN:    
    dest_dir = path_HE60 + os.sep + 'backend'
    os.chdir(dest_dir)
    for Id in range(Id_min_run, Id_max_run):
        # print('\r%4d'%(Id+1), end='')
        batchfile = './HydroLight6 < ../run/batch/I%s_%06d.txt'%(Tag, Id)
        os.system(batchfile)

#%%

path_printouts = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'printout'
path_digital = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'digital'

tf.transfer_PD_files(Tag, path_HE60)


#%%

Output_filename = 'Output_' + Tag

for t_v in theta_view:
    for p_v in phi_view:
        if CREATE_OUTPUT:
            # op.create_output(path_HE60, path, path_printouts, Tag, Comment, Id_min, Id_max, theta_view, phi_view)
            op.create_output(path_HE60, path, path_printouts, Tag, Comment, Id_start, Id_max, t_v, p_v)
        if PLOT:
            ghl.Graficar(path, Tag, t_v, p_v, save=False)
