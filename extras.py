import sys, os
from datetime import datetime,date

file_path = '/home/dave/Documents/python/structure/_posts/'
filename = '2018-01-26-test_post.md'

f = os.path.join(file_path, filename)
str=read_file(f)

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

def read_file(file_path):
    with open(file_path ,'r') as rf:
        str = rf.readlines()
        str = [line.strip() for line in str]
    return str
 
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
    print(content)

fname_to_date(filename)
get_content(str)
