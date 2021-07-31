#!/usr/bin/python3
'''
This script tracks time for deltas for specified category
'''

import os
from datetime import datetime
from datetime import timedelta


class TimedCategories:
    '''Class to set up the list of time categories based on timerpy.conf'''
    def __init__(self):
        with open('timerpy.conf', 'r') as self.file:
            self.file_lst = list(self.file)
        self.times = {}
        self.options = {}
    def start_times(self):
        '''takes time categories and creates a dictionary of
        categoies as well as a dictionary of options'''
        iterator = 1
        for line in self.file_lst:
            if '#' not in line:
                line = line.rstrip('\n')
                self.times[line] = 0
                self.options[str(iterator)] = line
                iterator += 1
        del iterator
        self.options.update({
            'r':'Refresh',
            'a':'Add a Category',
            's':'Summarize and Quit'
        })
    def add_time(self, cat_key, time_val):
        '''adds time specified by the val argument
        to the category specifed by the cat key arg'''
        self.times[cat_key] += time_val


def Make_Human_Readable(time_in_seconds):
    '''Takes seconds and returns formatted string'''
    str_format = '{} hour(s), {} minute(s), {} second(s)'
    time_list = str(timedelta(seconds=time_in_seconds)).split(':')
    time_as_strng = str_format.format(*time_list)
    return time_as_strng


def Get_Start_Time(prog_title):
    '''
    Gets start time based on either user input or function start time
    '''
    # Sets start date string as "YYYY MM DD"
    start_d_str = datetime.now().date().strftime('%Y %m %d')
    input_str_list = [
        prog_title,
        '',
        'Enter start time below in 24-hour format as hh mm ss',
        ' or simply hit enter to continue with current time',
        ''
    ]
    for line in input_str_list:
        print('{0:^61}'.format(line))
    while True:
        start_t_str = input(':')
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
            print("-- Error - enter time integers as suggested")
            continue
        # Checks whether string is an actual time and exits loop
        if 0 <= hrs < 25 and 0 <= mins < 60 and 0 <= secs < 60:
            break
        print('-- Error - enter a valid time as suggested')
    start_dt_str = '{} {}'.format(start_d_str, start_t_str)
    start_dt = datetime.strptime(start_dt_str, '%Y %m %d %H %M %S')
    return start_dt


def The_Menu(prog_title, categories):
    '''Prints out a formatted menu'''
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
    output_list = [
        prog_title,
        'Start Time: {}',
        'Time After 8 Hours: {}',
        '',
        '== Time Totals ==',
        '',
        '== Options =='
    ]
    opt_tbl = '{0:<3}{1:.>22}'   # makes options box 21 wide in justified format
    # inserts justified table into output list
    for option, category in sorted(categories.options.items(), reverse=True):
        output_list.insert(7, opt_tbl.format(option, '  ' + category))
    for line in output_list:  # Prints each line cetered from output_list
        print('{0:^61}'.format(line))
