import sys
import os
from os import getcwd
sys.path.insert(0,'..//class_files//')
from helper_objects import privkey
from helper_objects import addy
from helper_objects import read_parameter_file
from helper_objects import find_all
import datetime

def run(param_file = 'gen_btc_addr.input'):
    parameters = read_parameter_file(param_file)
    return get_end_date(param_file)
    #start = datetime.datetime.now()
    key = privkey()
    add = addy(int(key,16))
    out_string = key+',1'+add
    print(out_string)
    #print((datetime.datetime.now() - start).microseconds)

def print_list(my_list):
    """
    Takes a list and prints it out
    """
    for i in range(len(my_list)):
        print(my_list)

def get_end_date(param_file = 'gen_btc_addr.input'):
    """
    Returns the time to stop as a datetime.datetime
    """
    parameters = read_parameter_file(param_file)
    errors = []
    slashes = list(find_all(parameters['end_date'],'/'))
    colons = list(find_all(parameters['end_time'],':'))
    try:
        month = int(parameters['end_date'][:slashes[0]])
    except:
        errors.append("Error getting Month from 'end_date' in "+param_file)
    try:
        day = int(parameters['end_date'][slashes[0]+1:slashes[1]])
    except:
        errors.append("Error getting Day from 'end_date' in "+param_file)
    try:
        year = int(parameters['end_date'][slashes[1]+1:])
    except:
        errors.append("Error getting Year from 'end_date' in "+param_file)
    try:
        hour = int(parameters['end_time'][:colons[0]])
    except:
        errors.append("Error getting Hour from 'end_date' in "+param_file)
    try:
        minute = int(parameters['end_time'][colons[0]+1:])
    except:
        errors.append("Error getting Minute from 'end_date' in "+param_file)
    
    second = 0
    microsecond = 0
    
    if(len(errors) > 0):
        print_list(errors)
        return datetime.datetime(1970,1,1,1,1,0,0)
        
    if(month < 1 or month > 12):
        errors.append('Invalid Month: '+str(month))

    # Lazy I'm not validating how many days each month has
    if(day < 1 or day > 31):
        errors.append('Invalid Day: '+str(day))

    if(year < datetime.datetime.now().year):
        errors.append('Invalid Year: '+str(year))

    if(hour < -1 or hour > 23):
        errors.append('Invalid Hour: '+str(hour))

    if(minute < 0 or minute > 59):
        errors.append('Invalid Month: '+str(minute))

    if(len(errors) > 0):
        print_list(errors)
        return datetime.datetime(1970,1,1,1,1,0,0)

    return datetime.datetime(year,month,day,hour,minute,second,microsecond)

run()
