# Test Report

## Overview
This report summarizes the testing process and results for the **PDF Downloader** project. The tests were conducted to ensure the functionality, reliability, and robustness of the application.

---

## Discrepancies
During the testing process, it was noted that the `execute_parallel_downloads` method was not explicitly tested. This method encapsulates the logic for parallel execution using `ThreadPoolExecutor`. While its functionality is indirectly validated through the integration tests, direct unit tests for this method would ensure better coverage and help identify potential concurrency issues or edge cases.

---

## Test Cases

### 1. `is_valid_pdf` Function
**Description**: Tests the validity of PDF files by attempting to read their pages.

#### Test Scenarios:
- ✅ Valid PDF file.
- ✅ Invalid PDF file.
- ✅ Empty file.
- ✅ Non-PDF file.
- ✅ Non-existent file.
- ✅ Corrupt PDF file.

**Result**: All scenarios passed successfully.

---

### 2. `download_pdf` Function
**Description**: Tests the ability to download PDF files from URLs with retries and error handling.

#### Test Scenarios:
- ✅ No URL provided.
- ✅ Successful download of a valid PDF.
- ✅ Download of a corrupt PDF.
- ✅ Unsuccessful download due to HTTP error.
- ✅ Download timeout.
- ✅ Invalid URL format.

**Result**: All scenarios passed successfully.

---

### 3. `download_task` Function
**Description**: Tests the handling of primary and alternative URLs for downloading PDFs.

#### Test Scenarios:
- ✅ Valid primary URL.
- ✅ Valid alternative URL.
- ✅ Missing URLs.

**Result**: All scenarios passed successfully.

---

### 4. Integration Tests for `download_task`
**Description**: Tests the integration of `download_task` with the DataFrame and file system.

#### Test Scenarios:
- ✅ Downloading a file from a valid URL.
- ✅ Handling an invalid URL.

**Result**: All scenarios passed successfully.

---

## Summary
All test cases were executed successfully, and the application met the expected functionality and robustness criteria. The tests covered edge cases, error handling, and integration scenarios.

---

## Necessary Code Changes & Improvements
During the test creation phase, a few issues were discovered in the code:

1. **Encapsulation of Execution Logic**:
   - The code related to the `ThreadPoolExecutor` was encapsulated in a function called `execute_parallel_downloads`.
   - Added the following lines to ensure the program does not run during tests:
     ```python
     if __name__ == "__main__":
         execute_parallel_downloads()
     ```

2. **Fix for `download_task` Return Values**:
   - Previously, `download_task` always returned "Yes" for both valid and invalid PDFs.
   - Updated the return to `"No, Invalid PDF"` if the `is_valid_pdf()` function returns `False`.

3. **Introduction of `return_df` Function**:
   - Added the `return_df` function to easily obtain the DataFrame.
   - Updated `download_task` to include new parameters: `df` and `dwn_path`.
     - `df`: Allows passing the DataFrame explicitly.
     - `dwn_path`: Enables changing the download folder for tests, necessary for test cleanup (`tearDown`).

---

## Conclusion
The **PDF Downloader** project is functioning as intended, with all tests passing successfully. The application is ready for deployment with confidence in its reliability.
