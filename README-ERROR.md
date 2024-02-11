# PulseQueryViewer Error Handling and Logging Summary 📜

This document provides a summary of the error handling and logging capabilities of the PulseQueryViewer tool.

### 🖋️ Author
- **Pascal Weber (zoldax)**

## Table of Contents 📑

1. [Input Validation](#input-validation)
2. [File Handling](#file-handling)
3. [JSON Parsing](#json-parsing)
4. [Data Extraction](#data-extraction)
5. [Output Writing](#output-writing)
6. [Miscellaneous](#miscellaneous)

## Input Validation 📋

- **Missing Input**: 
  - **Error**: The script checks if the user has provided the required JSON files as input. If no files are specified, an error message is displayed.
  - **Logging**: The error along with a timestamp is logged to a designated error log file.

- **File Extension Check**: 
  - **Error**: The script ensures that the provided input files have a `.json` extension. If not, an error message is displayed.
  - **Logging**: The error and the name of the incorrectly formatted file are logged.

## File Handling 📁

- **File Existence**: 
  - **Error**: Before attempting to open a file, the script checks if the file exists. If a specified file is not found, an error message is displayed.
  - **Logging**: The error and the name of the missing file are logged.

- **File Permissions**: 
  - **Error**: The script checks for the necessary file permissions before reading from or writing to a file. If permissions are lacking, an error message is displayed.
  - **Logging**: The error, file name, and required permissions are logged.

## JSON Parsing 📊

- **Format Validation**: 
  - **Error**: The script validates the format of the JSON data. If the data is not valid JSON, an error message is displayed.
  - **Logging**: The error and details of the invalid format are logged.

- **Data Integrity**: 
  - **Error**: The script checks the integrity of the required data fields in the JSON file. If expected fields are missing or have incorrect data types, an error message is displayed.
  - **Logging**: The error and details of the missing or incorrect fields are logged.

## Data Extraction 📈

- **Empty Data**: 
  - **Error**: If the JSON file does not contain any queries or the required data, the script handles this gracefully and informs the user that no data was found.
  - **Logging**: A message stating that no data was found is logged along with the file name.

## Output Writing 📝

- **CSV Writing**: 
  - **Error**: The script handles errors that might occur while writing to a CSV file, such as permission issues or disk space issues, and displays an appropriate error message.
  - **Logging**: The error, along with details such as file name and possible reasons, are logged.

- **Markdown Writing**: 
  - **Error**: Similarly, errors encountered while writing to a Markdown file are caught, and an error message is displayed.
  - **Logging**: The error and relevant details are logged.

## Miscellaneous 🛠️

- **Argument Parsing**: 
  - **Error**: The script provides error handling for command-line arguments, ensuring that the user is informed of any incorrect usage or invalid options.
  - **Logging**: Any argument parsing errors are logged, along with suggestions for correct usage.

- **Graceful Termination**: 
  - **Error**: In any error scenario, the script aims to terminate gracefully, providing clear error messages and not leaving any partial or corrupt output files.
  - **Logging**: A termination message is logged, indicating whether the script ended successfully or due to an error.

---

By handling these various error scenarios and logging pertinent information, PulseQueryViewer aims to provide a robust, user-friendly, and traceable experience.

