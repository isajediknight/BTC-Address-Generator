import os

# Used to get current directory
from os import getcwd

# Used to get computer name
import platform

import sys
# Add class_files to the system path for importing our modules
if(platform.system() == 'Windows'):
    sys.path.insert(0,'..\\class_files\\')
elif(platform.system() == 'Linux'):
    sys.path.insert(0,'..//class_files//')

# ECDSA computations
# Generates a private key
from ecdsa_objects import privkey

# Computes the BTC address from the private key
from ecdsa_objects import addy

# Reads data from parameter file: .input
from helper_objects import read_parameter_file

# Returns all the occurances of a char or a string within another string
from helper_objects import find_all

# Returns list of files found in the given directory
from helper_objects import get_file_list

# Prints all the values in a list
from helper_objects import print_list

# Converts an integer given in Seconds to the largest time componet - unit of measure (years, days, etc)
from helper_objects import secs_mins_hours_days_as_time_part

# Converts an integer given in Seconds to the largest time componet - integer of (years, days, etc)
from helper_objects import secs_mins_hours_days_as_str_digit

# Used for benchmarking
import datetime

# Used for slowing down CPU usage
import time

def run(param_file = 'gen_btc_addr.input'):
    """
    """

    # Record how long the program runs
    start = datetime.datetime.now()

    # Read in all the paramters (commit interval, run, endate)
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

    # What time do we need to stop?
    end_date = get_end_date(param_file)

    # If a file has a date of today we will ignore it
    cur_datetime = datetime.datetime.now()

    # Build output filename
    # YYYY-MM-DD-COMPUTERNAME.txt
    cur_datetime = datetime.datetime.now()
    output_file_name = str(cur_datetime.year) + '-'
    output_file_name += (('0' + str(cur_datetime.month)) if (len(str(cur_datetime.month)) == 1) else str(cur_datetime.month)) + '-'
    output_file_name += (('0' + str(cur_datetime.day)) if (len(str(cur_datetime.day)) == 1) else str(cur_datetime.day)) + '_'
    output_file_name += platform.uname()[1]
    if(len(parameters['run_description']) > 0):
        output_file_name += '_' + parameters['run_description']
    output_file_name += '.txt'

    # If file exists append to it, otherwise create it
    # 'w' will delete and recreate the file - losing your data
    if(output_file_name in output_files):
        outfile = open(output_files_dir + output_file_name,'a')
    else:
        outfile = open(output_files_dir + output_file_name,'w')

    # Counts addresses generated
    counter = 0

    # Compute the commit interval, save the data to out_string for writting
    out_string = ''

    # Hoq many commit intervals have we reached?
    commit_interval_counter = 0

    # Display how long we are running for
    print('Running until '+str(end_date))

    # Name of the output file
    print('Writing to: ' + output_file_name)

    # Begin benchmark
    start_benchmark = datetime.datetime.now()

    # Checks to see if we have reached the end date
    check = end_date > datetime.datetime.now()
    while(check):

        # Counts addresses we've created
        counter += 1

        # Create private key
        key = privkey()

        # Gets the address of the private key
        add = addy(int(key,16))

        # Save address and private key to this variable to be written out
        out_string += key+',1'+add+'\n'

        if(float(parameters['sleep']) > 0):
            time.sleep(float(parameters['sleep']))

        # Once we reach our commit interval save all of it off
        if(counter % int(parameters['commit_interval']) == 0):

            # Benchmark since last commit
            diff = (datetime.datetime.now() - start_benchmark).seconds

            # Save data
            outfile.write(out_string)

            # Reset counter
            counter = 0

            # Reset out_string for next set of addresses
            out_string = ''

            # We've commited this manytimes
            commit_interval_counter += 1

            # Recompute how much longer we will run
            how_long_until_we_stop = end_date - datetime.datetime.now()

            # Display benchmark
            print(parameters['commit_interval'] + ' x' + str(commit_interval_counter) + ' took: ' + str(diff) + ' Seconds.  Running for another: ' +
                  secs_mins_hours_days_as_str_digit(how_long_until_we_stop.seconds) + ' ' + secs_mins_hours_days_as_time_part(how_long_until_we_stop.seconds))

            # Reset our break condition
            check = end_date > datetime.datetime.now()

            # Reset benchmark
            start_benchmark = datetime.datetime.now()

            # If we switch to a new day update the file name
            new_file_name = str(start_benchmark.year) + '-'
            new_file_name += (('0' + str(start_benchmark.month)) if (len(str(start_benchmark.month)) == 1) else str(start_benchmark.month)) + '-'
            new_file_name += (('0' + str(start_benchmark.day)) if (len(str(start_benchmark.day)) == 1) else str(start_benchmark.day))

            # Refresh file list to see if we need to create a new file or append to an existing one
            output_files = get_file_list(output_files_dir)

            if(output_file_name[:10] == new_file_name):
                pass
            else:
                outfile.close()
                del outfile

                # Get current date to build file name
                cur_datetime = datetime.datetime.now()
                output_file_name = str(cur_datetime.year) + '-'
                output_file_name += (('0' + str(cur_datetime.month)) if (len(str(cur_datetime.month)) == 1) else str(cur_datetime.month)) + '-'
                output_file_name += (('0' + str(cur_datetime.day)) if (len(str(cur_datetime.day)) == 1) else str(cur_datetime.day)) + '_'
                output_file_name += platform.uname()[1]
                if(len(parameters['run_description']) > 0):
                    output_file_name += '_' + parameters['run_description']
                output_file_name += '.txt'

                # If file exists append to it otherwise create it new
                if((new_file_name + '-' + platform.uname()[1]+ '.txt' ) in output_files):
                    outfile = open(output_files_dir + output_file_name,'a')
                else:
                    outfile = open(output_files_dir + output_file_name,'w')
                    print('Switching to a new ouput file: ' + output_file_name)

            if('graceful_stop' in output_files):
                # Graceful stop requested
                print('Graceful stop requested.  Please delete: ' + output_files_dir + 'graceful_stop before running again.')
                break
    
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
