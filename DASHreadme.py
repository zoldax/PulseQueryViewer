#!/usr/bin/env python3

import json
import sys
import logging

# Set up logging
logging.basicConfig(filename='ERROR.log', level=logging.ERROR)

if len(sys.argv) != 2:
    error_message = "Usage: python DASHreadme.py file.json"
    print(error_message)
    logging.error(error_message)
    sys.exit(1)

filename = sys.argv[1]
if not filename.endswith('.json'):
    error_message = "The file must have a .json extension"
    print(error_message)
    logging.error(error_message)
    sys.exit(1)

try:
    with open(filename, 'r') as f:
        data_dict = json.load(f)
except Exception as e:
    error_message = f"An error occurred while reading the file: {str(e)}"
    print(error_message)
    logging.error(error_message)
    sys.exit(1)

for count, item in enumerate(data_dict.get('items', {}).get('list', []), start=1):
    name = item.get('name', 'Name not found')
    query = item.get('query', {}).get('queryVal', 'Query not found')
    print(f"{count}. \033[91mName: {name}\033[0m")
    print(f"\033[92mQuery: {query}\033[0m\n")

