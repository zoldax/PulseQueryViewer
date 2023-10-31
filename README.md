# PulseQueryViewer for IBM QRadar

## 📚 Table of Contents
1. [Description](#description)
2. [Details](#details)
3. [Requirements](#requirements)
4. [Usage](#usage)
5. [Inputs](#inputs)
6. [Outputs](#outputs)
7. [Functionalities and Key Functions](#functionalities-and-key-functions)
8. [Error Handling](#error-handling)
9. [Notes](#notes)
10. [Disclaimer](#disclaimer)

## 📝 Description
PulseQueryViewer is a Python script designed to parse QRadar Pulse dashboard JSON exports, displaying the query results in a color-coded console output or converting them to a CSV file. It is meant for users who work with QRadar and need a quick and efficient way to view the AQL queries associated to dasboard widgets.

## 🛠 Details
**Author:** Pascal Weber (zoldax)  
**Version:** 1.0  
**License:** Apache License, Version 2.0

The script is designed to be user-friendly and efficient.

## 🔒 Requirements
- Python 3.x
- `argparse`, `json`, `sys`, `logging`, `csv` libraries (usually included with Python 3.x)

## 🚀 Usage
```bash
python PulseQueryViewer.py -f input_file.json [-c output_file.csv]
```

**Parameters:**
- `-f, --file`: Specify the input JSON file (required).
- `-c, --csv`: Specify the output CSV file (optional).
- `--version`: Show the version of the script.


## 📥 Inputs
- A JSON file exported from QRadar containing the query results.

## 📤 Outputs
- Console output of the parsed data with color-coded information.
- A CSV file of the parsed data (if specified with the `-c` option).

## 🎯 Functionalities and Key Functions
- **load_json:** Loads the JSON Pulse exported Dashboard file and extracts the queries and dashboard name.
- **extract_queries:** Extracts query information and populates the results list.
- **write_csv:** Writes the results to a CSV file.
- **print_results:** Prints the results to the console with color-coded output.
- **log_and_exit:** Logs an error message to ERROR.log, prints it to the console, and exits the script.

## 🚫 Error Handling
The script includes error handling for various scenarios such as missing input files, incorrect file extensions, and issues during file processing. All errors are logged to `ERROR.log`.

## 📝 Notes
- Make sure that the input JSON file follows the QRadar Pulse Dashboard export format.
- The script is case-sensitive when dealing with file paths and extensions.

## ⚠️ Disclaimer
This script is provided "as is," without warranty of any kind. The author and contributors are not responsible for any issues arising from the use of this script. By using this script, you agree to the terms and conditions of the Apache License, Version 2.0.

Q1 LABS, QRADAR and the 'Q' Logo are trademarks or registered trademarks of IBM Corp. All other trademarks are the property of their respective owners.

IBM, the IBM logo, and ibm.com are trademarks or registered trademarks of International Business Machines Corp., registered in many jurisdictions worldwide. Other product and service names might be trademarks of IBM or other companies.
