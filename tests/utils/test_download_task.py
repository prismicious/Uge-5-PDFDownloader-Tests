import unittest
from unittest.mock import patch, MagicMock
from scripts.download_files import download_task

class TestDownloadTask(unittest.TestCase):
    def setUp(self):
        # Patch shared dependencies
        self.patcher_df = patch("scripts.download_files.df")
        self.patcher_download_pdf = patch("scripts.download_files.download_pdf")
        self.patcher_copy = patch("scripts.download_files.shutil.copy")

        # Start patches
        self.mock_df = self.patcher_df.start()
        self.mock_download_pdf = self.patcher_download_pdf.start()
        self.mock_copy = self.patcher_copy.start()

    def tearDown(self):
        # Stop all patches
        self.patcher_df.stop()
        self.patcher_download_pdf.stop()
        self.patcher_copy.stop()

    def test_valid_primary_url(self):
        # Arrange
        self.mock_df.at = MagicMock(side_effect=lambda j, col: "http://example.com" if col == "Pdf_URL" else None)
        self.mock_download_pdf.return_value = "Yes, valid PDF"

        # Act
        result = download_task("12345")

        # Assert
        self.assertEqual(result, ("12345", "Yes, valid PDF"))
        self.mock_download_pdf.assert_called_once_with("http://example.com", unittest.mock.ANY)

    def test_valid_alternative_url(self):
        # Arrange
        self.mock_df.at = MagicMock(side_effect=lambda j, col: None if col == "Pdf_URL" else "http://alternative.com")
        self.mock_download_pdf.side_effect = ["No. Error: 404", "Yes, valid PDF"]

        # Act
        result = download_task("12345")

        # Assert
        self.assertEqual(result, ("12345", "Yes, by alternative URL"))
        self.assertEqual(self.mock_download_pdf.call_count, 2)
        self.mock_download_pdf.assert_any_call("http://alternative.com", unittest.mock.ANY)

    def test_missing_urls(self):
        # Arrange
        self.mock_df.at = MagicMock(return_value=None)
        self.mock_download_pdf.return_value = "No, because no URL is available"  # Explicitly set return value

        # Act
        result = download_task("12345")

        # Assert
        self.assertEqual(result, ("12345", "No, because no URL is available"))