# Categories
'''This will turn the comma-separated lists in "THE_FILE" into a dictionary
where the first item is the key while the other items become a list as the
value'''

import sys
import json

THE_FILE = 'categories.json'

def load_json_to_dict(file_path=THE_FILE):
    try:
        with open(THE_FILE, 'r') as json_file:
            lists = json.load(json_file)
    except FileNotFoundError:
        sys.exit('{} not found. Please refer to the README'.format(THE_FILE))


if __name__ == "__main__":
    # This block will only run if the script is executed directly
    pass