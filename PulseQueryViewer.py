#!/usr/bin/env python3

"""
PulseQueryViewer: A tool for viewing queries and other details from a JSON file related to QRadar dashboards.

Author: Pascal Weber (zoldax)
"""

import json
import sys
import logging
import argparse
import csv
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(filename='ERROR.log', level=logging.ERROR)


class PulseQueryViewer:
    def __init__(self, filename: str, csv_filename: Optional[str] = None):
        self.filename = filename
        self.csv_filename = csv_filename
        self.data_dict = {}
        self.results = []
        self.global_dashboard_name = ""

    def read_json_file(self):
        """Reads the JSON file and populates the data_dict attribute with its content."""
        if not self.filename.endswith('.json'):
            error_message = "The file must have a .json extension"
            print(error_message)
            logging.error(error_message)
            sys.exit(1)

        try:
            with open(self.filename, 'r') as f:
                self.data_dict = json.load(f)
        except Exception as e:
            error_message = f"An error occurred while reading the file: {str(e)}"
            print(error_message)
            logging.error(error_message)
            sys.exit(1)

    def extract_queries(self):
        """Extracts queries and related information from the data dictionary."""
        self.global_dashboard_name = self.data_dict.get('dashboards', {}).get('list', [])[0].get('name', 'Global Dashboard Name Not Found')
        for count, item in enumerate(self.data_dict.get('items', {}).get('list', []), start=1):
            name = item.get('name', 'Name not found')
            query = item.get('query', {}).get('queryVal', 'Query not found').replace('\n', ' ')
            self.results.append({"Global Dashboard": self.global_dashboard_name, "Number": count, "Name": name, "Query": query})

    def display_results(self):
        """Prints the extracted information to the console."""
        print(f"Global Dashboard: {self.global_dashboard_name}\n")
        for result in self.results:
            print(f"{result['Number']}. \033[91mName: {result['Name']}\033[0m")
            print(f"\033[92mQuery: {result['Query']}\033[0m\n")

    def save_to_csv(self):
        """Saves the extracted information to a CSV file."""
        if self.csv_filename:
            try:
                with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Global Dashboard', 'Number', 'Name', 'Query']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                    writer.writeheader()
                    for row in self.results:
                        writer.writerow(row)
                print(f"Results have been written to {self.csv_filename}")
            except Exception as e:
                error_message = f"An error occurred while writing to the CSV file: {str(e)}"
                print(error_message)
                logging.error(error_message)
                sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='PulseQueryViewer: A tool for viewing QRadar dashboard queries and details.')
    parser.add_argument('-f', '--file', help='Name of the JSON file', required=True)
    parser.add_argument('-c', '--csv', help='Name of the output CSV file (optional)')
    args = parser.parse_args()

    viewer = PulseQueryViewer(args.file, args.csv)
    viewer.read_json_file()
    viewer.extract_queries()

    if args.csv:
        viewer.save_to_csv()
    else:
        viewer.display_results()


if __name__ == "__main__":
    main()

