import os
import sys
import pandas as pd
import glob

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

Tag = 'v8_no_fl'

files = sorted(glob.glob(path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '_*.xlsx'))

# DF va a tener varios data frame. Las keys son las hojas.
DF = {}

# Hay que leer hoja por hoja...

pd.read_excel(files[0])

xl = pd.ExcelFile(files[0])

xl.sheet_names  # see all sheet names

#%%

# ADAPTAR. ESTE BLOQUE FUNCIONA BIEN PARA UNA HOJA. HAY QUE HACERLO PARA CADA HOJA.
# HABRÍA QUE LEER EL files[0] Y LEER AUTOMÁTICAMENTE LA LISTA DE HOJAS.

for sheet in xl.sheet_names[1:]:
    DF[sheet] = pd.DataFrame()
    for file in files:
        DF[sheet].append(pd.read_excel(file))
 
# create a new dataframe to store the
# merged excel file.
merged_DF = {}

pd.DataFrame()
for sheet in xl.sheet_names[1:]:
    merged_DF[sheet] = pd.DataFrame()
    
for file in files:
    # appends the data into the merged_DF.
    
    merged_DF[sheet] = merged_DF.append(
      DF[sheet], ignore_index=True)
 
    # Hice mucho lío con los nombres. Repasar paso a paso.
    
# exports the dataframe into excel file with
# specified name.
merged_DF.to_excel(path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '.xlsx', index=False)