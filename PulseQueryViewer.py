#!/usr/bin/env python3

"""
PulseQueryViewer: A script to parse QRadar Pulse dashboard JSON exports, displaying the widget name and AQL query data in console or converting it to CSV.

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
import os
import datetime
from typing import List, Dict, Optional

# Constants
LOG_FILENAME = 'PulseQueryViewer.log'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
JSON_EXT = '.json'
CSV_EXT = '.csv'
OLD_EXT = '.old'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
END = '\033[0m'
VERSION = "PulseQueryViewer 1.1"

# Setting up logging
logging.basicConfig(filename=LOG_FILENAME, level=LOG_LEVEL, format=LOG_FORMAT)

class PulseQueryViewer:
    def __init__(self, json_file: str, csv_file: Optional[str] = None) -> None:
        self.json_file = json_file
        self.csv_file = csv_file
        self.results = []
        self.dashboard_name = ""
        logging.info(f"Initialized PulseQueryViewer with JSON file: {json_file} and CSV file: {csv_file}")

    def run(self) -> None:
        logging.debug("Running PulseQueryViewer")

        if not self.json_file.endswith(JSON_EXT):
            self.log_and_exit("The file must have a .json extension", level=logging.ERROR)

        self.load_json()
        self.extract_queries()

        if self.csv_file:
            self.handle_existing_csv()
            self.write_csv()
        else:
            self.print_results()

    def handle_existing_csv(self) -> None:
        if os.path.exists(self.csv_file):
            overwrite = input(f"The file {self.csv_file} already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Exiting without writing to CSV.")
                sys.exit(0)
            else:
                now = datetime.datetime.now()
                new_name = f"{self.csv_file[:-4]}_{now.strftime('%Y%m%d_%H%M%S')}{OLD_EXT}{CSV_EXT}"
                os.rename(self.csv_file, new_name)
                print(f"The existing file has been renamed to {new_name}")

    def load_json(self) -> None:
        logging.info("Loading JSON data")
        try:
            with open(self.json_file, 'r') as f:
                data_dict = json.load(f)
            logging.debug("JSON data loaded successfully")
        except json.JSONDecodeError as e:
            self.log_and_exit(f"Failed to decode JSON file: {str(e)}", level=logging.ERROR)
        except FileNotFoundError:
            self.log_and_exit("The specified JSON file was not found.", level=logging.ERROR)
        except Exception as e:
            self.log_and_exit(f"An unexpected error occurred: {str(e)}", level=logging.ERROR)

        self.dashboard_name = data_dict.get('dashboards', {}).get('list', [{}])[0].get('name', '')
        self.results = data_dict.get('items', {}).get('list', [])
        logging.info("Queries and Dashboard name extracted")

    def extract_queries(self) -> None:
        if not self.results:
            logging.warning("No queries found in the JSON file.")
            print("No queries found in the JSON file.")
            return

        logging.info("Extracting queries")
        for count, item in enumerate(self.results, start=1):
            name = item.get('name', 'Name not found')
            query = item.get('query', {}).get('queryVal', 'Query not found').replace('\n', ' ')
            self.results[count-1] = {"Dashboard": self.dashboard_name, "Number": count, "Name": name, "Query": query}
        logging.debug("Queries extracted and results populated")

    def write_csv(self) -> None:
        logging.info(f"Writing results to CSV file: {self.csv_file}")
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
            logging.info(f"Results written to {self.csv_file} successfully. Total lines written: {line_count}")
        except Exception as e:
            self.log_and_exit(f"An error occurred while writing to the CSV file: {str(e)}", level=logging.ERROR)

    def print_results(self) -> None:
        print(f"    {YELLOW}Global Dashboard: {self.dashboard_name}{END}\n")

        for item in self.results:
            print(f"    {item['Number']}. {RED}Name: {item['Name']}{END}")
            print(f"    {GREEN}Query: {item['Query']}{END}\n")
        print("Total queries:", len(self.results))
        logging.info(f"Results printed to console successfully. Total queries: {len(self.results)}")

    def log_and_exit(self, msg: str, level: int) -> None:
        logging.log(level, msg)
        print(msg)
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse QRadar Pulse dashboard JSON exports.")
    parser.add_argument("-f", "--file", required=True, help="Specify the input JSON file")
    parser.add_argument("-c", "--csv", help="Specify the output CSV file")
    parser.add_argument("--version", action="version", version=VERSION)
    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def main() -> None:
    args = parse_arguments()
    viewer = PulseQueryViewer(args.file, args.csv)
    viewer.run()

if __name__ == "__main__":
    main()

