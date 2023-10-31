#!/usr/bin/env python3

"""
PulseQueryViewer: A script to parse QRadar JSON exports, displaying the data in console or converting it to CSV.

Author: Pascal Weber (zoldax)

   Copyright 2023 Pascal Weber (zoldax) / Abakus Sécurité

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Usage:
    python PulseQueryViewer.py -f input_file.json [-c output_file.csv]

Parameters:
    -f, --file: Specify the input JSON file (required).
    -c, --csv: Specify the output CSV file (optional).
    --version: Show the version of the script.

Outputs:
    - Console output of the parsed data.
    - CSV file of the parsed data (if specified).
"""

import json
import sys
import logging
import argparse
import csv
from typing import List, Dict, Optional

# Setting up logging
logging.basicConfig(filename='ERROR.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class PulseQueryViewer:
    """
    A class to parse QRadar JSON exports and convert them to a readable format or CSV.

    Attributes:
        json_file (str): The path to the input JSON file.
        csv_file (Optional[str]): The path to the output CSV file (if specified).
        results (List[Dict]): A list to store the parsed query results.
        dashboard_name (str): The name of the global dashboard.
    """

    def __init__(self, json_file: str, csv_file: Optional[str] = None) -> None:
        """
        The constructor for PulseQueryViewer class.

        Parameters:
            json_file (str): The path to the input JSON file.
            csv_file (Optional[str]): The path to the output CSV file (if specified).
        """
        self.json_file = json_file
        self.csv_file = csv_file
        self.results = []
        self.dashboard_name = ""

    def run(self) -> None:
        """
        The main method to control the flow of the script.
        """
        if not self.json_file.endswith('.json'):
            self.log_and_exit("The file must have a .json extension")
        
        self.load_json()
        self.extract_queries()
        
        if self.csv_file:
            self.write_csv()
        else:
            self.print_results()

    def load_json(self) -> None:
        """
        Loads the JSON file and extracts the queries and dashboard name.
        """
        try:
            with open(self.json_file, 'r') as f:
                data_dict = json.load(f)
        except json.JSONDecodeError as e:
            self.log_and_exit(f"Failed to decode JSON file: {str(e)}")
        except FileNotFoundError:
            self.log_and_exit("The specified JSON file was not found.")
        except Exception as e:
            self.log_and_exit(f"An unexpected error occurred: {str(e)}")
        
        self.dashboard_name = data_dict.get('dashboards', {}).get('list', [{}])[0].get('name', '')
        self.results = data_dict.get('items', {}).get('list', [])
        
    def extract_queries(self) -> None:
        """
        Extracts query information and populates the results list.
        """
        if not self.results:
            print("No queries found in the JSON file.")
            return
        
        for count, item in enumerate(self.results, start=1):
            name = item.get('name', 'Name not found')
            query = item.get('query', {}).get('queryVal', 'Query not found').replace('\n', ' ')
            self.results[count-1] = {"Dashboard": self.dashboard_name, "Number": count, "Name": name, "Query": query}
            
    def write_csv(self) -> None:
        """
        Writes the results to a CSV file.
        """
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Dashboard', 'Number', 'Name', 'Query']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                writer.writeheader()
                line_count = 0
                for row in self.results:
                    writer.writerow(row)
                    line_count += 1
            print(f"Results have been written to {self.csv_file}")
            print(f"Total lines written: {line_count}")
        except Exception as e:
            self.log_and_exit(f"An error occurred while writing to the CSV file: {str(e)}")

    def print_results(self) -> None:
        """
        Prints the results to the console with colored output, including the Global Dashboard name.
        """
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        END = '\033[0m'

        print(f"    {YELLOW}Global Dashboard: {self.dashboard_name}{END}\n")
        
        for item in self.results:
            print(f"    {item['Number']}. {RED}Name: {item['Name']}{END}")
            print(f"    {GREEN}Query: {item['Query']}{END}\n")

    @staticmethod
    def log_and_exit(message: str) -> None:
        """
        Logs an error message to ERROR.log, prints it to the console, and exits the script.

        Parameters:
            message (str): The error message to log and print.
        """
        print(message)
        logging.error(message)
        sys.exit(1)

def main():
    """
    Main function to handle command line arguments and run the script.
    """
    script_version = "1.0"

    parser = argparse.ArgumentParser(description='PulseQueryViewer by Pascal Weber (zoldax)')
    parser.add_argument('-f', '--file', help='Name of the JSON file', required=False)
    parser.add_argument('-c', '--csv', help='Name of the output CSV file (optional)', required=False)
    parser.add_argument('--version', action='version', version=f'%(prog)s {script_version}', help='Show the version of the script and exit')

    args = parser.parse_args()

    if args.file:
        viewer = PulseQueryViewer(args.file, args.csv)
        viewer.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

