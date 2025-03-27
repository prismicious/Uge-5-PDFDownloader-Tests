# -*- coding: utf-8 -*-
"""
PDF Download and Validation Script

This script downloads PDFs from a list of URLs, ensures their validity, and updates a metadata file with the download status.
"""

import pandas as pd
import PyPDF2
from pathlib import Path
import shutil
import urllib.request
import urllib.error
import socket
import glob
import ssl
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ignore SSL errors (temporary workaround)
ssl._create_default_https_context = ssl._create_unverified_context

# -------------------- PATH CONFIGURATION --------------------
# Define project root path (assumes script is inside a subdirectory of the project)
project_root = Path(__file__).resolve().parent.parent
dwn_path = project_root / "output" / "downloads"

# Define file paths
list_pth = project_root / "data" / \
    "GRI_2017_2020 (1).xlsx"  # Excel file containing URLs
metadata_pth = project_root / "data" / "Metadata2017_2020.xlsx"  # Metadata file

# -------------------- PDF VALIDATION FUNCTION --------------------

def is_valid_pdf(file_path):
    """Checks if a PDF file is valid by attempting to read its pages."""
    try:
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return len(pdf_reader.pages) > 0  # Valid if it has pages
    except (PyPDF2.errors.PdfReadError, Exception):
        return False  # Invalid PDF file

# -------------------- DOWNLOAD FUNCTION --------------------


def download_pdf(url, save_path, retries=3, timeout=10):
    """
    Attempts to download a PDF file with multiple retries in case of failures.
    - url: PDF download link
    - save_path: Local path to save the PDF
    - retries: Number of retry attempts
    - timeout: Time limit per download attempt
    """
    if not url:  # Skip if the URL is missing
        return "No URL provided"

    headers = {'User-Agent': 'Mozilla/5.0'}
    request = urllib.request.Request(url, headers=headers)

    e = None  # Initialize exception variable

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response, open(save_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print(f"Download successful: {save_path}")
            return "Yes, valid PDF" if is_valid_pdf(save_path) else "Yes, but file error (corrupt PDF)"
        except (urllib.error.URLError, socket.timeout, Exception) as err:
            e = err  # Store the error for reporting
            print(
                f"Download error (Attempt {attempt + 1}/{retries}): {url} - {e}")
            time.sleep(2)  # Wait before retrying

    return f"No. Error: {e}" if e else "Unknown error"

# -------------------- DOWNLOAD HANDLER FUNCTION --------------------


def download_task(j, df, dwn_pth=dwn_path):
    # Ensure the output directory exists
    dwn_pth.mkdir(parents=True, exist_ok=True)
    """
    Attempts to download a PDF for a given row index (BRnum).
    - Tries the primary URL first
    - If it fails, attempts an alternative URL if available
    - Returns download status
    """
    url1 = str(df.at[j, 'Pdf_URL']) if pd.notna(df.at[j, 'Pdf_URL']) else None
    url2 = str(df.at[j, 'Report Html Address']) if 'Report Html Address' in df.columns and pd.notna(
        df.at[j, 'Report Html Address']) else None
    savefile = dwn_pth / f"{j}.pdf"

    print(
        f"Attempting to download: {url1 if url1 else 'No URL'} -> {savefile}")

    if not url1 and not url2:
        return j, "No, because no URL is available"

    # Handle local file paths if provided as URLs
    if url1:
        parsed_url = urlparse(url1)
        if parsed_url.scheme == 'file':  # Check if the URL is a local file path
            local_path = parsed_url.path.lstrip('/')
            if Path(local_path).exists():  # Verify the local file exists
                shutil.copy(local_path, savefile)
                print(f"Copied local file: {savefile}")
                return j, "Yes, from local file"
            else:
                print(f"Local file not found: {local_path}")
                return j, "No, because local file is missing"

    # Try downloading from the primary URL
    # ADD ERROR TO THE STATUS SO THAT THE TEST CAN PASS
    status = download_pdf(url1, savefile) if url1 else "Error: No URL provided"

    # If the first download fails, attempt the second URL if available
    if "Error" in status and url2:
        print(f"Trying alternative URL: {url2}")
        status_alt = download_pdf(url2, savefile)

        if "valid PDF" in status_alt:
            return j, "Yes, by alternative URL"
        elif "Yes, but file error (corrupt PDF)" in status_alt:
            return j, "Yes, but second URL file error (corrupt PDF)"
        elif "HTTP Error" in status_alt:
            return j, f"No, because of second URL error: {status_alt.split(':', 1)[1].strip()}"
        else:
            return j, "No, because second URL failed"

    print(f"Saving file to: {savefile}")
    return j, status  # Return ID and status

# -------------------- PARALLEL DOWNLOAD EXECUTION --------------------


def execute_parallel_downloads():
    """
    Executes parallel downloads using ThreadPoolExecutor.
    Updates the DataFrame with the download status.
    """
    # Define the column used as the unique ID in the Excel file
    id = "BRnum"

    df = return_df(id)
    num_threads = 5  # Adjust based on system capabilities

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Pass df explicitly
        future_to_id = {executor.submit(
            download_task, j, df): j for j in df.index}
        for future, j in future_to_id.items():
            j, status = future.result()
            df.at[j, 'status'] = status  # Update DataFrame

    # Update metadata file with download statuses
    df_metadata = pd.read_excel(metadata_pth, sheet_name=0, dtype=str)

    # Ensure required columns exist in the metadata file
    if id not in df_metadata.columns or "pdf_downloaded" not in df_metadata.columns:
        raise ValueError(
            "Columns ID and 'pdf_downloaded' are missing in Metadata2017_2020.xlsx.")

    df_metadata[id] = df.index.astype(str)
    df_metadata["pdf_downloaded"] = df["status"].values

    # Save the updated metadata file
    df_metadata.to_excel(metadata_pth, sheet_name="Sheet1", index=False)

    print(f"Metadata updated successfully: {metadata_pth}")


def return_df(id, dwn_pth=dwn_path):
    """
    Returns the DataFrame containing the URLs to download.
    Excludes already downloaded files and limits the number of downloads.
    """
        
    # Get already downloaded files (to avoid unnecessary re-downloads)
    existing_files = {Path(f).stem for f in glob.glob(f"{dwn_pth}/*.pdf")}

    # -------------------- LOAD INPUT DATA --------------------
    # Load the Excel file containing PDF URLs
    df = pd.read_excel(list_pth, sheet_name=0, index_col=id)

    # Ensure the URL column is correctly formatted (replace non-string values with None)
    df["Report Html Address"] = df["Report Html Address"].apply(
        lambda x: x if isinstance(x, str) else None)

    # Exclude already downloaded files by checking their unique ID
    df = df[~df.index.astype(str).isin(existing_files)]

    # Limit the number of downloads (for controlled testing/prototyping)
    df = df.head(20)

    return df


# Necessary for not triggering when running tests
if __name__ == "__main__":
    execute_parallel_downloads()
