import os
import re
import pandas as pd

class LogProcessor:
    def __init__(self, directories):
        self.directories = directories
        self.user_code_pattern = re.compile(r"userCode=(\w+)")
        self.user_id_pattern = re.compile(r'"userId":"(\w+)"')
        self.user_codes = set()

    def process_log_files(self):
        for directory in self.directories:
            for filename in os.listdir(directory):
                if filename.endswith(".log"):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'r', errors='ignore') as file:
                        for line in file:
                            match_code = self.user_code_pattern.search(line)
                            match_id = self.user_id_pattern.search(line)
                            if match_code:
                                self.user_codes.add(match_code.group(1))
                            if match_id:
                                self.user_codes.add(match_id.group(1))

    def save_to_csv(self, output_path):
        df = pd.DataFrame(list(self.user_codes), columns=["userIdentifier"])
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        print(f"Number of unique usernames reported: {len(self.user_codes)}")

# Example paths to the directories containing log files
log_directories = [
    r"path_to_your_logs",
    r"path_to_your_logs",
    r"path_to_your_logs"
]

# Output CSV file path
csv_path = "extracted_user_codes.csv"

# Create an instance of LogProcessor and process the log files
log_processor = LogProcessor(log_directories)
log_processor.process_log_files()
log_processor.save_to_csv(csv_path)
