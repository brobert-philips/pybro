"""
File: dicom/files.py

This file defines several classes and methods to ease DICOM file and
DICOM directory management in pybro package.
"""

# Import packages and submodules
import logging
import pydicom

# Import submodules, classes and methods
from pybro.utils    import GenericFile, GenericDir

# Initialize logging in this file
logger = logging.getLogger(__name__)


class DicomFile(GenericFile):
    """
    DICOM file class inheriting from GenericFile.

    Attributes
    ----------
    file_path : str
        Path to the file.
    file_name : str
        Base name of the file.
    file_ext : str
        Extension of the file.
    file_dir : str
        Directory of the file.
    dataset : pydicom.dataset.FileDataset
        DICOM dataset.
    """

    FILE_TYPES = {
        ""    : "All files"  ,
        ".dcm": "DICOM files",
    }
    """Supported file extensions."""

    def __init__(self, file_path: str = None) -> None:
        """
        Initialize a DICOM file object.

        This method first initializes the GenericFile attributes and
        then extracts the DICOM dataset object.

        Parameters
        ----------
        file_path : str
            Path to the DICOM file.
        """
        # Initialize parent attributes
        super().__init__(file_path)

        # Retrieve DICOM dataset
        self.dataset = pydicom.dcmread(self.file_path)

    @staticmethod
    def test_file(file_path: str = None) -> bool:
        """
        Test if file exists, is writable and is a DICOM supported file.

        Parameters
        ----------
        file_path : str
            Path to the file.

        Returns
        -------
        bool
            True if file exists and is writable, False otherwise.
        """
        # Test if file exists and is writable
        if not GenericFile.test_file(file_path):
            return False
        try:
            dicom_tags = pydicom.dcmread(file_path)
        except pydicom.errors.InvalidDicomError:
            logger.info("No DICOM file found (%s).", file_path)
            return False

        # ImageType tag must exist, and it should have at least 3 values
        if (0x0008, 0x0008) not in dicom_tags:
            logger.info("No ImageType tag.")
            return False

        if len(dicom_tags[0x0008, 0x0008].value) < 3:
            logger.info("No ImageType tag.")
            return False

        return True


class DicomDir(GenericDir):
    """
    DICOM directory class inheriting from GenericDir.

    Attributes
    ----------
    dir_path : str
        Path to the folder.
    file_class : class, default GenericFile
        Supported file class.
    file_list : list[file_class]
        List of the files in the folder.
    """

    def __init__(self, dir_path: str = None) -> None:
        """
        Initialize a DICOM directory object.

        This method first initializes the GenericDir attributes.

        Parameters
        ----------
        dir_path : str
            Path to the directory.
        """
        # Initialize parent attributes
        super().__init__(dir_path, DicomFile)
