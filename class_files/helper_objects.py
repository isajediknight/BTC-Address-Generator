import datetime
import os
import time
from collections import namedtuple
from os import getcwd
from collections import defaultdict
import platform

def random_num():
    """
    Random Number generator.  Creates a number between 0 and 255.
    """
    return ord(os.urandom(1))

def add_spaces(in_var,
               in_pre_spaces,
               #in_post_spaces,#deciding if this is needed or not
               in_total_spaces):
    """
    Uniform spacing
    Returns a string such that the contents will always take up in_total_spaces spots
    """
    ans = ''
    if(type(in_var) == type(0)):
        pre_spaces = in_pre_spaces - len(str(in_var))
        post_spaces = in_total_spaces - pre_spaces
        ans = ' '*pre_spaces + str(in_var) + ' '*post_spaces
    elif(type(in_var) == type('')):
        pre_spaces = in_pre_spaces - len(str(in_var))
        post_spaces = in_total_spaces - pre_spaces
        ans = ' '*pre_spaces + in_var + ' '*post_spaces
    else:
        ans = 'Datatype Not Supported'
    return ans

def secs_mins_hours_days(seconds):
    """
    Takes an integer in seconds and converts it to seconds/minutes/hours/days
    """
    if(seconds == 0):
        ans = '0 Seconds'
    elif(seconds == 1):
        ans = '1 Second'
    elif(seconds < 60):
        ans = str(seconds) + ' Seconds'
    elif(seconds < 120):
        ans = '1 Minute'
    elif(seconds < 3600):
        ans = str(int(seconds/60)) + ' Minutes'
    elif(seconds < 7200):
        ans = '1 Hour'
    elif(seconds < 86400):
        ans = str(int(seconds/3600)) + ' Hours'
    elif(seconds < 172800):
        ans = '1 Day'
    elif(seconds < 172800):
        ans = str(int(seconds/86400)) + ' Days'
    return ans

def secs_mins_hours_days_as_str_digit(seconds):
    """
    Takes an integer in seconds and converts it to seconds/minutes/hours/days
    """
    if(seconds == 0):
        ans = '0'
    elif(seconds == 1):
        ans = '1'
    elif(seconds < 60):
        ans = str(seconds)
    elif(seconds < 120):
        ans = '1'
    elif(seconds < 3600):
        ans = str(int(seconds/60))
    elif(seconds < 7200):
        ans = '1'
    elif(seconds < 86400):
        ans = str(int(seconds/3600))
    elif(seconds < 172800):
        ans = '1'
    elif(seconds < 172800):
        ans = str(int(seconds/86400))
    return ans

def secs_mins_hours_days_as_time_part(seconds):
    """
    Takes an integer in seconds and converts it to seconds/minutes/hours/days
    """
    if(seconds == 0):
        ans = 'Seconds'
    elif(seconds == 1):
        ans = 'Second'
    elif(seconds < 60):
        ans = 'Seconds'
    elif(seconds < 120):
        ans = 'Minute'
    elif(seconds < 3600):
        ans = 'Minutes'
    elif(seconds < 7200):
        ans = 'Hour'
    elif(seconds < 86400):
        ans = 'Hours'
    elif(seconds < 172800):
        ans = 'Day'
    elif(seconds < 172800):
        ans = 'Days'
    return ans

def find_all(a_str, sub):
    """
    Returns the indexes of {sub} where they were found in {a_str}.  The values
    returned from this function should be made into a list() before they can
    be easily used.
    """

    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1

def get_file_list(directory):
    """
    Send in the absolute path of a directory and it will return the files in it
    """
    file_list = {}
    nt = namedtuple('file_attributes','filename accessed modified created directory raw_size type')
    for filename in os.listdir(directory):
        file_info = os.stat(os.path.join(directory,filename))
        file_list[filename] = (nt(filename,
                                  datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                  datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                  datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                  directory,
                                  file_info.st_size,
                                  'Folder' if file_info.st_size == 0 else 'File'
                                  ))
    return file_list

def indices(lst, element):
    """
    Pulled from http://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
    Scans an entire array and returns all the locations a value appears in it
    """
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)

def read_parameter_file(file_to_read):
    """
    Function to read in all the paramters to then do cool stuff like execute queries.
    """
    # TODO:
    # Add parameter for relative or absolute paths
    
    # Initialize variables
    charset_locs = defaultdict(list)
    parameter = defaultdict(list)
    charset_all_parameters = []
    parameter_search = defaultdict(list)
    parameters = defaultdict(list)
    charset = list(set(''))
    
    # Open the file for reading from input_files
    if(platform.system() == 'Windows'):
        readfile = open('..\\input_files\\'+file_to_read,'r')
    elif(platform.system() == 'Linux'):
        readfile = open('..//input_files//'+file_to_read,'r')
    
    # Counts the number of lines with invalid paramters
    invalid_counter = 0
    
    # Counts the number of lines in the file
    line_counter = 0
    
    # Go through each line in the file
    for line in readfile:
        
        # Clear these variables for each line
        del charset
        del charset_locs

        line_counter += 1
        charset_locs = defaultdict(list)
        charset = list(set(line))

        # Loop through the charset
        for x in range(len(charset)):
            charset_locs[charset[x]] = list(find_all(line,charset[x]))

        # Test to see if parameters were correctly entered
        try:
            parameter_name_begin = int(charset_locs['{'][0])
        except:
            parameter_name_begin = -1
        try:
            parameter_name_end = int(charset_locs['}'][0])
        except:
            parameter_name_end = -1

        # If a parameter was not entered correctly save the paramter as the line of the file
        if((parameter_name_end == -1 or parameter_name_begin == -1)
           or (parameter_name_end < parameter_name_begin)):
            invalid_counter += 1
            parameters['invalid_line_'+str(line_counter)] = line.strip('\n')

        # Else save the paramter
        else:
            # Make all keys lowercase
            parameter_search[line[int(parameter_name_begin)+1:int(parameter_name_end)].lower()] = charset_locs
            parameters[line[int(parameter_name_begin)+1:int(parameter_name_end)].lower()] = line[charset_locs['}'][0]+1:].strip('\n')
            
    # Close the file
    readfile.close()
    return parameters

def print_list(my_list):
    """
    Takes a list and prints it out
    """
    for i in range(len(my_list)):
        print(my_list[i])
