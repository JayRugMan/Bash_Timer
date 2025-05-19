#!/usr/bin/python3
'''
This script tracks time for deltas for specified category
'''


from python_timer_stuff import get_starting_input
from python_timer_stuff import TimedCategories
from python_timer_stuff import TheOutput
from python_timer_stuff import del_file, save_state, load_saved


def main():
    '''Main Event'''
    the_categories = load_saved()
    title = "=== Jason's TimeCard ==="
    if the_categories is None:
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
        # Class object for time clocks
        the_categories = TimedCategories(beginning, workday)
        save_state(the_categories)

    while True:
        menu = TheOutput(title, the_categories)
        menu.print_menu()
        while True:
            selection = input(': ')
            if selection in the_categories.options['sub']:
                break
        try:
            selection = int(selection)
            the_categories.add_time(str(selection))
            save_state(the_categories)
            continue
        except ValueError:
            # Refreshes menu with updated info, because "now" has changed
            if selection == 'r':
                the_categories.lastAction = 'refreshed time'
                continue
            if selection == 'a':  # Add a category
                the_categories.add_sub_category()  # will modify specified file
##JH            if selection == 's':  # Save timer state
##JH                save_state(the_categories)
            if selection == 'q':  # Summary and quit
                print(selection)
                summary = TheOutput(title, the_categories)
                summary.print_write_summary()
                del_file()  # Deletes any state file
                break


main()
