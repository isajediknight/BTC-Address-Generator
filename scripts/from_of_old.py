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

# Create private key
key = privkey()

# Gets the address of the private key
add = addy(int(key,16))

# Save address and private key to this variable to be written out
out_string += key+',1'+add+'\n'
