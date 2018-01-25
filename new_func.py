#!/usr/bin/python3

import sys
import os

params = {}
layouts = {}


#Test whether an argument was passed with the program command
def main():
    root = set_dir()
    load_params(root)
    compile_layouts(root)
#    print_dirs(root)
#    del_site(root,params['site'])

#set dir takes directory path argument or uses current directory upon failure
def set_dir():
    try:
        dir_name=sys.argv[1]
        if not os.path.isdir(dir_name):
            dir_name=os.getcwd()
            print('Argument is not a directory - using current directory.')
        print('Path set to ', dir_name)
    except:
        dir_name=os.getcwd()
        print('No argument passed - using current directory.\n', dir_name)
    return dir_name

def load_params(root_dir):
    param_file = os.path.join(root_dir, "_params.txt")
    if not os.path.isfile(param_file):
        print('_params.txt file missing in directory ', param_file, '\n Confirm file exists or correct folder used.')
        sys.exit(0)
    else:
        param_contents = read_file(param_file)
    for line in param_contents:
        try:
            split_line = line.split(":", 1)
            params.update({split_line[0].strip():split_line[1].strip()})
        except:
            print("Ignoring params file content where no colon separator exists")
    print("Global parameters dictionary loaded")

def compile_layouts(root_dir):
    layouts_path = os.path.join(root_dir, params['layouts'])
    includes_path = os.path.join(root_dir, params['includes'])
    if not os.path.isdir(includes_path):
        print(includes_path, " does not exist - exiting program.")
        sys.exit(0)
    if not os.path.isdir(layouts_path):
        print(layouts_path, " does not exist - exiting program.")
        sys.exit(0)
    else:
        layout_files = os.listdir(layouts_path)
    layout_text = []
    for entry in layout_files:
        entry_file = entry.strip()
        layout_key = os.path.splitext(entry_file)[0]
        f = os.path.join(layouts_path, entry_file)
        if os.path.isfile(f):
            include_files = read_file(f)
            layout_text.clear()
            for include_file in include_files:
                inc_file = os.path.join(includes_path, include_file.strip())
                if os.path.isfile(inc_file):
                    layout_text.extend(read_cached_files(inc_file))
                else:
                    print(inc_file, ' is not inside the ', params['includes'],'folder.')
                print(layout_text)
        layouts.update({layout_key:layout_text})
    print(layouts)

def read_cached_files(includes_file, _cache={}):
    if includes_file in _cache:
        return _cache[includes_file]
    str = read_file(includes_file)
    _cache[includes_file] = str
    return str


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
