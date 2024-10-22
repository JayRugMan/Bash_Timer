import os
from datetime import datetime
from datetime import timedelta
from json_to_dict import CATEGORIES


def make_human_readable(time_in_seconds):
    '''Takes seconds and returns formatted string'''
    str_format = '{}h {}m {}s ({:.3f})'
    time_list = str(timedelta(seconds=int(time_in_seconds))).split(':')
    # Turn each list item from string to integer
    time_list = [int(i) for i in time_list]
    time_as_strng = str_format.format(*time_list, (time_list[0]+
                                                   time_list[1]/60+
                                                   time_list[2]/3600))
    del str_format, time_list
    return time_as_strng


def print_centered_61(the_output_lst):
    '''Prints the lines in the list provided centered in 61 characters'''
    for line in the_output_lst:
        print('{0:^61}'.format(line))


class TheOutput:
    '''Class defining the menu or summary output to be printed'''
    def __init__(self, prog_title, cats):
        '''starts the basic structure of the program output'''
        self.cats = cats
        # Adds up total time
        self.tut_time = sum(self.cats.times['sup'].values())
        tut_time_str = make_human_readable(self.tut_time)
        self.tut_str = 'Total used time: ' + tut_time_str
        self.tt_str = '========= Time Totals ========='
        self.final_lst = [
            prog_title,
            'Start time: {}'.format(self.cats.beg_str),
            '',
            self.tt_str,
            '',
            self.tut_str,
            ''
        ]
    def insert_tot_minus_lunch(self, ins_num):
        '''This should get called if the "Lunch" category exists and is
        more than 0. It subtracts total lunch time from total time'''
        tt_minus_lunch = self.tut_time - self.cats.times['sub']['Lunch']
        ttml_str = 'Used minus lunch: ' + make_human_readable(tt_minus_lunch)
        self.final_lst.insert(ins_num, ttml_str)
    def insert_eod_plus_lunch(self):
        '''This should get called if the "Lunch" category exists
        and is more than 0. It adds lunch to the end-of-day time'''
        et_w_lunch = (self.cats.end_time +
            timedelta(seconds=self.cats.times['sub']['Lunch'])
        )
        eod_w_lnch = 'Time plus lunch: {}'.format(et_w_lunch.time())
        self.final_lst.insert(3, eod_w_lnch)
    def show_menu_info(self, duration):
        '''Inserts components appearing only in menu output'''
        # Gets unused time and puts in human-readable string
        unused_sec = (datetime.now()-self.cats.rolling_time).total_seconds()
        uu_time_str = make_human_readable(unused_sec)
        all_time_str = make_human_readable(self.tut_time + unused_sec)
        # Calculates end of day considering lunch isn't included in full day
        # PER CURRENT VERSION, "Lunch" IS A NECESSARY CATEGORY (See README)
        ##JH et_w_lunch = (self.cats.end_time +
        ##JH     timedelta(seconds=self.cats.times['sub']['Lunch'])
        ##JH )
        wrkdy_hrs_mins = str(duration).split(':')
        wrkdy_hrs_mins.pop()  # to remove the unneeded "seconds"
        wrkdy_hrs_mins = [int(i) for i in wrkdy_hrs_mins]  # no zero-padding!
        # End of day
        eod = 'Time after {} hrs {} mins: {}'.format(*wrkdy_hrs_mins,
                                                     self.cats.end_time.time())
        unused_time_str = 'Total unused time: ' + uu_time_str
        total_time_str = 'Total Time: ' + all_time_str
        opts_heading = '======== Options ========'
        ## Inserts headings and totals
        self.final_lst.insert(2, eod)
        # Determines the line of "Total Used time" for unused and total time
        used_ins = self.final_lst.index(self.tut_str)
        self.final_lst.insert(used_ins+1, total_time_str)
        self.final_lst.insert(used_ins, unused_time_str)
        self.final_lst.insert((used_ins+4), opts_heading)
        try:
            if self.cats.times['sup']['Lunch']:
                if self.cats.times['sub']['Lunch'] > 0:
                    self.insert_eod_plus_lunch()
        except KeyError:
            self.final_lst.insert(3, "See README about Lunch")
        # Inserts the categories as numbered options, as well
        # as other options defined by the TimedCategories class,
        # into the menu print list
        opt_tbl = '{0:<3}{1:.>22}'  # makes justified options box 25 wide
        # Determines line number after options heading for insterting options
        o_ins = self.final_lst.index(opts_heading) + 1
        # inserts justified table into output list to center the whole table
        for opt, cat in self.cats.options['sub'].items():
            self.final_lst.insert(o_ins, opt_tbl.format(opt, ' ' + cat))
            o_ins += 1
        self.final_lst.insert(o_ins, '')
    def show_time_totals(self):
        '''Inserts the times into the output after sub-heading
        Time Totals. Used in menu, as well as in the summary'''
        # Determines line number for inserting times to lines under Time Totals
        tt_ins = self.final_lst.index(self.tt_str) + 1
        multi_cats = False
        # Inserts centered table into output list
        for sup_cat, sub_cats in CATEGORIES.items():
            sp_time = self.cats.times['sup'][sup_cat]
            if sp_time > 0:
                # for adding space buffer when more than one super cat
                if multi_cats:
                    self.final_lst.insert(tt_ins, ' ')
                    tt_ins += 1
                else:
                    multi_cats = True
                cat_times_str = '--- {}: {} ---'.format(
                    sup_cat,
                    make_human_readable(sp_time)
                )
                for sub_cat in sub_cats:
                    sb_time = self.cats.times['sub'][sub_cat]
                    if sb_time > 0:
                        cat_times_str += '\n{}: {}'.format(
                            sub_cat,
                            make_human_readable(sb_time)
                        )
                for sub_line in cat_times_str.split('\n'):
                    self.final_lst.insert(tt_ins, sub_line)
                    tt_ins += 1
        # take lunch duration away from total time
        used_ins = self.final_lst.index(self.tut_str) + 1
        try:
            if self.cats.times['sup']['Lunch']:
                if self.cats.times['sub']['Lunch'] > 0:
                    self.insert_tot_minus_lunch(used_ins)
        except KeyError:
            self.final_lst.insert(used_ins, "No Lunch today")
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


if __name__ == "__main__":
    # This block will only run if the script is executed directly
    pass