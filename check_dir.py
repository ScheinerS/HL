import os
import sys

def check_dir(path):
    is_dir = os.path.isdir(path)
    if(not is_dir):
        os.mkdir(path)
        print('Created:', path)
        
def check_dir_HE60(path):
    is_dir = os.path.isdir(path)
    if(not is_dir):
        print(50*'*')
        print('ERROR: %s NOT FOUND.'%path)
        print(50*'*')
        sys.exit()