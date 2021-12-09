#!/usr/bin/python3
'''
This script tracks time for deltas for specified category
'''

from datetime import datetime
from datetime import timedelta
from python_timer_stuff import TimedCategories
from python_timer_stuff import TheOutput


def make_human_readable(time_in_seconds):
    '''Takes seconds and returns formatted string'''
    str_format = '{} Hr(s), {} Min(s), {} Sec(s)'
    time_list = str(timedelta(seconds=int(time_in_seconds))).split(':')
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
            break
        # Checks whether entry is integers in suggested format
        try:
            hrs = int(user_input[0:2])
            mins = int(user_input[3:5])
        except ValueError:
            print("-- Error - enter time integers as suggested")
            continue
        # Checks whether string is an actual time and exits loop
        if 0 <= hrs < 25 and 0 <= mins < 60:
            del hrs, mins
            break
        print('-- Error - enter a valid time as suggested')

    # If the output type is to be a time
    if output_type == 'time':
        # Sets start date string as "YYYY MM DD"
        start_d_str = datetime.now().date().strftime('%Y %m %d')
        # This if no time is entered, meaning default was chosen
        if not user_input:
            user_input = datetime.now().strftime('%H %M')
        start_dt_str = '{} {}'.format(start_d_str, user_input)
        final_output = datetime.strptime(start_dt_str, '%Y %m %d %H %M')
        del start_d_str, start_dt_str

    # If the output type is to be a duration
    if output_type == 'duration':
        if not user_input:
            user_input = '08 00'
        final_output = timedelta(hours=int(user_input[0:2]),
                               minutes=int(user_input[3:5]))

    del prompt_text_lst, user_input, output_type
    return final_output


def main():
    '''Main Event'''

    title = "=== Jason's TimeCard ==="
    ##JH conf_file = 'timerpy.conf'
    conf_file = 'timerpy_test.conf'

    start_time_prompt = [
        title,
        '',
        'Enter start time below in 24-hour format as hh mm',
        'or simply hit enter to continue with current time',
        ''
    ]

    total_hrs_prompt = [
        '',
        'How many hours are you working today (hh mm)?',
        'or simply hit enter to continue with 8 hours',
        ''
    ]

    beginning = get_starting_input(start_time_prompt, 'time')
    workday = get_starting_input(total_hrs_prompt, 'duration')
    ##JH beginning, workday = get_start_time(title)
    # Check for/read conf file
    categories = TimedCategories(conf_file, beginning, workday)

    while True:
        menu = TheOutput(title, categories)
        menu.print_menu(workday)
        while True:
            selection = input(': ')
            if selection in categories.options:
                break
        try:
            selection = int(selection)
            categories.add_time(str(selection))
            continue
        except ValueError:
            # refreshes menu with updated info, because "now" has changed
            if selection == 'r':
                continue
            if selection == 'a':  # add a category
                categories.add_category(conf_file)  # will modify specified file
            if selection == 'q':  # Summary and quit
                print(selection)
                summary = TheOutput(title, categories)
                summary.print_write_summary()
                break


main()
