import configparser  # Module for configuration file parsing
import os  # Module to interact with the operating system
import re  # Module for regular expressions
import pandas as pd  # Module for data manipulation and analysis
from concurrent.futures import ThreadPoolExecutor  # Module for parallel processing
import logging  # Module for logging
import argparse  # Module for command-line argument parsing

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
        logging.info('Starting to process log files...')
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._process_single_file, os.path.join(directory, filename))
                for directory in self.directories
                if os.path.exists(directory)
                for filename in os.listdir(directory)
                if self.file_pattern.match(filename)
            ]
            logging.info('Submitted %d files for processing', len(futures))

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
            logging.info('Processing file: %s', filepath)
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
            logging.info('Saving data to CSV: %s', output_path)
            df = pd.DataFrame(list(self.user_codes), columns=["userIdentifier"])
            df.to_csv(output_path, index=False)
            logging.info('Data saved to %s', output_path)
            logging.info('Number of unique usernames reported: %d', len(self.user_codes))
        except Exception as e:
            logging.error('Error saving data to CSV: %s', e)

def setup_logging(log_file_path, log_level):
    """
    Configure logging settings.
    :param log_file_path: Path to the log file.
    :param log_level: Logging level.
    """
    logging.basicConfig(
        filename=log_file_path,
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )
    logging.info('Logging set up with log file: %s and log level: %s', log_file_path, log_level)

def load_config(config_file):
    """
    Load configuration settings from a file.
    :param config_file: Path to the configuration file.
    :return: ConfigParser object with loaded settings.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def main():
    """
    Main function to set up configuration, logging, and run the log processing.
    """
    parser = argparse.ArgumentParser(description="Log User Extractor")
    parser.add_argument('--config', help='Path to the configuration file', default='config.ini')
    parser.add_argument('--log_directories', help='Comma-separated list of directories to scan for log files')
    parser.add_argument('--file_pattern', help='Pattern to match log files')
    parser.add_argument('--output_csv', help='Path to the output CSV file')
    parser.add_argument('--log_file', help='Path to the log file')
    parser.add_argument('--log_level', help='Logging level')

    args = parser.parse_args()

    if args.log_directories and args.file_pattern and args.output_csv and args.log_file and args.log_level:
        log_directories = args.log_directories.split(',')
        file_pattern = args.file_pattern
        output_csv_path = args.output_csv
        log_file_path = args.log_file
        log_level = args.log_level
        print("Configuration set from command-line arguments.")
    else:
        config = load_config(args.config)
        log_directories = config['Paths']['log_directories'].split(',')
        file_pattern = config['Settings']['file_pattern']
        output_csv_path = config['Paths']['output_csv']
        log_file_path = config['Logging']['log_filename']
        log_level = config['Logging']['log_level']
        print(f"Configuration loaded from {args.config}.")

    setup_logging(log_file_path, log_level)

    logging.info('Log directories: %s', log_directories)
    logging.info('File pattern: %s', file_pattern)
    logging.info('CSV output path: %s', output_csv_path)
    logging.info('Log file path: %s', log_file_path)

    log_processor = LogProcessor(log_directories, file_pattern)
    log_processor.process_log_files()
    log_processor.save_to_csv(output_csv_path)

    if os.path.exists(output_csv_path):
        print(f"CSV file created successfully at {output_csv_path}.")
        logging.info('CSV file created successfully.')
    else:
        print(f"Failed to create CSV file at {output_csv_path}.")
        logging.error('Failed to create CSV file.')

if __name__ == '__main__':
    main()
