import os
# import sys
import pandas as pd
import glob
from time import sleep

path = os.getcwd()
# path = os.path.dirname(os.path.realpath('__file__'))
# sys.path.append(path)

TAGS = ['v8_no_fl', 'v9', 'TEST_3']
# Tag = 'v8_no_fl'
Tag = 'TEST_3'

# ESTO AUTOMATIZARLO DESPUÉS:
[theta_view, phi_view] = [40, 135]

output_filename = path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '_vaz%dvphi%d.xlsx'%(theta_view, phi_view)# + '_%06d-%06d.xlsx'%(Id_min, Id_max)

files = sorted(glob.glob(path + os.sep + 'Outputs' + os.sep + 'Output_' + Tag + '_*.xlsx'))

if output_filename in files:
    files.remove(output_filename)

Sheets = pd.ExcelFile(files[0]).sheet_names # see all sheet names

print('\nOutput file:', output_filename)

#%%

merged_DF = pd.DataFrame()
writer = pd.ExcelWriter(output_filename, engine='openpyxl', mode='w')
merged_DF.to_excel(writer, sheet_name='README', header=True, index=False)

for sheet in Sheets[1:]:
    print(sheet)

    merged_DF = pd.DataFrame()
    
    for file in files:
        merged_DF = merged_DF.append(pd.read_excel(file, sheet_name=sheet, dtype={'Id': str}), ignore_index=True)
    
    merged_DF = merged_DF.drop_duplicates()

    writer = pd.ExcelWriter(output_filename, engine='openpyxl', mode='a')
    merged_DF.to_excel(writer, sheet_name=sheet, header=True, index=False)
    writer.save()
    
    # sleep(5)