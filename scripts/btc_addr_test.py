import sys
import os
from os import getcwd
sys.path.insert(0,'..//class_files//')
from helper_objects import privkey
from helper_objects import addy
import datetime

def run():
    start = datetime.datetime.now()
    key = privkey()
    add = addy(int(key,16))
    out_string = key+',1'+add
    print(out_string)
    print((datetime.datetime.now() - start).microseconds)

run()
