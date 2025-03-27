from pathlib import Path
import unittest
import os
from scripts.download_files import download_task, return_df

# Ensure test_output_dir exists before tests run
project_root = Path(__file__).resolve().parent.parent
test_output_dir = project_root / "tests" / "test_output"
test_output_dir.mkdir(parents=True, exist_ok=True)
id = "BRnum"

class TestDownloadTaskIntegration(unittest.TestCase):
    def setUp(self):
        """Set up the test environment and initialize the dataframe."""
        self.df = return_df(id)

        # Ensure dataframe is valid
        self.assertIsNotNone(self.df, "return_df() returned None!")
        self.assertGreater(len(self.df), 0, "Dataframe is empty!")

        self.output_path = test_output_dir
        self.pdf_path = test_output_dir / "BR50041.pdf"

    def test_download_valid_url(self):
        """Test downloading a file from a valid URL."""
        
        # Arrange
        valid_df = self.df.copy(deep=True)  # Prevent unexpected modifications
        valid_df.at[self.df.index[0], "Pdf_URL"] = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        # Act
        try:
            result = download_task(self.df.index[0], valid_df, self.output_path)
        except Exception as e:
            self.fail(f"download_task() raised an exception: {e}")

        # Assert
        self.assertEqual(result[1], "Yes, valid PDF")  # Check the status

    def test_download_invalid_url(self):
        """Test downloading from an invalid URL."""

        # Arrange
        invalid_df = self.df.copy(deep=True)
        invalid_df.at[self.df.index[0], "Pdf_URL"] = "http://invalid-url.com"

        # Act
        try:
            result = download_task(self.df.index[0], invalid_df, self.output_path)
        except Exception as e:
            self.fail(f"download_task() raised an exception: {e}")

        # Assert
        self.assertEqual(result[1], "No, Invalid PDF")
