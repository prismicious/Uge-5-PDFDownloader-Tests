# PDF Downloader

This script automates the process of downloading PDF files from a list of URLs, checking the validity of the downloaded PDFs, and updating a metadata file with the download status.

## Description

This project provides a Python script to download PDFs from a list of URLs in an Excel file. The script checks each PDF's validity by attempting to read its pages and marks the download status accordingly. If any errors are encountered, the script retries the download two times before marking it as failed. The script also updates a metadata file with the download status for each entry.

## Getting Started

### Dependencies

* pandas
* PyPDF2

### Installing

* Download or clone the repository containing the script.

### Executing program

* Navigate to the scripts folder where the download_files.py script is located.
* Run the script with the following command:
    ```
    python download_files.py
    ```

This will start the process of downloading the PDFs. The status of each download will be shown in the terminal, and the metadata file will be updated once all downloads are complete.

### Customization

You can adjust the number of download attempts and tweak other parameters directly in the script to suit your needs. By default, the script processes 20 entries for testing, but you can modify this number as required.

## Possible Improvements:
* The code could be divided into classes instead:
    * PDFDownloader
    * MetadataUpdater
    * DownloadManager

* The classes could be placed in separate Python files within a utils folder, for example:
    * downloader.py
    * validator.py
    * metadata.py
    * config.py

* Using requests instead of urllib could improve usability and error handling.

* Implementing logging instead of print() would allow logs to be saved to a file, making debugging easier.

## Author

Dennis Russell
[@DennisRussell0](https://github.com/DennisRussell0)

## Version History

* 0.1
    * Initial Release
