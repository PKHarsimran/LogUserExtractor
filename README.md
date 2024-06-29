# 🚀 Log User Extractor

This Python script processes log files to extract user identifiers (userCode and userId) and saves the unique identifiers to a CSV file. It is designed to work with multiple directories containing log files.

## ✨ Features

- 📂 Scans specified directories for log files.
- 🔍 Extracts user identifiers (userCode and userId) from log files.
- 💾 Saves unique user identifiers to a CSV file.

## 🛠 Requirements

- 🐍 Python 3.x
- 🐼 pandas

## 📥 Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/PKHarsimran/LogUserExtractor
    ```

2. **Navigate to the project directory:**

    ```sh
    cd LogUserExtractor
    ```

3. **Install the required Python packages:**

    ```sh
    pip install pandas
    ```

## 🚀 Usage

1. **Modify the script to include your directories:**

    Replace the `log_directories` list with the paths to your log directories:

    ```python
    log_directories = [
        r"path_to_your_logs\log01.log",  # Replace with your actual directory path
        r"path_to_your_logs\log02.log",  # Replace with your actual directory path
        r"path_to_your_logs\log03.log"   # Replace with your actual directory path
    ]
    ```

2. **Run the script:**

    ```sh
    python log_user_extractor.py
    ```

3. **Check the output:**

    The script will create a CSV file named `extracted_user_codes.csv` with the unique user identifiers.


## 📊 Flowchart
![output](https://github.com/PKHarsimran/LogUserExtractor/assets/22066581/af707e16-48cd-4467-b954-cb07589a682c)

1. **Start**
2. **Initialize LogProcessor with directories**
   - Input: List of directories containing log files.
3. **Process log files**
   - For each directory:
     - List files in the directory.
     - For each file:
       - Check if the file ends with `.log`.
       - If true, process the file.
4. **Process the file**
   - Read the file line by line.
   - For each line:
     - Extract `userCode`.
     - Extract `userId`.
     - Add identifiers to a set to ensure uniqueness.
5. **Save identifiers to CSV**
   - Convert the set of identifiers to a DataFrame.
   - Save the DataFrame to a CSV file.
6. **End**


## 🤝 Contributing

1. 🍴 Fork the repository.
2. 🌿 Create a new branch.
3. 💾 Make your changes and commit them.
4. 🚀 Push to the branch.
5. 🔄 Create a new Pull Request.
