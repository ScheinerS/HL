import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import check_dir as cd

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.close('all')

#%%

TAGS = ['Tesis_v7', 'v8']

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

cd.check_dir(path + os.sep + 'Graficos')
save_path = path + os.sep + 'Graficos' + os.sep + 'Run_times'
cd.check_dir(save_path)

# De acá en adelante hay que leer el archivo y adaptar:´

RUN_TIMES = {}
ID = {}

RUN_TIMES['CHL'] = None
RUN_TIMES['CDOM'] = None
RUN_TIMES['NAP'] = None

#%%
for Tag in TAGS:
    RUN_TIMES[Tag] = pd.read_csv(path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '.csv', index_col=('Id'))
    # RUN_TIMES[Tag].index = RUN_TIMES[Tag]['Id']
    ID[Tag] = pd.read_excel(path + os.sep + 'Inputs' + os.sep + 'Id_' + Tag + '.xlsx', engine = 'openpyxl', index_col=('Id'))
    # ID[Tag].index = ID[Tag]['Id']
    
    # ID = ID[Tag].iloc[RUN_TIMES[Tag].index]

for Tag in TAGS:
    for i in ID[Tag].index:
        if not i in RUN_TIMES[Tag].index:
            ID[Tag].drop(i, inplace=True)
#%%
    # Remuevo los que no estén:
    
# def hist(Tag):
#     plt.figure()
#     plt.hist(RUN_TIMES['Run time'])
#     plt.xlabel('t [m]')
#     #plt.ylabel('')
#     plt.title(Tag)
#     plt.savefig(save_path + os.sep + 'Output_' + Tag + '_hist.png')

variables = ['CHL', 'NAP', 'CDOM']
colormaps = {'CHL': 'winter', 'CDOM': 'Wistia', 'NAP': 'OrRd'}
units = {'CHL': 'mg/m^{3}', 'CDOM': 'm^{-1}', 'NAP': 'g/m^{3}'}

FS = 15

for Tag in TAGS:
    for var in variables:
        plt.figure()
        # plt.plot(, '.')
        plt.scatter(RUN_TIMES[Tag].index, RUN_TIMES[Tag]['Run time'], c=ID[Tag][var], cmap=colormaps[var])
        plt.xlabel(r'Id')
        plt.ylabel(r't [m]')
        plt.title(r'\verb|%s|'%Tag)
        cbar = plt.colorbar()
        cbar.set_label(var + r'$\;[%s]$'%units[var], fontsize=FS)
        plt.show()
        plt.savefig(save_path + os.sep + 'runtimes_' + Tag + '_' + var + '.png')