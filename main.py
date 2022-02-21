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
# import Graficar_HL as ghl

#%%

# Flags:
CREATE_BATCHRUN_FILES = 1
RUN = 1

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

# Back up del Input:
path_inputs = path + os.sep + 'Inputs'
cd.check_dir(path_inputs)
shutil.copyfile('Input.xlsx', path_inputs + os.sep + 'Inputs_%s.xlsx'%Tag)

def geometric_progression(start, stop, factor):
    # Geometric progression starting at from 'start' to 'stop' where a(i+1)=factor*a(i).
    N = int(np.log(stop/start)/np.log(factor))+1 # cantidad necesaria de valores.
    u = np.empty(N+1,)
    u[0] = start
    u[1:] = factor
    gp = np.cumprod(u)
    gp = np.append(0,gp)
    return gp
    
# start = 10
# stop = 100
# factor = 5
# geometric_progression(start, stop, factor)

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
A_c_star_660 = [Inputs['A_c_star_660'][0]]
E_c_star_660 = [Inputs['E_c_star_660'][0]]
Astar_NAP_443 = [Inputs['Astar_NAP_443'][0]]
Astar_NAP_offset = [float(i) for i in str(Inputs['Astar_NAP_offset'][0]).split(',')]
Bstar_NAP_555 = [Inputs['Bstar_NAP_555'][0]]
S_NAP = [Inputs['S_NAP'][0]]
GAMMA_C_NAP = [Inputs['GAMMA_C_NAP'][0]]
S_CDOM = [Inputs['S_CDOM'][0]]
SPF_FF_BB_B_NAP = [Inputs['SPF_FF_BB_B_NAP'][0]]
SPF_FF_BB_B_CHL = [Inputs['SPF_FF_BB_B_CHL'][0]]

suntheta = [Inputs['suntheta'][0]]
sunphi = [Inputs['sunphi'][0]]

theta_view = [Inputs['theta_view'][0]]
phi_view = [Inputs['phi_view'][0]]

cloud = [Inputs['cloud'][0]]
windspeed = [Inputs['windspeed'][0]]

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

# Printout de los valores para verificar la configuración:
    
print(50*'-')

print('Tag:\t', Tag)
print('Comment:\t', Comment)

print(50*'-')

print('\nCHL:\n', CHL)
print('\nCDOM:\n', CDOM)
print('\nNAP:\n', NAP)

print(50*'-')

print('\nAstar_NAP_443:\n', Astar_NAP_443)
print('\nAstar_NAP_offset:\n', Astar_NAP_offset)
print('\nBstar_NAP_555:\n', Bstar_NAP_555)
print('\nS_NAP:\n', S_NAP)
print('\nGAMMA_C_NAP:\n', GAMMA_C_NAP)
print('\nS_CDOM:\n', S_CDOM)

print(50*'-')

print('\nSPF_FF_BB_B_NAP:\n', SPF_FF_BB_B_NAP)
print('\n:SPF_FF_BB_B_CHL\n', SPF_FF_BB_B_CHL)

print(50*'-')

print('\nsuntheta:\n', suntheta)
print('\nsunphi:\n', sunphi)
print('\ntheta_view:\n', theta_view)
print('\nphi_view:\n', phi_view)
print('\ncloud:\n', cloud)
print('\nwindspeed:\n', windspeed)

print(50*'-')

input('Continue (ENTER)?')

# Chequeo de sobreescritura:
output_file = 'Output_' + Tag + '.xlsx'
is_file = os.path.isfile(output_file)
if is_file:
    print('\n"%s" already exists.'%output_file)
    input('Overwrite (ENTER)?')

#%%

DF = pd.DataFrame()

DF['Id'] = None
DF['CHL'] = None
DF['NAP'] = None
DF['CDOM'] = None
DF['A_c_star_660'] = None
DF['E_c_star_660'] = None
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

#%%

# Verificación de directorios:
PATH = '/home/santiago/Documents'
paths = [PATH + '/HE60/data/DATA_SS', PATH + '/tesis/HL/batchruns',  PATH + '/tesis/HL/DATA']

for p in paths:
    tf.check_dir(p)

del paths, PATH

#%%
# Creamos los archivos de a y b para cada componente (CHL, NAP, CDOM):

# Id_min = 0
Id = 0

combination = list(itertools.product(CHL, NAP, CDOM, A_c_star_660, E_c_star_660, Astar_NAP_443, Astar_NAP_offset, Bstar_NAP_555, S_NAP, GAMMA_C_NAP, S_CDOM, SPF_FF_BB_B_NAP, SPF_FF_BB_B_CHL, suntheta, sunphi, cloud, windspeed))
# print(combination)
Id_max = len(combination)

DF.columns

if CREATE_BATCHRUN_FILES:
    # Id = Id_min
    for comb in combination:
        print('\r%4d'%(Id+1), end='')
        
        line = [str('%04d'%Id)]
        line.extend(list(comb))
        
        DF.at[Id] = line
        
        chl = line[1]
        cdom = line[2]
        nap = line[3]
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
        
        # A ESTA FUNCIÓN LE FALTA EL OFFSET DEL NAP (FALTA IMPLEMENTAR EN LA FUNCIÓN TAMBIÉN):
        ab.create_data_files(str('%04d'%Id), chl, nap, cdom, a_c_star_660, e_c_star_660, astar_nap_443, astar_nap_offset, bstar_nap_555, s_nap, s_cdom, gamma_c_nap)
            
        hlb.create_batchrun_file(Id, Tag, Comment, chl, cdom, nap, s_cdom, spf_ff_bb_b_nap, spf_ff_bb_b_chl, suntheta, sunphi, cloud, windspeed)
        
        Id += 1

#%%

# Este bloque va a ser reemplazado por el anterior:
# if CREATE_BATCHRUN_FILES:
#     print('\nCreating HL batchruns:')
#     Id = Id_min
#     for chl in CHL:
#         for nap in NAP:
#             for cdom in CDOM:
#                 for astar_nap in Astar_NAP_443:
#                     for bstar_nap_555 in Bstar_NAP_555:
#                         for s_nap in S_NAP:
#                             for s_cdom in S_CDOM:
#                                 for gamma_c_nap in GAMMA_C_NAP:
#                                     for spf_ff_bb_b_nap in SPF_FF_BB_B_NAP:
#                                         for spf_ff_bb_b_chl in SPF_FF_BB_B_CHL:
    
#                                             # print('\r%4d'%(Id+1), end='')                                            
#                                             # DF.at[Id] = [str('%04d'%Id), chl, nap, cdom, astar_nap, bstar_nap_555, s_nap, s_cdom, gamma_c_nap, spf_ff_bb_b_nap, spf_ff_bb_b_chl]
#                                             # ab.create_data_files(str('%04d'%Id), chl, nap, cdom, A_c_star_660, E_c_star_660, astar_nap, bstar_nap_555, s_nap, s_cdom, gamma_c_nap)
                                            
#                                             # hlb.create_batchrun_file(Id, Tag, Comment, chl, cdom, nap, s_cdom, spf_ff_bb_b_nap, spf_ff_bb_b_chl, suntheta, sunphi, cloud, windspeed)
                                            
#                                             Id += 1
#     Id_max = Id
    
    
# Transferencia de los archivos:
    
# Batchruns:
path_batchruns = path + os.sep + 'batchruns'
cd.check_dir(path_batchruns)
tf.transfer(path_batchruns, path_HE60 + os.sep + 'run/batch')

# Datos de a y b:
path_ab = path + os.sep +'/DATA'
cd.check_dir(path_ab)
tf.transfer(path + '/DATA', path_HE60 + os.sep + 'data/DATA_SS')


#%%

if RUN:    
    dest_dir = path_HE60 + os.sep + 'backend'
    os.chdir(dest_dir)
    # print('Running:')
    for Id in range(Id_max):
        print('\r%4d'%(Id+1), end='')
        os.system('./HydroLight6 < ../run/batch/I%s_%04d.txt'%(Tag, Id))
        
#%%
# Reemplazado por el bloque anterior:
    
# if RUN:
#     print('\nRunning:')
#     #os.system('cd %s'%batchruns_dir)
    
#     dest_dir = path_HE60 + os.sep + 'backend'
#     os.chdir(dest_dir)

#     Id = 0
#     for chl in CHL:
#         for nap in NAP:
#             for cdom in CDOM:
#                 for astar_nap in Astar_NAP_443:
#                     for bstar_nap_555 in Bstar_NAP_555:
#                         for s_nap in S_NAP:
#                             for s_cdom in S_CDOM:
#                                 for gamma_c_nap in GAMMA_C_NAP:
#                                     for spf_ff_bb_b_nap in SPF_FF_BB_B_NAP:
#                                         for spf_ff_bb_b_chl in SPF_FF_BB_B_CHL:
#                                             os.system('./HydroLight6 < ../run/batch/I%s_%04d.txt'%(Tag, Id))
#                                             Id += 1

#     print('\nDone.\n')

#%%

# Regresamos al directorio original de trabajo:
os.chdir(path)
cd.check_dir(path + os.sep + 'Inputs')
DF.to_excel('Inputs/Id_%s.xlsx'%Tag, index = False)

path_printouts = path_HE60 + os.sep + 'output' + os.sep + 'HydroLight' + os.sep + 'printout' 

Output_filename = 'Output_' + Tag # Nombre para el archivo de salida.

for t_v in theta_view:
    for p_v in phi_view:
        op.create_output(path_HE60, path, path_printouts, Tag, Comment, t_v, p_v)

# ghl.Graficar(Tag)

# print('Cantidad de simulaciones:', Id_max)