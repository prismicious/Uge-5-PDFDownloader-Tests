# PDF Downloader Test Suite

[![Test on Deploy to Main](https://github.com/prismicious/Uge-5-PDFDownloader-Tests/actions/workflows/test-on-deploy.yml/badge.svg)](https://github.com/prismicious/Uge-5-PDFDownloader-Tests/actions/workflows/test-on-deploy.yml)

<!-- COVERAGE_BADGE -->

This project is focused on adding a comprehensive test suite for the PDF Downloader application. The goal is to ensure the reliability, correctness, and robustness of the PDF Downloader by implementing various automated tests.

## Features

- Unit tests for individual components of the PDF Downloader.
- Integration tests to verify the interaction between components.
- End-to-end tests to simulate real-world usage scenarios.

## Test Details

### Unit Tests
Unit tests are written to validate the behavior of individual functions:
- **`is_valid_pdf`**: Ensures that the function correctly identifies valid and invalid PDF files.
- **`download_pdf`**: Tests the ability to download PDFs, handle errors, and validate the downloaded files.

### Integration Tests
Integration tests verify the interaction between multiple components:
- **`download_task`**: Tests the handling of primary and alternative URLs, as well as the integration with the DataFrame and file system.

### Edge Cases
The test suite includes scenarios for:
- Missing or invalid URLs.
- Corrupt or empty PDF files.
- Network errors such as timeouts and HTTP errors.

## Test Report

The test report provides a detailed summary of the testing process and results. It includes information about the test cases, scenarios, and their outcomes. The report ensures transparency and helps identify areas for improvement.

### Key Highlights:
- **Coverage**: The report covers unit tests, integration tests, and edge cases.
- **Results**: All test cases have been executed successfully, ensuring the reliability of the application.
- **Improvements**: The report identifies necessary code changes and enhancements made during testing.

For more details, refer to the [Test Report](test_report.md).

## Getting Started

1. Clone the repository.
2. Install dependencies using your preferred package manager:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the test suite using the following command:
   ```bash
   python -m unittest discover -s tests
   ```


