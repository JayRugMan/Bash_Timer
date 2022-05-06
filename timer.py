#!/usr/bin/python3
'''
This script tracks time for deltas for specified category
'''

from python_timer_stuff import get_starting_input
from python_timer_stuff import TimedCategories
from python_timer_stuff import TheOutput


def main():
    '''Main Event'''
    title = "=== Jason's TimeCard ==="
    start_time_prompt = [
        title,
        '',
        'Enter 24-hour start time below as "hours minutes"',
        'or simply hit enter to continue with current time',
        ''
    ]
    total_hrs_prompt = [
        '',
        'How long are you working today ("hours minutes")?',
        'or simply hit enter to continue with 8 hours',
        ''
    ]
    beginning = get_starting_input(start_time_prompt, 'time')
    workday = get_starting_input(total_hrs_prompt, 'duration')
    ##JH beginning, workday = get_start_time(title)
    # Check for/read conf file
    the_categories = TimedCategories(beginning, workday)


    while True:
        menu = TheOutput(title, the_categories)
        menu.print_menu(workday)
        while True:
            selection = input(': ')
            if selection in the_categories.options['sub']:
                break
        try:
            selection = int(selection)
            the_categories.add_time(str(selection))
            continue
        except ValueError:
            # refreshes menu with updated info, because "now" has changed
            if selection == 'r':
                continue
            if selection == 'a':  # add a category
                the_categories.add_sub_category()  # will modify specified file
            if selection == 'q':  # Summary and quit
                print(selection)
                summary = TheOutput(title, the_categories)
                summary.print_write_summary()
                break


main()
