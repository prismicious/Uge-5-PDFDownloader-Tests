import os
import unittest

from scripts.download_files import is_valid_pdf
from tests.utils.utils import create_corrupt_pdf, create_pdf_file, delete_folder

path = "tests/test_files"


class TestIsValidPDF(unittest.TestCase):

    """This test suite will use Arrange, Act, Assert (AAA) pattern."""

    def setUp(self) -> None:
        """Set up test environment."""
        os.makedirs(path, exist_ok=True)

    def tearDown(self) -> None:
        """Clean up test environment."""
        delete_folder(path)

    def test_is_valid_pdf_valid(self) -> None:
        # Arrange
        valid_pdf_path: str = f"{path}/valid_pdf.pdf"
        create_pdf_file(valid_pdf_path)

        # Act
        result: bool = is_valid_pdf(valid_pdf_path)

        # Assert
        self.assertTrue(result)

    def test_is_valid_pdf_invalid(self) -> None:
        # Arrange
        invalid_pdf_path: str = f"{path}/invalid_pdf.pdf"

        # Act
        result: bool = is_valid_pdf(invalid_pdf_path)

        self.assertFalse(result)

    def test_empty_file(self) -> None:
        # Arrange
        empty_file_path: str = f"{path}/empty_file.pdf"
        with open(empty_file_path, 'wb') as f:
            pass

        # Act
        result: bool = is_valid_pdf(empty_file_path)

        # Assert
        self.assertFalse(result)

    def test_non_pdf_file(self) -> None:
        # Arrange
        non_pdf_path: str = f"{path}/non_pdf.txt"
        with open(non_pdf_path, 'w') as f:
            f.write("This is not a PDF file.")

        # Act
        result: bool = is_valid_pdf(non_pdf_path)

        # Assert
        self.assertFalse(result)

    def test_non_existent_file(self) -> None:
        # Arrange
        non_existent_path: str = "tests/test_files/non_existent.pdf"

        # Act
        result: bool = is_valid_pdf(non_existent_path)

        # Assert
        self.assertFalse(result)

    def test_corrupt_pdf(self) -> None:
        # Arrange
        save_path = f"output/downloads/corrupt_pdf.pdf"
        create_corrupt_pdf(save_path)

        # Act
        result: bool = is_valid_pdf(save_path)

        # Assert
        self.assertFalse(result)

        # Clean up the corrupt file
        if os.path.exists(save_path):
            os.remove(save_path)
