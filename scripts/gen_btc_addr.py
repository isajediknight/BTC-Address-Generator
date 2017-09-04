import sys
import os
from os import getcwd
import platform

# Add class_files to the system path for importing our modules
if(platform.system() == 'Windows'):
    sys.path.insert(0,'..\\class_files\\')
elif(platform.system() == 'Linux'):
    sys.path.insert(0,'..//class_files//')

from ecdsa_objects import privkey
from ecdsa_objects import addy
from helper_objects import read_parameter_file
from helper_objects import find_all
from helper_objects import get_file_list
from helper_objects import print_list
from helper_objects import secs_mins_hours_days_as_time_part
from helper_objects import secs_mins_hours_days_as_str_digit
import datetime

def run(param_file = 'gen_btc_addr.input'):
    """
    """

    start = datetime.datetime.now()
    
    parameters = read_parameter_file(param_file)

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

    end_date = get_end_date(param_file)
    cur_datetime = datetime.datetime.now()

    # Build output filename
    # YYYY-MM-DD-COMPUTERNAME.txt
    output_file_name = str(cur_datetime.year) + '-'
    output_file_name += (('0' + str(cur_datetime.month)) if (len(str(cur_datetime.month)) == 1) else str(cur_datetime.month)) + '-'
    output_file_name += (('0' + str(cur_datetime.day)) if (len(str(cur_datetime.day)) == 1) else str(cur_datetime.day)) + '_'
    output_file_name += platform.uname()[1] + '_'
    output_file_name += parameters['run_description'] + '.txt'

    if(output_file_name in output_files):
        outfile = open(output_files_dir + output_file_name,'a')
    else:
        outfile = open(output_files_dir + output_file_name,'w')
    
    counter = 0
    out_string = ''
    commit_interval_counter = 0
    print('Running until '+str(end_date))
    print('Writing to: ' + output_file_name)
    start_benchmark = datetime.datetime.now()
    check = end_date > datetime.datetime.now()
    while(check):
        counter += 1
        key = privkey()
        add = addy(int(key,16))
        out_string += key+',1'+add+'\n'
        if(counter % int(parameters['commit_interval']) == 0):
            diff = (datetime.datetime.now() - start_benchmark).seconds
            outfile.write(out_string)
            counter = 0
            out_string = ''
            commit_interval_counter += 1
            how_long_until_we_stop = datetime.datetime.now() - end_date
            print(parameters['commit_interval'] + ' x' + str(commit_interval_counter) + ' took: ' + str(diff) + ' Seconds.  Running for another: ' +
                  secs_mins_hours_days_as_str_digit(how_long_until_we_stop.seconds) + ' ' + secs_mins_hours_days_as_time_part(how_long_until_we_stop.seconds))
            check = end_date > datetime.datetime.now()
            start_benchmark = datetime.datetime.now()

            new_file_name = str(start_benchmark.year) + '-'
            new_file_name += (('0' + str(start_benchmark.month)) if (len(str(start_benchmark.month)) == 1) else str(start_benchmark.month)) + '-'
            new_file_name += (('0' + str(start_benchmark.day)) if (len(str(start_benchmark.day)) == 1) else str(start_benchmark.day))

            if(output_file_name[:10] == new_file_name):
                pass
            else:
                outfile.close()
                del outfile
                output_files = get_file_list(output_files_dir)

                cur_datetime = datetime.datetime.now()

                output_file_name = str(cur_datetime.year) + '-'
                output_file_name += (('0' + str(cur_datetime.month)) if (len(str(cur_datetime.month)) == 1) else str(cur_datetime.month)) + '-'
                output_file_name += (('0' + str(cur_datetime.day)) if (len(str(cur_datetime.day)) == 1) else str(cur_datetime.day)) + '_'
                output_file_name += platform.uname()[1] + '_'
                output_file_name += parameters['run_description'] + '.txt'
                
                if((new_file_name + '-' + platform.uname()[1]+ '.txt' ) in output_files):
                    outfile = open(output_files_dir + output_file_name,'a')
                else:
                    outfile = open(output_files_dir + output_file_name,'w')
                    print('Switching to a new ouput file: ' + output_file_name)
                
    outfile.write(out_string)
    outfile.close()
    #print((datetime.datetime.now() - start).microseconds)

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
