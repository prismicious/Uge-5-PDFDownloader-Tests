from pathlib import Path
import time
import unittest
import os
from scripts.download_files import download_task, return_df

project_root = Path(__file__).resolve().parent.parent

test_output_dir = project_root / "tests" / "test_output"


class TestDownloadTaskIntegration(unittest.TestCase):

    def setUp(self):
        """Set up the test environment and initialize the dataframe."""
        self.id = "BRnum"
        self.df = return_df(self.id)
        os.makedirs(test_output_dir, exist_ok=True)
        self.output_path = test_output_dir
        self.pdf_path = test_output_dir / "BR50041.pdf"

    def tearDown(self):
        """Clean up any residual files or directories after each test."""
        if os.path.exists(test_output_dir):
            for root, dirs, files in os.walk(test_output_dir, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(test_output_dir)

    def test_download_valid_url(self):
        """Test downloading a file from a valid URL."""

        # Act
        download_task(self.df.index[0], self.df, self.output_path)

        # Assert
        self.assertTrue(self.pdf_path.exists())

    def test_download_invalid_url(self):
        """Test downloading from an invalid URL."""

        # Ensure the output directory exists
        os.makedirs(test_output_dir, exist_ok=True)
        invalid_output_path = test_output_dir / "invalid.pdf"

        # Perform the download and expect an exception
        with self.assertRaises(Exception):
            download_task("invalid_url", invalid_output_path)

        # Assert the file was not created
        self.assertFalse(invalid_output_path.exists())

    def test_download_to_nonexistent_directory(self):
        """Test downloading to a nonexistent directory."""
        url = "https://example.com/sample.pdf"  # Replace with a valid test URL

        # Ensure the directory does not exist
        nonexistent_dir = project_root / "nonexistent_dir"
        if nonexistent_dir.exists():
            nonexistent_dir.rmdir()

        # Perform the download
        output_path = nonexistent_dir / "sample.pdf"
        download_task(url, output_path)

        # Assert the file was downloaded
        self.assertTrue(output_path.exists())

