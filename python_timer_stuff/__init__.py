"""Classes and functions for timer.py"""


import os
import sys
import json
from datetime import datetime
from datetime import timedelta
from calendar import day_abbr
from python_timer_stuff import json_to_dict as categories


def make_human_readable(time_in_seconds):
    '''Takes seconds and returns formatted string'''
    str_format = '{} Hr(s), {} Min(s), {} Sec(s)'
    time_list = str(timedelta(seconds=int(time_in_seconds))).split(':')
    # Turn each list item from string to integer
    time_list = [int(i) for i in time_list]
    time_as_strng = str_format.format(*time_list)
    del str_format, time_list
    return time_as_strng


def print_centered_61(the_output_lst):
    '''Prints the lines in the list provided centered in 61 characters'''
    for line in the_output_lst:
        print('{0:^61}'.format(line))


def get_starting_input(prompt_text_lst, output_type):
    '''
    Gets start time or hours based on either user input or default values
    '''
    print_centered_61(prompt_text_lst)
    # Loops to get the start time in proper format

    while True:
        user_input = input(': ')
        # If left blank, then default value is chosen and loop exits
        if not user_input:
            # This if no time or duration is entered, thus default was chosen
            user_input = datetime.now().strftime('%H %M')
            hrs = 8
            mins = 0
            break
        # Checks whether entry is integers in suggested format
        try:
            hrs = int(user_input.split(' ')[0])
            mins = int(user_input.split(' ')[1])
        except ValueError:
            print("-- Error - enter time integers as suggested")
            continue
        except IndexError:
            print("-- Error - enter a value for both hours and minutes")
            continue
        # Checks whether string is an actual time and exits loop
        if 0 <= hrs < 25 and 0 <= mins < 60:
            break
        print('-- Error - enter a valid time as suggested')

    # If the output type is to be a time
    if output_type == 'time':
        # Sets start date string as "YYYY MM DD"
        start_d_str = datetime.now().date().strftime('%Y %m %d')
        start_dt_str = '{} {}'.format(start_d_str, user_input)
        final_output = datetime.strptime(start_dt_str, '%Y %m %d %H %M')
        del start_d_str, start_dt_str

    # If the output type is to be a duration
    if output_type == 'duration':
        final_output = timedelta(hours=hrs,
                               minutes=mins)

    del prompt_text_lst, user_input, output_type, hrs, mins

    return final_output



class TimedCategories:
    '''Class to set up the dictionary of time categories based on
    categories.json in current working directory. this file is required
    to run this program. see README for detials'''


    def __init__(self, start_time, workday_hrs):

        self.times = {
            'sup': {},
            'sub': {}
        }  # dict of sub and super category dicts
        self.options = {
            'sup': {},
            'sub': {}
        }  # dict of sub and super options dicts
        self.beginning = start_time
        self.beg_str = day_abbr[self.beginning.weekday()] +\
            ' ' +\
            str(self.beginning)
        self.rolling_time = self.beginning
        self.end_time = start_time + workday_hrs
        # Takes time categories and creates a
        # dictionary of categories and one of options

        sup_iterator = 1
        sub_iterator = 1
        for sup_cat,sub_cats in categories.lists.items():
            self.times['sup'][sup_cat] = 0
            self.options['sup'][str(sup_iterator)] = sup_cat
            sup_iterator += 1
            for sub_cat in sub_cats:
                self.times['sub'][sub_cat] = 0
                self.options['sub'][str(sub_iterator)] = sub_cat
                sub_iterator += 1
        self.options['sub'].update({
            'r':'Refresh',
            'a':'Add a Category',
            'q':'Summarize and Quit'
        })


    def add_time(self, option):
        '''adds time specified by the val argument
        to the category specifed by the cat sbcat arg'''
        sbcat = self.options['sub'][option]
        right_now = datetime.now()
        time_2_add = int((right_now - self.rolling_time).total_seconds())
        self.rolling_time = right_now
        self.times['sub'][sbcat] += time_2_add
        for spcat,sbcats in categories.lists.items():
            if sbcat in sbcats:
                self.times['sup'][spcat] += time_2_add


    def add_sub_category(self):
        '''Opens file to append new category as provided by
        user when prompted, then adds the new category to
        the times and options dictionaries'''

        new_subcat = input('Please enter the new sub-category: ')

        # Displays list of super cats & loops 'til valid sel is made
        while True:
            for opt,spcat in self.options['sup'].items():
                print("{} - {}".format(opt,spcat))
            selection = input('Under which super catetory: ')
            if selection in self.options['sup'].keys():
                newsubs_supcat = self.options['sup'][str(selection)]
                categories.lists[newsubs_supcat].append(new_subcat)
                break

        # Adds the new category to the json file
        with open(categories.THE_FILE, 'w') as json_file:
            json_file.write(
                json.dumps(
                    categories.lists, sort_keys=True, indent=2
                ) + '\n'
            )

        # Adds new catetory to times dict with 0 time
        self.times['sub'][new_subcat] = 0

        # Inserts new category to options dictionary
        new_opt_num = 1
        num_items_lst = []
        str_items_lst = []

        for opt, cat in self.options['sub'].items():
            try:
                if int(opt) == new_opt_num:
                    num_items_lst.append((opt, cat))
                    new_opt_num += 1
            except ValueError:
                str_items_lst.append((opt, cat))

        num_items_lst.append((str(new_opt_num), new_subcat))
        self.options['sub'] = dict(num_items_lst + str_items_lst)



class TheOutput:
    '''Class defining the menu or summary outout to be printed'''


    def __init__(self, prog_title, cats):
        '''starts the basic structure of the program output'''

        self.cats = cats
        # Adds up total time
        self.tut_time = sum(self.cats.times['sup'].values())
        tut_time_str = make_human_readable(self.tut_time)
        self.final_lst = [
            prog_title,
            'Start time: {}'.format(self.cats.beg_str),
            '',
            '== Time Totals ==',
            '',
            'Total used time: ' + tut_time_str,
            ''
        ]


    def show_menu_info(self, duration):
        '''Inserts components appearing only in menu output'''

        # Gets unused time and puts in human-readable string
        unused_sec = (datetime.now()-self.cats.rolling_time).total_seconds()
        uu_time_str = make_human_readable(unused_sec)
        all_time_str = make_human_readable(self.tut_time + unused_sec)

        # Calculates end of day considering lunch isn't included in full day
        # PER CURRENT VERSION, "Lunch" IS A NECESSARY CATEGORY (See README)
        et_w_lunch = (self.cats.end_time +
            timedelta(seconds=self.cats.times['sub']['Lunch'])
        )
        wrkdy_hrs_mins = str(duration).split(':')
        wrkdy_hrs_mins.pop()  # to remove the unneeded "seconds"
        wrkdy_hrs_mins = [int(i) for i in wrkdy_hrs_mins]  # no zero-padding!

        eod = 'Time after {} hrs {} mins: {}'.format(*wrkdy_hrs_mins,
                                                     self.cats.end_time.time())
        eod_w_lnch = 'Time plus lunch: {}'.format(et_w_lunch.time())
        unused_time_str = 'Total unused time: ' + uu_time_str
        total_time_str = 'Total Time: ' + all_time_str
        opts_heading = '== Options =='

        self.final_lst.insert(2, eod)
        self.final_lst.insert(3, eod_w_lnch)

        # Determines the line of "Total Used time" for unused and total time
        unused_ins = [
            i for i, s in enumerate(self.final_lst) if 'Total used time' in s
        ][0]
        self.final_lst.insert(unused_ins+1, total_time_str)
        self.final_lst.insert(unused_ins, unused_time_str)
        self.final_lst.insert((unused_ins+4), opts_heading)

        # Inserts the categories as numbered options, as well
        # as other options defined by the TimedCategories class,
        # into the menu print list
        opt_tbl = '{0:<3}{1:.>22}'  # makes justified options box 25 wide

        # Determines line number for insterting options
        o_ins = [
            i+1 for i, s in enumerate(self.final_lst) if 'Options' in s
        ][0]

        # inserts justified table into output list to center the whole table
        for opt, cat in self.cats.options['sub'].items():
            self.final_lst.insert(o_ins, opt_tbl.format(opt, ' ' + cat))
            o_ins += 1
        self.final_lst.insert(o_ins, '')


    def show_time_totals(self):
        '''Inserts the times into the output after sub-heading
        Time Totals. Used in menu, as well as in the summary'''

        # Determines line number for inserting times to lines under Time Totals
        tt_ins = [
            i+2 for i, s in enumerate(self.final_lst) if 'Time Totals' in s
        ][0]

        # Inserts centered table into output list
        for sup_cat,sub_cats in categories.lists.items():

            sp_time = self.cats.times['sup'][sup_cat]
            if sp_time > 0:
                spcat_string = '--------- {} ---------'.format(sup_cat)
                sptime_string = '{}\n'.format(make_human_readable(sp_time))
                self.final_lst.insert(tt_ins, sptime_string)
                self.final_lst.insert(tt_ins, spcat_string)
                tt_ins += 2

            for sub_cat in sub_cats:

                sb_time = self.cats.times['sub'][sub_cat]
                if sb_time > 0:
                    sbcat_string = '-- {} --'.format(sub_cat)
                    sbtime_string = '{}\n'.format(make_human_readable(sb_time))
                    self.final_lst.insert(tt_ins, sbtime_string)
                    self.final_lst.insert(tt_ins, sbcat_string)
                    tt_ins += 2


    def print_menu(self, duration):
        '''Prints out a formatted menu'''

        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen

        # Insert lines into final output string
        self.show_menu_info(duration)
        self.show_time_totals()

        # Prints each line centered from output_list
        print_centered_61(self.final_lst)


    def print_write_summary(self):
        '''prints summary and records to a file'''
        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen

        # Insert lines into final output string
        self.show_time_totals()

        # Prints each line centered from output_list
        print_centered_61(self.final_lst)

        # Create and/or write to output file
        file_date = self.cats.beginning.strftime('%Y-%m-%d')
        ## JH file_name = 'Time_Log_{}_test.txt'.format(file_date)
        file_name = 'Time_Log_{}.txt'.format(file_date)

        ## Writes, either new file or append
        with open(file_name, 'a+') as sum_file:
            sum_file.write('_'*61+'\n')
            for line in self.final_lst:
                sum_file.write('{0:^61}\n'.format(line))
