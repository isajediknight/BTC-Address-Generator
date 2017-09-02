import sys
import os
from os import getcwd
import platform
# this is not working the way i want yet
#if(platform.system() == 'Windows'):
#    sys.path.insert(0,'../class_files/')
#elif(platform.system() == 'Linux'):
#    sys.path.insert(0,'..\\class_files\\')
sys.path.insert(0,'..//class_files//')
from helper_objects import privkey
from helper_objects import addy
from helper_objects import read_parameter_file
from helper_objects import find_all
from helper_objects import get_file_list
import datetime

def run(param_file = 'gen_btc_addr.input'):
    parameters = read_parameter_file(param_file)
    #print(get_end_date(param_file))

    if(platform.system() == 'Windows'):
        slashes = list(find_all(getcwd(),'\\'))
        input_files_dir = getcwd()[:slashes[-1]+1]+'input_files\\'
        output_files_dir = getcwd()[:slashes[-1]+1]+'output_files\\'
        class_files_dir = getcwd()[:slashes[-1]+1]+'class_files\\'
        scripts_dir = getcwd()
        # Assumes this script is actually run from the \\scripts directory
        scripts_files = get_file_list(scripts_dir)
        input_files = get_file_list(input_files_dir)
        output_files = get_file_list(output_files_dir)
        class_files = get_file_list(class_files_dir)
        

    elif(platform.system() == 'Linux'):
        slashes = list(find_all(getcwd(),'/'))
        input_files_dir = getcwd()[:slashes[-1]+1]+'input_files/'
        output_files_dir = getcwd()[:slashes[-1]+1]+'output_files/'
        class_files_dir = getcwd()[:slashes[-1]+1]+'class_files/'
        scripts_dir = getcwd()
        # Assumes this script is actually run from the //scripts directory
        scripts_files = get_file_list(scripts_dir)
        input_files = get_file_list(input_files_dir)
        output_files = get_file_list(output_files_dir)
        class_files = get_file_list(class_files_dir)

    
    #start = datetime.datetime.now()
    end_date = get_end_date(param_file)
    outfile = open(output_files_dir + 'try1.txt','w')
    counter = 0
    out_string = ''
    five_hundred_counter = 0
    print('Running until '+str(end_date))
    check = end_date > datetime.datetime.now()
    start_500 = datetime.datetime.now()
    while(check):
        counter += 1
        key = privkey()
        add = addy(int(key,16))
        out_string += key+',1'+add+'\n'
        if(counter % 500 == 0):
            diff = (datetime.datetime.now() - start_500).seconds
            outfile.write(out_string)
            counter = 0
            out_string = ''
            five_hundred_counter += 1
            print('500 x '+str(five_hundred_counter) + '\t' + str(diff) + '\tseconds' )
            check = end_date > datetime.datetime.now()
            start_500 = datetime.datetime.now()
    outfile.write(out_string)
    outfile.close()
    #print((datetime.datetime.now() - start).microseconds)

def print_list(my_list):
    """
    Takes a list and prints it out
    """
    for i in range(len(my_list)):
        print(my_list[i])

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
        month = 1
        errors.append("Error getting Month from 'end_date' in "+param_file)
    try:
        day = int(parameters['end_date'][slashes[0]+1:slashes[1]])
    except:
        day = 1
        errors.append("Error getting Day from 'end_date' in "+param_file)
    try:
        year = int(parameters['end_date'][slashes[1]+1:])
    except:
        year = 1970
        errors.append("Error getting Year from 'end_date' in "+param_file)
    try:
        hour = int(parameters['end_time'][:colons[0]])
    except:
        hour = 0
        errors.append("Error getting Hour from 'end_date' in "+param_file)
    try:
        minute = int(parameters['end_time'][colons[0]+1:])
    except:
        minute = 0
        errors.append("Error getting Minute from 'end_date' in "+param_file)

    # We're not going down to the second or microsecond level
    second = 0
    microsecond = 0
        
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

    if(datetime.datetime.now() > datetime.datetime(year,month,day,hour,minute,second,microsecond)):
        errors.append("End time of " +
                      str(datetime.datetime(year,month,day,hour,minute,second,microsecond))
                      + " occurs in the past")

    if(len(errors) > 0):
        print_list(errors)
        return datetime.datetime(1970,1,1,0,0,0,0)

    # If we've made it this far return the valid end datetime
    return datetime.datetime(year,month,day,hour,minute,second,microsecond)

run()
