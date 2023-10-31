#!/usr/bin/env python3

import json
import sys

if len(sys.argv) != 2:
    print("Usage: python DASHreadme.py file.json")
    sys.exit(1)

filename = sys.argv[1]
if not filename.endswith('.json'):
    print("The file must have a .json extension")
    sys.exit(1)

try:
    with open(filename, 'r') as f:
        data_dict = json.load(f)
except Exception as e:
    print(f"An error occurred while reading the file: {str(e)}")
    sys.exit(1)

for item in data_dict.get('items', {}).get('list', []):
    name = item.get('name', 'Name not found')
    query = item.get('query', {}).get('queryVal', 'Query not found')
    print(f"\033[91mName: {name}\033[0m")
    print(f"\033[92mQuery: {query}\033[0m\n")


