#!/usr/bin/python3

import sys, os
from datetime import datetime,date

filepath = '/home/dave/Documents/python/structure/_posts/'
filename = '2018-01-26-test-post.md'

def main():
    p1 = PostData(filepath, filename)
    print(p1.fpath)
    print(p1.folders)
    print(p1.title)
    print(p1.layout)
    print(p1.image)
    print(p1.tags)
    

class PostData(object):
    """A post will have the following attributes:

    Attributes:
        fname - the actual filename passed to the class
        path - the folder path passed to the class

    Functions:
        write folders?
    """

    def __init__(self, path, fname):
        self.path = path
        self.fname = fname
        self.image = []
        self.tags = []
        self.body = []
        self.content = {}
        self.get_fpath()
        self.get_raw_data()
        self.get_date()
        self.get_bounds()
        self.get_fm()
        self.get_content()
        self.assign_attributes()

    def get_fpath(self):
        self.fpath = os.path.join(self.path, self.fname)
        if not os.path.isfile(self.fpath):
            print(self.fpath, ' is not a valid file path.')
            sys.exit(0)
            return

    def get_date(self):
        try:
            d_format = '%d-%m-%Y' 
            dirs = self.fname.split('-', 3)
            year, month, day, post = dirs
            d_str = day+'-'+month+'-'+year
            dt_obj = datetime.strptime(d_str, d_format)           
            year = dt_obj.strftime("%Y")
            month = dt_obj.strftime("%m")
            day = dt_obj.strftime("%d")
            post = os.path.splitext(post)[0]
            self.folders = (year, month, day, post)
            self.post_date = dt_obj.strftime("%d %B %Y").lstrip('0')
            del year, month, day, post, d_format, dt_obj, d_str, dirs
        except:
            print('Filename does not follow valid date convention. Expected dd-mm-yy-filename.\n Amend: ',self.fname)
            sys.exit(0)
        return

    def get_raw_data(self):
        with open(self.fpath ,'r') as rf:
            self.raw_data = [line.strip() for line in rf.readlines()]
        return

    def get_bounds(self):
        self.bounds = [i for i,line in enumerate(self.raw_data) if line=='---']
        if not len(self.bounds) == 2:
            print('Did not find valid front matter boundaries --- in ', self.fpath)
        return

    def get_fm(self):
        for bound in range(self.bounds[0]+1, self.bounds[1]):
            try:
                line_item = [line.strip() for line in self.raw_data[bound].split(":", 1)]
                self.content.update({line_item[0]:line_item[1]})
            except:
                print("Ignoring entry where no colon separator exists")
        del bound
        return

    def get_content(self):
        contents = []
        for bound in range(self.bounds[1]+1, len(self.raw_data)):
            if not self.raw_data[bound].strip() == '':
                contents.append(self.raw_data[bound].strip())
        self.content.update({'body':contents})
        del bound
        del contents
        return

    def assign_attributes(self):
        try:
            self.title = self.content['title']
        except:
            self.title = self.folders[3].replace("-", " ").capitalize()
        try:
            self.layout = self.content['layout']
        except:
            print("No layout defined in file ", self.fname)
            sys.exit(0)
        try:
            self.image = self.content['image']
        except:
            pass
        try:
            self.tags = self.content['tags']
        except:
            pass
        try:
            self.body = self.content['body']
        except:
            pass
        return



if __name__ == "__main__":
    main()
