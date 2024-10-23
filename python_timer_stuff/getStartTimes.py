from datetime import datetime
from datetime import timedelta
from .processOutput import print_centered_61


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
            if len(user_input.split(' ')) == 1:
                user_input = f"{user_input} 0"
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
            if output_type == 'time':
                # Create a datetime object for the entered time
                entered_time = datetime.now().replace(hour=hrs, minute=mins, second=0, microsecond=0)
                # Check if the entered time is before the current time
                if entered_time < datetime.now():
                    break
                else:
                    print('-- Error - entered time is not before the current time')
            else:
                break
        else:
            print('-- Error - enter a valid time as suggested')
    # If the output type is to be a time
    if output_type == 'time':
        # Sets start date string as "YYYY MM DD"
        start_d_str = datetime.now().date().strftime('%Y %m %d')
        start_dt_str = f'{start_d_str} {user_input}'
        final_output = datetime.strptime(start_dt_str, '%Y %m %d %H %M')
        del start_d_str, start_dt_str
    # If the output type is to be a duration
    if output_type == 'duration':
        final_output = timedelta(hours=hrs,
                               minutes=mins)
    del prompt_text_lst, user_input, output_type, hrs, mins
    return final_output


if __name__ == "__main__":
    # This block will only run if the script is executed directly
    pass