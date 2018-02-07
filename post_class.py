#!/usr/bin/python3

import sys, os
from datetime import datetime,date

filepath = '/home/dave/Documents/python/structure/_posts/'
filename = '2018-01-26-test_post.md'

def main():
    p1 = PostData(filepath, filename)
    print(p1.fpath)
    print(p1.raw_data)


class PostData(object):
    """A post will have the following details:

    Attributes:
        fname - the actual filename passed to the class
        path - the folder path passed to the class

    Functions:
        
    """

    def __init__(self, path, fname):
        self.path = path
        self.fname = fname
        self.get_fpath()
        self.get_raw_data()

    def get_fpath(self):
        self.fpath = os.path.join(self.path, self.fname)
        if not os.path.isfile(self.fpath):
            print(self.fp, ' is not a valid file path.')
            sys.exit(0)
            return

    def get_raw_data(self):
        with open(self.fpath ,'r') as rf:
            self.raw_data = rf.readlines()
            self.raw_data = [line.strip() for line in self.raw_data]
        return

    

if __name__ == "__main__":
    main()
