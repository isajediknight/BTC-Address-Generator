# Various code snippets testing how fast they run

def stupid():
    import random
    a = int(random.random()*1000)
    if (a > 255):
        a = stupid()
    else:
        pass
    return a

def check_it():
    """
    """
    start = datetime.datetime.now()
    check_max = 0
    check_min = 255
    counter = 0
    dict_counter = {}
    for x in range(256):
	    dict_counter[str(x)] = 0
    for x in range(100000):
	    possible = ord(os.urandom(1))
	    if(possible > check_max):
		    check_max = possible
	    if(possible < check_min):
		    check_min = possible
	    if(possible < 128):
		    counter += 1
	    dict_counter[str(possible)] = dict_counter[str(possible)] + 1
    print(str((counter/100000.0)*100)+'%')
    print((datetime.datetime.now() - start).microseconds)
    return dict_counter

def check_it_2():
    start = datetime.datetime.now()
    check_max = 0
    check_min = 255
    counter = 0
    dict_counter = {}
    for x in range(256):
	    dict_counter[str(x)] = 0
    for x in range(100000):
	    possible = stupid()
	    if(possible > check_max):
		    check_max = possible
	    if(possible < check_min):
		    check_min = possible
	    if(possible < 128):
		    counter += 1
	    dict_counter[str(possible)] = dict_counter[str(possible)] + 1
    print(str((counter/100000.0)*100)+'%')
    print((datetime.datetime.now() - start).microseconds)
    return dict_counter

def check_it_3():
    start = datetime.datetime.now()
    check_max = 0
    check_min = 255
    counter = 0
    dict_counter = {}
    for x in range(256):
	    dict_counter[str(x)] = 0
    for x in range(100000):
	    possible = random.SystemRandom().choice(rand_list)
	    if(possible > check_max):
		    check_max = possible
	    if(possible < check_min):
		    check_min = possible
	    if(possible < 128):
		    counter += 1
	    dict_counter[str(possible)] = dict_counter[str(possible)] + 1
    print(str((counter/100000.0)*100)+'%')
    print((datetime.datetime.now() - start).microseconds)
    return dict_counter
