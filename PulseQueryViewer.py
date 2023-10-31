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

# Constants to maintain easily configurable values at the top of the script
LOG_FILENAME = 'PulseQueryViewer.log'  # Log file name
LOG_LEVEL = logging.DEBUG              # Logging level
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'  # Logging format
JSON_EXT = '.json'                     # Expected JSON file extension
CSV_EXT = '.csv'                       # Expected CSV file extension
OLD_EXT = '.old'                       # Extension for old files during overwriting
RED = '\033[91m'                       # ANSI code for red color
GREEN = '\033[92m'                     # ANSI code for green color
YELLOW = '\033[93m'                    # ANSI code for yellow color
END = '\033[0m'                        # ANSI code to end coloring
VERSION = "PulseQueryViewer 1.1"       # Version of the script

# Configure logging to write logs to file and print them on the console
logging.basicConfig(filename=LOG_FILENAME, level=LOG_LEVEL, format=LOG_FORMAT)

class PulseQueryViewer:
    """
    Main class to handle parsing and displaying of QRadar Pulse dashboard queries.
    """
    def __init__(self, json_file: str, csv_file: Optional[str] = None) -> None:
        """
        Initializes the PulseQueryViewer with input and output file paths.

        :param json_file: Path to the input JSON file.
        :param csv_file: Optional path to the output CSV file.
        """
        self.json_file = json_file
        self.csv_file = csv_file
        self.results = []
        self.dashboard_name = ""
        logging.info(f"Initialized PulseQueryViewer with JSON file: {json_file} and CSV file: {csv_file}")

    def run(self) -> None:
        """
        Main execution method to parse queries and display or save them.
        """
        logging.debug("Running PulseQueryViewer")

        # Check if the file has a .json extension
        if not self.json_file.endswith(JSON_EXT):
            self.log_and_exit("The file must have a .json extension", level=logging.ERROR)

        self.load_json()       # Load and parse the JSON file
        self.extract_queries() # Extract queries from the loaded JSON data

        if self.csv_file:      # If CSV file is specified, write the results to it
            self.handle_existing_csv()
            self.write_csv()
        else:                  # Otherwise, print the results to console
            self.print_results()

    def handle_existing_csv(self) -> None:
        """
        Handles existing CSV file if the specified output file already exists.
        """
        if os.path.exists(self.csv_file):
            overwrite = input(f"The file {self.csv_file} already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Exiting without writing to CSV.")
                sys.exit(0)
            else:
                # Rename existing file by appending a timestamp and '.old' before the '.csv' extension
                now = datetime.datetime.now()
                new_name = f"{self.csv_file[:-4]}_{now.strftime('%Y%m%d_%H%M%S')}{OLD_EXT}{CSV_EXT}"
                os.rename(self.csv_file, new_name)
                print(f"The existing file has been renamed to {new_name}")

    def load_json(self) -> None:
        """
        Loads and parses the input JSON file.
        """
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

        # Extract dashboard name and results (queries) from the loaded JSON data
        self.dashboard_name = data_dict.get('dashboards', {}).get('list', [{}])[0].get('name', '')
        self.results = data_dict.get('items', {}).get('list', [])
        logging.info("Queries and Dashboard name extracted")

    def extract_queries(self) -> None:
        """
        Extracts and formats queries from the loaded JSON data.
        """
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
        """
        Writes the extracted queries to a CSV file.
        """
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
        except PermissionError:
            self.log_and_exit("Permission denied to write to the specified CSV file. Please check the file permissions.", level=logging.ERROR)
        except Exception as e:
            self.log_and_exit(f"An error occurred while writing to the CSV file: {str(e)}", level=logging.ERROR)

    def print_results(self) -> None:
        """
        Prints the extracted queries to the console.
        """
        if not self.results:
            print("No queries to display.")
            return

        print(f"\n{YELLOW}Dashboard: {self.dashboard_name}{END}")
        for item in self.results:
            print(f"\nWidget Number: {item['Number']}")
            print(f"{RED}    Name: {item['Name']}{END}")
            print(f"{GREEN}    Query: {item['Query']}{END}")

    def log_and_exit(self, message: str, level: int = logging.INFO) -> None:
        """
        Logs a message and exits the program.

        :param message: The message to log and print.
        :param level: The logging level to use (default is INFO).
        """
        logging.log(level, message)
        print(RED + message + END)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse QRadar Pulse dashboard queries from JSON exports.")
    parser.add_argument("-f", "--file", help="Specify the input JSON file.", required=True)
    parser.add_argument("-c", "--csv", help="Specify the output CSV file. (optional)", required=False)
    parser.add_argument("--version", help="Show the version of the script", action='version', version=VERSION)

    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    # Initialize and run the PulseQueryViewer
    pqv = PulseQueryViewer(json_file=args.file, csv_file=args.csv)
    pqv.run()

