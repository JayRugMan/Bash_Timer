# Categories
'''This will turn the comma-separated lists in "THE_FILE" into a dictionary
where the first item is the key while the other items become a list as the
value'''

import sys
import json

CAT_FILE = 'categories.json'
CATEGORIES = {}

try:
    with open(CAT_FILE, 'r') as json_file:
        CATEGORIES = json.load(json_file)
except FileNotFoundError:
    sys.exit(f'{CAT_FILE} not found. Please refer to the README')

if __name__ == "__main__":
    # This block will only run if the script is executed directly
    pass