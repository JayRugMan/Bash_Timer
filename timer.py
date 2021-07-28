#!/usr/bin/python3
'''
This script tracks time for deltas for specified category
'''

from datetime import datetime


def get_start_time(prog_title):
    '''
    Gets start time based on either user input or function start time
    '''
    print(prog_title)
    input_str1 = "To designate a start-time, enter it below in 24-hour format"
    input_str2 = "(hh mm ss - no leading zeros) or hit enter to continue\n: "
    # Sets start date string as "YYYY MM DD"
    start_d_str = datetime.now().date().strftime('%Y %m %d')
    while True:
        start_t_str = input(input_str1 + '\n' + input_str2)
        # Sets start time as now if not entered and exits loop
        if not start_t_str:
            start_t_str = datetime.now().strftime('%H %M %S')
            break
        # Checks whether entry is integers in suggested format
        try:
            hrs = int(start_t_str[0:2])
            mins = int(start_t_str[3:5])
            secs = int(start_t_str[6:8])
        except ValueError:
            print("\nError - enter time integers as suggested\n")
            continue
        # Checks whether string is an actual time and exits loop
        if 0 <= hrs < 25 and 0 <= mins < 60 and 0 <= secs < 60:
            break
    start_dt_str = '{} {}'.format(start_d_str, start_t_str)
    start_dt = datetime.strptime(start_dt_str, '%Y %m %d %H %M %S')
    return start_dt
