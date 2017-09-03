def run(parameter_file):
    """
    Method to check if existing BTC address was used

    btc_gen_addr_file should be an absolute path
    """
    import sys
    sys.path.insert(0,'..//class_files//')
    import datetime
    from helper_objects import read_parameter_file
    from helper_objects import find_all
    from helper_objects import secs_mins_hours_days

    start = datetime.datetime.now()
    parameters = read_parameter_file('address_check.input')
    read_used_btc_addr = open(parameters['balance_file'],'r')
    btc_used_addr_dict = {}
    skipped = []
    counter = 0
    one_counter = 0
    for line in read_used_btc_addr:
        try:
            loc = line.find(';')
            btc_used_addr_dict[line[:loc]] = line[loc+1:].strip()
            counter += 1
            #if(line[:loc][0] == '1'):
            #    one_counter += 1
        except:
            skipped.append(line.strip())
    #print('last addr',line[:loc])
    #print('Addresses that begin with 1: '+str(one_counter))
    print('Addresses with BTC: '+str(counter))
    if(len(skipped) > 0):
        print('Skipped: '+str(len(skipped)))
    read_used_btc_addr.close()
    time_diff = datetime.datetime.now() - start
    print('Read in: '+secs_mins_hours_days(time_diff.seconds)+'\n')

    files_to_check = []
    for param in parameters:
        if(param.find('addr_file_') == 0):
            files_to_check.append(param)

    for i in range(len(files_to_check)):
        check_begin_time = datetime.datetime.now()
        skipped = []
        btc_gen_addr_dict = {}
        counter = 0
        read_gen_btc_addr = open(parameters[files_to_check[i]],'r')
        for line in read_gen_btc_addr:
            try:
                loc = line.find(',')
                btc_gen_addr_dict[line[loc+1:].strip()] = 0
                counter += 1
            except:
                skipped.append(line.strip())

        print(parameters[files_to_check[i]])
        print('Addresses to check: '+str(counter))
        if(len(skipped) > 0):
            print('Skipped: '+str(len(skipped)))
        for i in btc_gen_addr_dict:
            if(i in btc_used_addr_dict):
                print('FOUND:'+i)
        time_diff = datetime.datetime.now() - check_begin_time
        print('Completed in '+secs_mins_hours_days(time_diff.seconds)+'\n')
    #print('last check',i)
    time_diff = datetime.datetime.now() - start
    print('Program took '+secs_mins_hours_days(time_diff.seconds))

run('address_check.input')
