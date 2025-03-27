import os
import socket
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from scripts.download_files import download_pdf


class TestDownloadPDF(unittest.TestCase):
    def setUp(self) -> None:
        # Patch shared dependencies
        self.patcher_urlopen = patch("urllib.request.urlopen")
        self.patcher_copyfileobj = patch("shutil.copyfileobj")
        self.patcher_open = patch("builtins.open", new_callable=MagicMock)
        self.patcher_is_valid_pdf = patch(
            "scripts.download_files.is_valid_pdf")

        # Start patches
        self.mock_urlopen = self.patcher_urlopen.start()
        self.mock_copyfileobj = self.patcher_copyfileobj.start()
        self.mock_open = self.patcher_open.start()
        self.mock_is_valid_pdf = self.patcher_is_valid_pdf.start()

        # Mock default behaviors
        self.mock_is_valid_pdf.return_value = True
        self.mock_response = MagicMock()
        self.mock_response.__enter__.return_value = self.mock_response
        self.mock_urlopen.return_value = self.mock_response

    def tearDown(self) -> None:
        # Stop all patches
        self.patcher_urlopen.stop()
        self.patcher_copyfileobj.stop()
        self.patcher_open.stop()
        self.patcher_is_valid_pdf.stop()

    def test_no_url_provided(self) -> None:
        # Arrange
        url: None = None
        save_path: str = f"output/no_url.pdf"

        # Act
        result: str = download_pdf(url, save_path)

        # Assert
        self.assertEqual(result, "No URL provided")

    def test_successful_download(self) -> None:
        # Arrange
        url: str = "http://example.com"
        save_path: str = f"output/successful_download.pdf"
        self.mock_response.read.return_value = b"%PDF-1.4"  # Simulate valid PDF content

        # Act
        result: str = download_pdf(url, save_path)

        # Assert
        self.assertEqual(result, "Yes, valid PDF")
        self.mock_urlopen.assert_called_once()
        self.mock_copyfileobj.assert_called_once_with(
            self.mock_response, self.mock_open.return_value.__enter__.return_value)
        self.mock_is_valid_pdf.assert_called_once_with(save_path)

    def test_corrupt_pdf_download(self) -> None:
        # Arrange
        url: str = "http://corrupted.pdf"
        save_path: str = "output/downloads/corrupt_pdf.pdf"
        # Simulate corrupt PDF content
        self.mock_response.read.return_value = b"This is not valid PDF content"
        self.mock_is_valid_pdf.return_value = False

        # Act
        result: str = download_pdf(url, save_path)

        # Assert
        self.assertEqual(result, "No, Invalid PDF")
        self.mock_urlopen.assert_called_once()
        self.mock_copyfileobj.assert_called_once_with(
            self.mock_response, self.mock_open.return_value.__enter__.return_value)
        self.mock_is_valid_pdf.assert_called_once_with(save_path)

    def test_unsuccessful_download(self) -> None:
        # Arrange
        url: str = "http://example.com"
        save_path: str = f"output/downloads/unsuccessful_download.pdf"

        # Mock the request and response
        self.mock_urlopen.side_effect = HTTPError(
            url, 404, "Not Found", None, None)

        # Act
        result: str = download_pdf(url, save_path)

        # Assert
        self.assertIn("Error", result)
        self.assertIn("404", result)
        self.assertEqual(self.mock_urlopen.call_count, 3)

    def test_download_timeout(self) -> None:
        # Arrange
        url: str = "http://example.com"
        save_path: str = f"output/downloads/download_timeout.pdf"

        # Simulate a timeout
        self.mock_urlopen.side_effect = socket.timeout("timed out")

        # Act
        result: str = download_pdf(url, save_path)

        # Assert
        self.assertEqual(result, "No. Error: timed out")
        self.assertEqual(self.mock_urlopen.call_count, 3)

    def test_invalid_url(self) -> None:
        # Arrange
        url = "some_test_url"
        save_path = f"output/downloads/invalid_url.pdf"

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            download_pdf(url, save_path)

        # Check the exception message
        self.assertEqual(str(context.exception),
                         "unknown url type: 'some_test_url'")

        # Ensure no file is created
        self.assertFalse(os.path.exists(save_path))

        # Ensure urlopen is not called
        self.mock_urlopen.assert_not_called()
