# Categories
'''This will turn the comma-separated lists in "the_file" into a dictionary 
where the first item is the key while the other items become a list as the 
value'''

import sys

the_file = 'timerpy_test.conf'
lists = {}


try:
    with open(the_file, 'r') as file:
        file_output = list(file)
except FileNotFoundError:
    sys.exit('{} not found. Please refer to the README'.format(the_file))


for line in file_output:
    if '#' not in line:
        line = line.rstrip('\n')
        list_from_line = line.split(',')
        lists[list_from_line[0]] = list_from_line[1:]


