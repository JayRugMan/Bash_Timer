import dill
import os
from datetime import datetime, timedelta


def save_state(the_class):
    '''This saves the dictionary to pick up and use again so timers can persist a reboot'''
    the_file = '.timer_saved_state.pkl'
    with open(the_file, 'wb') as file:
        dill.dump(the_class, file)
    the_class.lastAction = f'saved state to {the_file}'


def load_saved():
    the_file = '.timer_saved_state.pkl'
    try:
        # Get "now"
        now = datetime.now()
        # Get file's date/time if it exists
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(the_file))
        # If it's older than 8 hours, delete it
        if now - file_mod_time > timedelta(hours=8):
            os.remove(the_file)
            return None
        # if it's not older than 8 hours, open it and load into the active script
        with open(the_file, 'rb') as file:
            the_class = dill.load(file)
        the_class.lastAction = 'loaded state from file'
        return the_class
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    # This block will only run if the script is executed directly
    pass
