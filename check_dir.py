import os

def check_dir(path):
    is_dir = os.path.isdir(path)
    if(not is_dir):
        os.mkdir(path)
        print('Created:', path)
        
def check_dir_HE60(path):
    is_dir = os.path.isdir(path)
    if(not is_dir):
        print('ERROR: %s NOT FOUND.'%path)