import unittest
from unittest.mock import patch
import pandas as pd
from scripts.download_files import download_task


class TestDownloadTask(unittest.TestCase):
    def setUp(self):
        # Patch shared dependencies
        self.patcher_download_pdf = patch("scripts.download_files.download_pdf")
        self.patcher_copy = patch("scripts.download_files.shutil.copy")

        # Start patches
        self.mock_download_pdf = self.patcher_download_pdf.start()
        self.mock_copy = self.patcher_copy.start()

    def tearDown(self):
        # Stop all patches
        self.patcher_download_pdf.stop()
        self.patcher_copy.stop()

    def test_valid_primary_url(self):
        # Arrange
        df = pd.DataFrame({
            "Pdf_URL": ["http://example.com"],
            "Report Html Address": [None]
        }, index=["12345"])
        self.mock_download_pdf.return_value = "Yes, valid PDF"

        # Act
        result = download_task("12345", df=df)

        # Assert
        self.assertEqual(result, ("12345", "Yes, valid PDF"))
        self.mock_download_pdf.assert_called_once_with("http://example.com", unittest.mock.ANY)
    
    def test_valid_alternative_url(self):
        # Arrange
        df = pd.DataFrame({
            "Pdf_URL": [None],
            "Report Html Address": ["http://alternative.com"]
        }, index=["12345"])
        self.mock_download_pdf.return_value = "Yes, valid PDF"
        # Act
        result = download_task("12345", df=df)

        # Assert
        self.assertEqual(result, ("12345", "Yes, by alternative URL"))
        self.assertEqual(self.mock_download_pdf.call_count, 1)
        self.mock_download_pdf.assert_any_call("http://alternative.com", unittest.mock.ANY)

    def test_missing_urls(self):
        # Arrange
        df = pd.DataFrame({
            "Pdf_URL": [None],
            "Report Html Address": [None]
        }, index=["12345"])

        # Act
        result = download_task("12345", df=df)

        # Assert
        self.assertEqual(result, ("12345", "No, because no URL is available"))
