#!/usr/bin/python3

import sys
import os

#Test whether an argument was passed with the program command
def main():
    root = set_dir()
    params = {}
    params.update(load_params(root))
    print_dirs(root)
    del_site(root,params['site'])

#set dir takes directory path argument or uses current directory upon failure
def set_dir():
    try:
        dir_name=sys.argv[1]
        if not os.path.isdir(dir_name):
            dir_name=os.getcwd()
			print('Argument is not a directory - using current directory.\n', dir_name)
    except:
        dir_name=os.getcwd()
        print('No argument passed - using current directory.\n', dir_name)
    return dir_name

def load_params(root_dir):
    param_path = os.path.join(root_dir, "_params.txt")
    params_exists(param_path)
    params = read_params(param_path)
    new_params = {}
    for line in params:
        try:
            line2 = line.split(":")
            new_params.update({line2[0].strip():line2[1].strip()})
        except:
            print('White space ignored in params file')
    return new_params
   
# confirm_params seeks _params.txt file in directory and exits program if not present
def params_exists(params_path):
    if not os.path.isfile(params_path):
        print("_params.txt file missing in directory ", dir_name)
        sys.exit(0)

def read_params(param_file):
    params = read_file(param_file)
    return params

#reads a supplied filename and returns the contents as a list
def read_file(file_path):
	with open(file_path ,'r') as rf:
		str = rf.readlines()
	return str

# delete all files and directories within "_site" folder 
def del_site(path, site):
    site_path = os.path.join(path, site)
    if os.path.isdir(site_path):
        for root, dirs, files in os.walk(site_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(site_path)

#for modification and use later
def print_dirs(dir_name):
    if os.path.isdir(dir_name):
        for root, dirs, files in os.walk(dir_name, topdown=False):
            for name in files:
                print(os.path.join(root, name))
            for dir_name in dirs:
                print(os.path.join(root, dir_name))


if __name__ == "__main__":
    main()








#remove dir including itself - requires import shutil
def remove_dirs(dir_name):
    site_dir = "_site"
    site_path = os.path.join(dir_name, site_dir)
    shutil.rmtree(site_path)

#NOT BEING USED BUT CODE MIGHT BE HANDY
def dir_contents(dir_name):
    dir_list = os.listdir(dir_name)
    for line in dir_list:
        print(line)
    return dir_list

#NOT BEING USED
def print_dict(d):
    for key, val in d.items():
        print(key, " >> ", val)

    
