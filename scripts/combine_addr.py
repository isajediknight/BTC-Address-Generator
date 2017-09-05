# Used to determine Computer Name
import platform

import sys
# Add class_files to the system path for importing our modules
# As in helper_objects.py
if(platform.system() == 'Windows'):
    sys.path.insert(0,'..\\class_files\\')
elif(platform.system() == 'Linux'):
    sys.path.insert(0,'..//class_files//')

# Gets list of files in a directory (no recursive)
from helper_objects import get_file_list

# Gets parameters from parameter file
from helper_objects import read_parameter_file

# Prints out all the values in a list
from helper_objects import print_list

# Used for benchmarking
import datetime

# Used for copying/moving files
import shutil

def run(parameter_file):
    """
    Method to take the BTC Addresses generated from multiple machines and combine them into one file
    """
    # Read paramters from the parameter file
    parameters = read_parameter_file(parameter_file)

    # List of files in the uncombined directory
    uncombined_files = get_file_list(parameters['uncombined_dir'])

    # List of files in the combined directory
    combined_files = get_file_list(parameters['combined_dir'])

    # Save off errors to later display them
    errors = []

    # Get today's date.  If an address file was created today we won't combine it until tomorrow to prevent duplicating addresses
    date_today = datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)

    # Total Processed
    total_processed = 0

    # Loop through list of files in uncombined_files directory
    for my_file in uncombined_files:

        # Check to see if naming convention was followed
        try:
            combined_date = datetime.date(int(my_file[:4]),int(my_file[5:7]),int(my_file[8:10]))
        except:
            combined_date = datetime.date(1970,1,1)
            errors.append(my_file + ' did not have a valid YYYY-MM-DD at beginning of the filename')

        # If file was created from a day older than today combine it
        if(combined_date < date_today):

            # Count addresses read in
            addr_counter = 0

            # Open the address file for reading
            readfile = open(parameters['uncombined_dir'] + my_file, 'r')

            # Refresh combined file list
            # If a combined file already exists we want to append and not overwrite
            combined_files = get_file_list(parameters['combined_dir'])
            
            if((str(combined_date) + '.txt') in combined_files):
                # File exists append to it
                outfile = open(parameters['combined_dir'] + str(combined_date) + '.txt','a')
            else:
                # File does not exist create it new
                outfile = open(parameters['combined_dir'] + str(combined_date) + '.txt','w')

            # Loop through addresses and write them to a combined file
            for line in readfile:
                addr_counter += 1
                outfile.write(line)

            # File editing complete - close them
            readfile.close()
            outfile.close()

            # Clear them for next iteration of the loop
            del readfile
            del outfile

            # Move file thatwas read from to the processed directory
            shutil.move(parameters['uncombined_dir'] + my_file,parameters['processed_dir'] + my_file)
            print('Processed:\t' + my_file + '\t' + str(addr_counter))
            total_processed += addr_counter
        else:
            print('Ignored:\t' + my_file)

    # Total number of Addresses imported
    print('Addresses imported: ' + str(total_processed))

    # Display any errors to the user
    if(len(errors) > 0):
        print_list(errors)
    
run('combine_addr.input')
