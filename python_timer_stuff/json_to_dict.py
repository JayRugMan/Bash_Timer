# Categories
'''This will turn the comma-separated lists in "THE_FILE" into a dictionary
where the first item is the key while the other items become a list as the
value'''

import sys
import json

THE_FILE = 'categories.json'

try:
    with open(THE_FILE, 'r') as json_file:
        lists = json.load(json_file)
except FileNotFoundError:
    sys.exit('{} not found. Please refer to the README'.format(THE_FILE))
