#!/usr/bin/python3
'''
This script tracks time for deltas for specified category
'''

import os
import sys
from datetime import datetime
from datetime import timedelta


class TimedCategories:
    '''Class to set up the dictionary of time categories based on
    timerpy.conf in current working directory. this file is required
    to run this program. see README for detials'''
    def __init__(self, the_file):
        try:
            with open(the_file, 'r') as file:
                self.file_lst = list(file)
        except FileNotFoundError:
            sys.exit(
                '{} not found. please refer to the README'.format(the_file)
            )
        self.times = {}
        self.options = {}
        # Takes time categories and creates a dictionary of
        # categories as well as a dictionary of options
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
    def add_time(self, option, start_time):
        '''adds time specified by the val argument
        to the category specifed by the cat key arg'''
        key = self.options[option]
        time_2_add = int((datetime.now() - start_time).total_seconds())
        self.times[key] += time_2_add
    def add_category(self, the_file):
        '''opens file to append new category as provided by
        user when prompted, then adds the new category to
        the times and options dictionaries'''
        new_category = input('Please enter the new catetory: ')
        # adds the new category to the py.conf file
        with open(the_file, 'a') as file:
            file.write(new_category + '\n')
        # adds new catetory to times dict with 0 time
        self.times[new_category] = 0
        # inserts new category to options dictionary
        new_opt_num = 1
        for option_key in self.options:
            try:
                if int(option_key) == new_opt_num:
                    new_opt_num += 1
            except ValueError:
                continue
        num_items_lst = []
        str_items_lst = []
        for key, val in self.options.items():
            try:
                tosser = int(key)  # this just to test for numbered option
                num_items_lst.append((key, val))
            except ValueError:
                str_items_lst.append((key, val))
        del tosser
        num_items_lst.append((str(new_opt_num), new_category))
        self.options = dict(num_items_lst + str_items_lst)


class MenuOutputList:
    '''Class defining the menu outout list to be printed'''
    def __init__(self, prog_title, cats, start_time):
        self.prog_title = prog_title
        self.cats = cats
        self.start_time = start_time
        self.end_time = self.start_time + timedelta(hours=8)
        self.et_w_lunch = (self.end_time +
            timedelta(seconds=self.cats.times['Lunch'])
        )
        self.final_lst = [
            self.prog_title,
            'Start time: {}'.format(self.start_time),
            'Time after 8 hours: {}'.format(self.end_time.time()),
            '8 Hours plus lunch: {}'.format(self.et_w_lunch.time()),
            '',
            '== Time Totals ==',
            '',
            '== Options =='
        ]
    def ins_times(self):
        '''Inserts the times into the menu print list'''
        tt_ins = [
            i+1 for i, s in enumerate(self.final_lst) if 'Time Totals' in s
        ][0]
        # Inserts centered table into output list
        for cat, time in self.cats.times.items():
            if time > 0:
                self.final_lst.insert(tt_ins, '-- {} --'.format(cat))
                tt_ins += 1
                self.final_lst.insert(
                    tt_ins, '{}\n'.format(make_human_readable(time))
                )
                tt_ins += 1
        del tt_ins
    def ins_options(self):
        '''Inserts the categories as numbered options, as well
        as other options defined by the TimedCategories class,
        into the menu print list'''
        opt_tbl = '{0:<3}{1:.>22}'  # makes options box 25 wide in justified format
        # line number for insterting uptions
        o_ins = [
            i+1 for i, s in enumerate(self.final_lst) if 'Options' in s
        ][0]
        # inserts justified table into output list
        for opt, cat in self.cats.options.items():
            self.final_lst.insert(o_ins, opt_tbl.format(opt, ' ' + cat))
            o_ins += 1
        del opt_tbl, o_ins


def make_human_readable(time_in_seconds):
    '''Takes seconds and returns formatted string'''
    str_format = '{} Hr(s), {} Min(s), {} Sec(s)'
    time_list = str(timedelta(seconds=time_in_seconds)).split(':')
    time_as_strng = str_format.format(*time_list)
    del str_format, time_list
    return time_as_strng


def get_start_time(prog_title):
    '''
    Gets start time based on either user input or function start time
    '''
    # Sets start date string as "YYYY MM DD"
    start_d_str = datetime.now().date().strftime('%Y %m %d')
    input_str_list = [
        prog_title,
        '',
        'Enter start time below in 24-hour format as hh mm ss',
        'or simply hit enter to continue with current time',
        ''
    ]
    for line in input_str_list:
        print('{0:^61}'.format(line))
    while True:
        start_t_str = input(': ')
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
    del start_d_str, input_str_list, start_t_str, hrs, mins, secs, start_dt_str
    return start_dt


def print_menu(prog_title, cats, start_time):
    '''Prints out a formatted menu'''
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
    output_list = MenuOutputList(prog_title, cats, start_time)
    output_list.ins_times()
    output_list.ins_options()
    ## Prints each line centered from output_list
    for line in output_list.final_lst:
        print('{0:^61}'.format(line))
    del output_list


def main():
    '''Main Event'''
    title = "=== Jason's TimeCard ==="
    conf_file = 'timerpy.conf'
    categories = TimedCategories(conf_file)  # checks for conf file and reads
    beginning = get_start_time(title)
    while True:
        print_menu(title, categories, beginning)
        while True:
            selection = input('\n: ')
            if selection in categories.options:
                break
        try:
            selection = int(selection)
            categories.add_time(str(selection), beginning)
            continue
        except ValueError:
            if selection == 'r':
                continue
            if selection == 'a':
                categories.add_category(conf_file)  # will modify specified file
            #if selection == 's':
                #sum_and_quit(title, categories)
    ### Get option selection
    ### if summary and quit, sum_quit()
    ### if refresh, refresh print_menu()


main()
