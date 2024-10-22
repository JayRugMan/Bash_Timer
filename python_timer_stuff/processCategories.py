import json
from datetime import datetime
from calendar import day_abbr
from json_to_dict import CATEGORIES, CAT_FILE


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
        for sup_cat,sub_cats in CATEGORIES.items():
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
        for spcat,sbcats in CATEGORIES.items():
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
                CATEGORIES[newsubs_supcat].append(new_subcat)
                break
        # Adds the new category to the json file
        with open(CAT_FILE, 'w') as json_file:
            json_file.write(
                json.dumps(
                    CATEGORIES, sort_keys=True, indent=2
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


if __name__ == "__main__":
    # This block will only run if the script is executed directly
    pass
