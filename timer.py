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
    def __init__(self, the_file, start_time):
        try:
            with open(the_file, 'r') as file:
                self.file_lst = list(file)
        except FileNotFoundError:
            sys.exit(
                '{} not found. please refer to the README'.format(the_file)
            )
        self.times = {}
        self.options = {}
        self.beginning = start_time
        self.rolling_time = self.beginning
        self.end_time = start_time + timedelta(hours=8)
        # Takes time categories and creates a
        # dictionary of categories and one of options
        iterator = 1
        for line in self.file_lst:
            if '#' not in line:
                line = line.rstrip('\n')
                self.times[line] = 0
                self.options[str(iterator)] = line
                iterator += 1
        self.options.update({
            'r':'Refresh',
            'a':'Add a Category',
            's':'Summarize and Quit'
        })
    def add_time(self, option):
        '''adds time specified by the val argument
        to the category specifed by the cat key arg'''
        key = self.options[option]
        right_now = datetime.now()
        time_2_add = int((right_now - self.rolling_time).total_seconds())
        self.rolling_time = right_now
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


class TheOutput:
    '''Class defining the menu or summary outout to be printed'''
    def __init__(self, prog_title, cats):
        '''starts the basic structure of the program output'''
        self.cats = cats
        # Adds up total time
        t_time_str = make_human_readable(sum(self.cats.times.values()))
        self.final_lst = [
            prog_title,
            'Start time: {}'.format(self.cats.beginning),
            '',
            '== Time Totals ==',
            '',
            'Total time: ' + t_time_str,
            ''
        ]
    def ins_menu_info(self):
        '''Inserts components for menu output'''
        # Gets unused time and puts in human-readable string
        unused_sec = (datetime.now()-self.cats.rolling_time).total_seconds()
        uu_time_str = make_human_readable(unused_sec)
        # Calculates end of day considering lunch isn't included in full day
        # PER CURRENT VERSION, "Lunch" IS A NECESSARY CATEGORY (See README)
        et_w_lunch = (self.cats.end_time +
            timedelta(seconds=self.cats.times['Lunch'])
        )
        eod = 'Time after 8 hours: {}'.format(self.cats.end_time.time())
        eod_w_lnch = '8 Hours plus lunch: {}'.format(et_w_lunch.time())
        unused_str = 'Total unused time: ' + uu_time_str
        opts_heading = '== Options =='
        self.final_lst.insert(2, eod)
        self.final_lst.insert(3, eod_w_lnch)
        # Determines the line just below "Total time" for unused time
        unused_ins = [
            i for i, s in enumerate(self.final_lst) if 'Total time' in s
        ][0]
        self.final_lst.insert(unused_ins, unused_str)
        self.final_lst.insert(10, opts_heading)
        #
        # Inserts the categories as numbered options, as well
        # as other options defined by the TimedCategories class,
        # into the menu print list
        opt_tbl = '{0:<3}{1:.>22}'  # makes options box 25 wide in justified format
        # Determines line number for insterting uptions
        o_ins = [
            i+1 for i, s in enumerate(self.final_lst) if 'Options' in s
        ][0]
        # inserts justified table into output list
        for opt, cat in self.cats.options.items():
            self.final_lst.insert(o_ins, opt_tbl.format(opt, ' ' + cat))
            o_ins += 1
        self.final_lst.insert(o_ins, '')
    def ins_times(self):
        '''Inserts the times into the output after sub-heading Time Totals'''
        tt_ins = [
            i+2 for i, s in enumerate(self.final_lst) if 'Time Totals' in s
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
    def print_menu(self):
        '''Prints out a formatted menu'''
        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
        self.ins_menu_info()
        self.ins_times()
        ## Prints each line centered from output_list
        for line in self.final_lst:
            print('{0:^61}'.format(line))
    def print_summary(self):
        '''prints summary and records to a file'''
        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
        self.ins_times()
        ## Prints each line centered from output_list
        for line in self.final_lst:
            print('{0:^61}'.format(line))


def make_human_readable(time_in_seconds):
    '''Takes seconds and returns formatted string'''
    str_format = '{} Hr(s), {} Min(s), {} Sec(s)'
    time_list = str(timedelta(seconds=int(time_in_seconds))).split(':')
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


##JH    def print_menu(prog_title, cats):
##JH        '''Prints out a formatted menu'''
##JH        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
##JH        output_list = MenuOutputList(prog_title, cats)
##JH        output_list.ins_times()
##JH        output_list.ins_options()
##JH        ## Prints each line centered from output_list
##JH        for line in output_list.final_lst:
##JH            print('{0:^61}'.format(line))
##JH        del output_list


def main():
    '''Main Event'''
    title = "=== Jason's TimeCard ==="
    conf_file = 'timerpy.conf'
    beginning = get_start_time(title)
    categories = TimedCategories(conf_file, beginning)  # checks for conf file and reads
    while True:
        menu = TheOutput(title, categories)
        menu.print_menu()
        while True:
            selection = input(': ')
            if selection in categories.options:
                break
        try:
            selection = int(selection)
            categories.add_time(str(selection))
            continue
        except ValueError:
            if selection == 'r':  # refreshes menu with updated info
                continue
            if selection == 'a':  # add a category
                categories.add_category(conf_file)  # will modify specified file
            if selection == 's':  # Summary and quit
                summary = TheOutput(title, categories)
                summary.print_summary()


main()
