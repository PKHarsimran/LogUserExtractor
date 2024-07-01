# 🚀 Log User Extractor

A powerful and efficient Python script designed to process log files, extract unique user identifiers (`userCode` and `userId`), and save them into a CSV file. Ideal for environments with multiple directories containing extensive log files.

## ✨ Features

- **📂 Directory Scanning:** Scans specified directories for log files.
- **🔍 Identifier Extraction:** Extracts user identifiers (`userCode` and `userId`) from log files.
- **💾 CSV Output:** Saves unique user identifiers to a CSV file.
- **⚡ Parallel Processing:** Handles multiple log files simultaneously, significantly reducing processing time.
- **🔧 Robust Logging:** Enhanced error handling and logging for improved monitoring and debugging.
- **⚙️ Configurable Parameters:** Easily specify file patterns, output file names, and log levels via a configuration file.

## 🛠 Requirements

- **🐍 Python 3.x**
- **🐼 pandas**

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

1. **Configure the script:**

    Edit the `config.ini` file to specify your directories, file pattern, output file name, and log level:

    ```ini
    [Paths]
    log_directories = test
    output_csv = extracted_user_codes.csv

    [Settings]
    file_pattern = .*\.log$

    [Logging]
    log_filename = log_user_extractor.log
    log_level = INFO
    ```

2. **Run the script:**

    ```sh
    python log_user_extractor.py
    ```

3. **Check the output:**

    The script will create a CSV file named `extracted_user_codes.csv` containing the unique user identifiers.

## 📊 Flowchart

![958ZJGQMU7](https://github.com/PKHarsimran/LogUserExtractor/assets/22066581/22fbbab6-9d6c-4600-8c81-6aca8240b93b)


## 📊 Workflow

1. **Start**
2. **Load Configuration from `config.ini`**
3. **Initialize LogProcessor with directories and file pattern**
   - Input: List of directories containing log files and the file pattern to match.
4. **Process log files**
   - For each directory:
     - List files in the directory.
     - For each file:
       - Check if the file matches the pattern.
       - If true, process the file.
5. **Process the file**
   - Read the file line by line.
   - For each line:
     - Extract `userCode`.
     - Extract `userId`.
     - Add identifiers to a set to ensure uniqueness.
6. **Save identifiers to CSV**
   - Convert the set of identifiers to a DataFrame.
   - Save the DataFrame to a CSV file.
7. **End**

## 🚀 Recent and Planned Improvements

We're excited to share the latest updates and upcoming enhancements for the Log User Extractor script. These changes are designed to make the script smarter, faster, and more user-friendly!

### 🎉 Recently Implemented

#### ⚡ Parallel Processing
- **Status:** Implemented
- **Details:** We've introduced parallel processing to handle multiple log files simultaneously. This enhancement significantly reduces the time required to process large datasets, making the script more efficient and scalable.

#### 🔧 Enhanced Error Handling and Logging
- **Status:** Implemented
- **Details:** We've added robust error handling and logging mechanisms to track processing status and any issues that arise. This improvement enhances monitoring, debugging, and the overall reliability of the script.

#### ⚙️ Configurable Parameters
- **Status:** Implemented
- **Details:** Users can now specify options such as file patterns, output file names, and log levels through a configuration file. This provides greater flexibility and customization.

### 📈 Progress Tracking

We believe in transparency and continuous improvement. Here's a snapshot of our progress:

- **Parallel Processing:** ✅ Completed
- **Enhanced Error Handling and Logging:** ✅ Completed
- **Configurable Parameters:** ✅ Completed

Stay tuned for more updates as we continue to enhance the Log User Extractor. Your feedback and contributions are always welcome!

## 🤝 Contributing

We welcome contributions to enhance Log User Extractor. To contribute:

1. 🍴 Fork the repository.
2. 🌿 Create a new branch.
3. 💾 Make your changes and commit them.
4. 🚀 Push to the branch.
5. 🔄 Create a new Pull Request.

We appreciate your help in making this project better for everyone!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📝 Acknowledgments

Special thanks to all the contributors who have helped in improving this project. Your efforts are highly valued!
