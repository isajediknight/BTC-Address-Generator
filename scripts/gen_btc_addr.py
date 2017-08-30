import sys
import os
from os import getcwd
sys.path.insert(0,'..//class_files//')
from helper_objects import privkey
from helper_objects import addy
from helper_objects import read_parameter_file
import datetime

def run():
    parameters = read_parameter_file('gen_btc_addr.input')
    #start = datetime.datetime.now()
    key = privkey()
    add = addy(int(key,16))
    out_string = key+',1'+add
    print(out_string)
    #print((datetime.datetime.now() - start).microseconds)

run()
