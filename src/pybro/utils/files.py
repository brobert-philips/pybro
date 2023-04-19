"""
File: utils/files.py

This file defines several classes and methods to ease file and
directory management in pybro package.
"""

# Import packages and submodules
import os
import logging

# Initialize logging in this file
logger = logging.getLogger(__name__)


class GenericFile:
    """
    Generic file class.

    Attributes
    ----------
    file_path : str
        Path to the file.
    file_name : str
        Base name of the file.
    file_ext : str
        Extension of the file.
    file_folder : str
        Folder of the file.
    """

    def __init__(self, file_path: str = None) -> None:
        """
        Initialize a generic file object.

        This method first checks the provided path. It opens a
        file-selection dialog box if no path is provided. If file
        exists and is supported, it processes the file.

        Parameters
        ----------
        path : str
            Path to the file.
        """
        self.file_path = file_path

    @staticmethod
    def test_file(file_path: str = None) -> bool:
        """
        Test if a file exists.

        Parameters
        ----------
        file_path : str
            Path to the file.

        Returns
        -------
        bool
            True if file exists and is writable, False otherwise.
        """
        # Check file path and reformat it
        if file_path is None:
            err_msg = "No file path was provided."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Check if file exists or if file can be created
        if not os.path.isfile(file_path):
            logger.info("%s is not a file.", file_path)
            return False

        if not os.access(file_path, os.R_OK):
            logger.info("%s is not readable.", file_path)
            return False

        if not os.access(file_path, os.W_OK):
            logger.info("%s is not writable.", file_path)
            return False

        return True
