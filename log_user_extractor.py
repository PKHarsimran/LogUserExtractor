import os  # Module to interact with the operating system
import re  # Module for regular expressions
import pandas as pd  # Module for data manipulation and analysis
from concurrent.futures import ThreadPoolExecutor  # Module for parallel processing

class LogProcessor:
    def __init__(self, directories):
        """
        Initialize the LogProcessor with directories to scan for log files.
        :param directories: List of directories containing log files.
        """
        self.directories = directories  # Directories to search for log files
        # Regular expression to find userCode patterns in the logs
        self.user_code_pattern = re.compile(r"userCode=(\w+)")
        # Regular expression to find userId patterns in the logs
        self.user_id_pattern = re.compile(r'"userId":"(\w+)"')
        # Set to store unique user identifiers (userCode or userId)
        self.user_codes = set()

    def process_log_files(self):
        """
        Process each log file in the specified directories to extract user identifiers.
        """
        with ThreadPoolExecutor() as executor:
            futures = []
            for directory in self.directories:
                for filename in os.listdir(directory):  # List files in the directory
                    if filename.endswith(".log"):  # Check if the file is a log file
                        filepath = os.path.join(directory, filename)  # Full path to the log file
                        futures.append(executor.submit(self._process_single_file, filepath))
            
            # Ensure all threads have completed
            for future in futures:
                future.result()

    def _process_single_file(self, filepath):
        """
        Process a single log file to extract user identifiers.
        :param filepath: Path to the log file.
        """
        with open(filepath, 'r', errors='ignore') as file:
            for line in file:  # Read each line in the log file
                self._extract_user_identifiers(line)

    def _extract_user_identifiers(self, line):
        """
        Extract user identifiers from a single line of log.
        :param line: A single line from the log file.
        """
        # Search for userCode in the line
        match_code = self.user_code_pattern.search(line)
        # Search for userId in the line
        match_id = self.user_id_pattern.search(line)
        if match_code:
            # Add the found userCode to the set
            self.user_codes.add(match_code.group(1))
        if match_id:
            # Add the found userId to the set
            self.user_codes.add(match_id.group(1))

    def save_to_csv(self, output_path):
        """
        Save the extracted user identifiers to a CSV file.
        :param output_path: Path to save the output CSV file.
        """
        # Create a DataFrame from the set of user identifiers
        df = pd.DataFrame(list(self.user_codes), columns=["userIdentifier"])
        # Save the DataFrame to a CSV file
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        print(f"Number of unique usernames reported: {len(self.user_codes)}")

# Example paths to the directories containing log files
log_directories = [
    r"test",  # Replace with your actual directory path
]

# Output CSV file path
csv_path = "extracted_user_codes.csv"

# Create an instance of LogProcessor and process the log files
log_processor = LogProcessor(log_directories)
log_processor.process_log_files()
log_processor.save_to_csv(csv_path)
