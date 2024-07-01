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
    git clone https://github.com/PKHarsimran/LogUserExtractor.git
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

![8Dj3Iv3LAH](https://github.com/PKHarsimran/LogUserExtractor/assets/22066581/d98cbb19-e763-4479-a2d5-ad29011d3aca)

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

## 🚀 Recent and Planned Improvements

We're excited to share the latest updates and upcoming enhancements for the Log User Extractor script. These changes are designed to make the script smarter, faster, and more user-friendly!

### 🎉 Recently Implemented

1. **⚡ Parallel Processing**
   - **Status:** Implemented
   - **Details:** We've introduced parallel processing to handle multiple log files simultaneously. This enhancement significantly reduces the time required to process large datasets, making the script more efficient and scalable.

2. **🔧 Enhanced Error Handling and Logging**
   - **Status:** Implemented
   - **Details:** We're working on adding robust error handling and logging mechanisms to track processing status and any issues that arise. This will improve monitoring, debugging, and overall reliability of the script.

3. **⚙️ Configurable Parameters**
   - **Status:** Implemented
   - **Details:** Future updates will introduce configurable parameters, allowing users to specify options such as file patterns, output file names, and log levels through a configuration file or command-line arguments. This will provide greater flexibility and customization for users.

### 📈 Progress Tracking

We believe in transparency and continuous improvement. Here's a snapshot of our progress:

- **Parallel Processing:** ✅ Completed
- **Enhanced Error Handling and Logging:** ✅ Completed
- **Configurable Parameters:** ✅ Completed

Stay tuned for more updates as we continue to enhance the Log User Extractor. Your feedback and contributions are always welcome!


## 🤝 Contributing

1. 🍴 Fork the repository.
2. 🌿 Create a new branch.
3. 💾 Make your changes and commit them.
4. 🚀 Push to the branch.
5. 🔄 Create a new Pull Request.
