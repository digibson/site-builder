#!/usr/bin/python3

import sys, os
from datetime import datetime,date

params = {}
layouts = {}
p_holder = {}

#Test whether an argument was passed with the program command
def main():
    root = set_dir()
    load_params(root)
    load_ph(root)
    compile_layouts(root)
    compile_page('/home/dave/Documents/python/structure/_posts/','2018-01-26-test_post.md')
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

def load_ph(root_dir):
    ph_file = os.path.join(root_dir, params['placeholders'])
    if not os.path.isfile(ph_file):
        print(params[placeholders], ' file missing in directory. Confirm file exists.')
        sys.exit(0)
    else:
        ph_contents = read_file(ph_file)
    for line in ph_contents:
        try:
            split_line = line.split(":", 1)
            split_line2 = split_line[1].split(',', 1)
            split_line2 = [line.strip() for line in split_line2]
            p_holder.update({split_line[0].strip():tuple(split_line2)})
        except:
            print("Ignoring p_holder file content where no colon separator exists")
    print(p_holder)
    print("Global placeholders dictionary loaded")

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
        layouts[layout_key]=layout_text[:]
    print(layouts)

def read_cached_files(includes_file, _cache={}):
    if includes_file in _cache:
        return _cache[includes_file]
    str = read_file(includes_file)
    str = [line.strip() for line in str]
    _cache[includes_file] = str
    return str

def fname_to_date(fname):
    try:
        formatter_str = '%Y-%m-%d' 
        post_date = filename.split('-', 3)
        date_str = post_date[0]+'-'+post_date[1]+'-'+post_date[2]
        datetime_obj = datetime.strptime(date_str, formatter_str)
        date_str = datetime_obj.strftime("%d %B %Y").lstrip('0')
        print(date_str)
    except:
        print('Filename does not follow valid date convention. Expected dd-mm-yy-filename.\n Amend: ',fname)
        sys.exit(0)
    return date_str

def get_content(str):
    content = {} #how do we ensure clear each time?
    contents = []#might need to test if created and clear if it is
    bounds = [i for i,line in enumerate(str) if line=='---']
    if not len(bounds) == 2:
        print('EXIT HERE - Need to have file name to write exit note')
    for x in range(bounds[0]+1, bounds[1]):
        try:
            split_line = str[x].split(":", 1)
            content.update({split_line[0].strip():split_line[1].strip()})
        except:
            print("Ignoring entry where no colon separator exists")
    for x in range(bounds[1]+1, len(str)):
        if not str[x].strip() == '':
           contents.append(str[x].strip())
        content.update({'content':contents})
    return content

def compile_page(path, f_name): ## NEEDS FURTHER DEVELOPMENT ## 
    content = {}
    f = os.path.join(path, f_name)
    str=read_file(f)
    content.update(get_content(str))
    layout_template = layouts[content['layout']]
    for key, val in p_holder.items():
        try:
            line_no = layout_template.index(key)
            layout_template[line_no] = val[1].format(content[val[0]])
        except:
            print('No entry for ', key)
    print(layout_template)

#reads a supplied filename and returns the contents as a list
def read_file(file_path):
    with open(file_path ,'r') as rf:
        str = rf.readlines()
        str = [line.strip() for line in str]
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
