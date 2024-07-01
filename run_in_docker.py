import configparser  # Module for configuration file parsing
import os  # Module to interact with the operating system
import re  # Module for regular expressions
import pandas as pd  # Module for data manipulation and analysis
from concurrent.futures import ThreadPoolExecutor  # Module for parallel processing
import logging  # Module for logging

class LogProcessor:
    def __init__(self, directories, file_pattern):
        """
        Initialize the LogProcessor with directories to scan for log files and file pattern to match.
        :param directories: List of directories containing log files.
        :param file_pattern: Pattern to match log files.
        """
        self.directories = directories
        self.file_pattern = re.compile(file_pattern)
        self.user_code_pattern = re.compile(r"userCode=(\w+)")
        self.user_id_pattern = re.compile(r'"userId":"(\w+)"')
        self.user_codes = set()
        logging.info('LogProcessor initialized with directories: %s and file pattern: %s', directories, file_pattern)

    def process_log_files(self):
        """
        Process each log file in the specified directories to extract user identifiers.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._process_single_file, os.path.join(directory, filename))
                for directory in self.directories
                for filename in os.listdir(directory)
                if self.file_pattern.match(filename)
            ]

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logging.error('Error processing file: %s', e)

    def _process_single_file(self, filepath):
        """
        Process a single log file to extract user identifiers.
        :param filepath: Path to the log file.
        """
        line_count = 0
        try:
            with open(filepath, 'r', errors='ignore') as file:
                for line in file:
                    self._extract_user_identifiers(line)
                    line_count += 1
            logging.info('Processed file: %s with %d lines', filepath, line_count)
        except Exception as e:
            logging.error('Error processing file %s: %s', filepath, e)

    def _extract_user_identifiers(self, line):
        """
        Extract user identifiers from a single line of log.
        :param line: A single line from the log file.
        """
        try:
            match_code = self.user_code_pattern.search(line)
            match_id = self.user_id_pattern.search(line)
            if match_code:
                self.user_codes.add(match_code.group(1))
            if match_id:
                self.user_codes.add(match_id.group(1))
        except Exception as e:
            logging.error('Error extracting identifiers from line: %s', e)

    def save_to_csv(self, output_path):
        """
        Save the extracted user identifiers to a CSV file.
        :param output_path: Path to save the output CSV file.
        """
        try:
            df = pd.DataFrame(list(self.user_codes), columns=["userIdentifier"])
            df.to_csv(output_path, index=False)
            logging.info('Data saved to %s', output_path)
            logging.info('Number of unique usernames reported: %d', len(self.user_codes))
        except Exception as e:
            logging.error('Error saving data to CSV: %s', e)

def main():
    """
    Main function to set up configuration, logging, and run the log processing.
    """
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Configure logging
    logging.basicConfig(
        filename=config['Logging']['log_filename'],
        level=getattr(logging, config['Logging']['log_level'].upper(), logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )

    # Read configuration settings
    log_directories = config['Paths']['log_directories'].split(',')
    file_pattern = config['Settings']['file_pattern']
    csv_path = config['Paths']['output_csv']

    # Initialize and run log processor
    log_processor = LogProcessor(log_directories, file_pattern)
    log_processor.process_log_files()
    log_processor.save_to_csv(csv_path)

    # Ensure output file is written and accessible
    if os.path.exists(csv_path):
        logging.info('CSV file created successfully.')
    else:
        logging.error('Failed to create CSV file.')

if __name__ == '__main__':
    main()
