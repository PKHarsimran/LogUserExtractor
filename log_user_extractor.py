import os  # Module to interact with the operating system
import re  # Module for regular expressions
import pandas as pd  # Module for data manipulation and analysis
from concurrent.futures import ThreadPoolExecutor  # Module for parallel processing
import logging  # Module for logging
import configparser  # Module for configuration file parsing

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')  # Configuration file name

# Configure logging
logging.basicConfig(
    filename=config['Logging']['log_filename'],  # Log file name from configuration
    level=getattr(logging, config['Logging']['log_level'].upper(), logging.INFO),  # Log level from configuration
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    filemode='w'  # Overwrite log file each time the script runs
)

class LogProcessor:
    def __init__(self, directories, file_pattern):
        """
        Initialize the LogProcessor with directories to scan for log files and file pattern to match.
        :param directories: List of directories containing log files.
        :param file_pattern: Pattern to match log files.
        """
        self.directories = directories  # Directories to search for log files
        self.file_pattern = file_pattern  # File pattern to match
        # Regular expression to find userCode patterns in the logs
        self.user_code_pattern = re.compile(r"userCode=(\w+)")
        # Regular expression to find userId patterns in the logs
        self.user_id_pattern = re.compile(r'"userId":"(\w+)"')
        # Set to store unique user identifiers (userCode or userId)
        self.user_codes = set()
        logging.info('LogProcessor initialized with directories: %s and file pattern: %s', directories, file_pattern)

    def process_log_files(self):
        """
        Process each log file in the specified directories to extract user identifiers.
        """
        with ThreadPoolExecutor() as executor:  # Use ThreadPoolExecutor for parallel processing
            futures = []  # List to keep track of submitted tasks
            for directory in self.directories:
                logging.info('Processing directory: %s', directory)  # Log the directory being processed
                for filename in os.listdir(directory):  # List files in the directory
                    if re.match(self.file_pattern, filename):  # Check if the file matches the pattern
                        filepath = os.path.join(directory, filename)  # Full path to the log file
                        logging.info('Submitting file for processing: %s', filepath)  # Log file submission
                        futures.append(executor.submit(self._process_single_file, filepath))  # Submit file for processing

            for future in futures:
                try:
                    future.result()  # Wait for each future to complete
                except Exception as e:
                    logging.error('Error processing file: %s', e)  # Log any errors that occur

    def _process_single_file(self, filepath):
        """
        Process a single log file to extract user identifiers.
        :param filepath: Path to the log file.
        """
        line_count = 0  # Initialize line count
        try:
            with open(filepath, 'r', errors='ignore') as file:  # Open the log file
                for line in file:  # Read each line in the log file
                    self._extract_user_identifiers(line)  # Extract user identifiers from the line
                    line_count += 1  # Increment line count
            logging.info('Processed file: %s with %d lines', filepath, line_count)  # Log file processing completion
        except Exception as e:
            logging.error('Error processing file %s: %s', filepath, e)  # Log any errors that occur

    def _extract_user_identifiers(self, line):
        """
        Extract user identifiers from a single line of log.
        :param line: A single line from the log file.
        """
        try:
            match_code = self.user_code_pattern.search(line)  # Search for userCode in the line
            match_id = self.user_id_pattern.search(line)  # Search for userId in the line
            if match_code:
                self.user_codes.add(match_code.group(1))  # Add the found userCode to the set
            if match_id:
                self.user_codes.add(match_id.group(1))  # Add the found userId to the set
        except Exception as e:
            logging.error('Error extracting identifiers from line: %s', e)  # Log any errors that occur

    def save_to_csv(self, output_path):
        """
        Save the extracted user identifiers to a CSV file.
        :param output_path: Path to save the output CSV file.
        """
        try:
            df = pd.DataFrame(list(self.user_codes), columns=["userIdentifier"])  # Create a DataFrame from the set of user identifiers
            df.to_csv(output_path, index=False)  # Save the DataFrame to a CSV file
            logging.info('Data saved to %s', output_path)  # Log file saving completion
            logging.info('Number of unique usernames reported: %d', len(self.user_codes))  # Log the number of unique usernames reported
        except Exception as e:
            logging.error('Error saving data to CSV: %s', e)  # Log any errors that occur

# Load parameters from the configuration file
log_directories = config['Paths']['log_directories'].split(',')  # Directories containing log files
file_pattern = config['Settings']['file_pattern']  # File pattern to match log files
csv_path = config['Paths']['output_csv']  # Output CSV file path

# Create an instance of LogProcessor and process the log files
log_processor = LogProcessor(log_directories, file_pattern)
log_processor.process_log_files()
log_processor.save_to_csv(csv_path)
