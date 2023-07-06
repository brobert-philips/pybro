"""
File: utils/files.py

This file defines several classes and methods to ease file and
directory management in pybro package.
"""

# Import packages and submodules
import os
import logging

# Import classes and methods
from PyQt6.QtWidgets import QApplication, QFileDialog

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
    file_dir : str
        Directory of the file.
    """

    FILE_TYPES = {
        "": "All files",
    }
    """Supported file extensions."""

    def __init__(self, file_path: str = None) -> None:
        """
        Initialize a generic file object.

        This method first checks the provided path. It opens a
        file-selection dialog box if no path is provided. If file
        exists and is supported, it processes the file.

        Parameters
        ----------
        file_path : str
            Path to the file.
        """
        # Select file if no path is provided
        try:
            if file_path is None:
                file_types = \
                    [f"{value} (*{key})" for key, value in self.FILE_TYPES.items()]
                file_types = ";;".join(file_types)
                file_path  = GenericFile.dialog_select_file(opt=file_types)
        finally:
            self.file_path = os.path.abspath(file_path)

        # Control if path is valid and file supported
        if not self.__class__.test_file(self.file_path):
            err_msg = f"File is not supported ({self.file_path})."
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

        # Extract file information
        self.file_name = os.path.basename(self.file_path)
        self.file_ext  = os.path.splitext(self.file_name)[1]
        self.file_dir  = os.path.dirname (self.file_path)

    def __str__(self) -> str:
        """
        Return a string representation of the object.

        Returns
        -------
        str
            String representation of the object.
        """
        class_name = self.__class__.__name__
        return_str = \
            f"{class_name}(file_name: {self.file_name} ; file_dir: {self.file_dir})"
        return return_str

    def __eq__(self, __value: object) -> bool:
        """
        Check if two objects are equal.

        Parameters
        ----------
        __value : object
            Object to compare with.

        Returns
        -------
        bool
            True if objects are equal, False otherwise.
        """
        return self.file_path == __value.file_path

    @staticmethod
    def test_file(file_path: str = None) -> bool:
        """
        Test if file exists and is writable.

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

    @staticmethod
    def dialog_select_file(
        dir_path: str = os.getcwd(),
        func: str = "open",
        opt : str = "All files (*.*)"
    ) -> str:
        """
        Create a dialog for file selection (save/open).

        Parameters
        ----------
        dir_path : str, default 'os.getcwd()'
            Path to the starting folder.
        func : {"open", "save"}
            Type of dialog box.
        opt : str, default 'All files (*.*)'
            Options that can be used to select file. Different file
            types should be separated by 2 semicolons.

        Returns
        -------
        str
            Path to the selected file.
        """
        # Initialize method variables
        qt_app  = QApplication([])
        if not GenericDir.test_dir(dir_path):
            err_msg = "No valid folder path was provided."
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

        # Control if func parameters are valid
        title = f"{func.capitalize()} a file"
        if func not in ["open", "save"]:
            err_msg  = f"Method cannot handle '{func}' func-parameter."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Show dialog box
        if func == "open":      # open dialog box
            path = QFileDialog.getOpenFileName(None, title, dir_path, opt)
            path = path[0]

        elif func == "save":    # save dialog box
            path = QFileDialog.getSaveFileName(None, title, dir_path, opt)
            path = f"{os.path.dirname(path[0])}{os.sep}{os.path.basename(path[0])}"

        else:
            err_msg  = f"Method cannot handle '{func}' func-parameter.)"
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Return path
        qt_app.closeAllWindows()
        logger.info("File %s was selected.", path)
        return path


class GenericDir:
    """
    Generic directory class.

    Attributes
    ----------
    dir_path : str
        Path to the folder.
    file_class : class, default GenericFile
        Supported file class.
    file_list : list[file_class]
        List of the files in the folder.
    """

    def __init__(self, dir_path: str = None, file_class: object =  GenericFile) -> None:
        """
        Initialize a generic directory object.

        This method is first checks the provided path. It opens a
        directory-selection dialog box if no path is provided. If
        directory exists and files are supported, it loads all files.

        Parameters
        ----------
        dir_path : str
            Path to the directory.
        file_class : class, default GenericFile
            Supported file class.
        """
        # Check dir_path and set its instance value
        # Select directory path if no path is provided
        if dir_path is None:
            dir_path  = GenericDir.dialog_select_dir()
        dir_path = os.path.abspath(dir_path)

        # Control if dir_path is valid
        if not GenericDir.test_dir(dir_path):
            err_msg = f"No valid directory path was provided ({dir_path})."
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

        # Set instance attributes
        self.dir_path   = dir_path
        self.file_class = file_class

        # List all supported files in directory
        self.file_list = self.list_files(
            dir_path   = self.dir_path,
            recur      = True,
            file_class = self.file_class
        )

    def __str__(self) -> str:
        """
        Return a string representation of the object.

        Returns
        -------
        str
            String representation of the object.
        """
        class_name = self.__class__.__name__
        return_str = \
            f"{class_name}(dir_path: {self.dir_path} ; file_class: {self.file_class})"
        return return_str

    def __eq__(self, __value: object) -> bool:
        """
        Check if two objects are equal.

        Parameters
        ----------
        __value : object
            Object to compare with.

        Returns
        -------
        bool
            True if objects are equal, False otherwise.
        """
        if not isinstance(__value, GenericDir):
            return False

        tmp_test = self.dir_path == __value.dir_path
        return tmp_test and (self.file_class == __value.file_class)

    @staticmethod
    def test_dir(dir_path: str):
        """
        Test if directory is a writable directory.

        Parameters
        ----------
        dir_path : str
            Path to directory to test. Path must exist and be writable.

        Returns
        -------
        bool
            True if path to directory is valid and directory is
            writable, False otherwise.
        """
        # Check directory path and reformat it
        if dir_path is None:
            logger.info("No directory path was provided.")
            return False

        # Check if directory exists or if directory can be created
        if not os.path.isdir(dir_path):
            logger.info("%s does not exist.", dir_path)
            return False

        if os.path.isfile(dir_path):
            logger.info("%s is a file, and not a folder.", dir_path)
            return False

        if not os.access(dir_path, os.R_OK):
            logger.info("%s is not readable.", dir_path)
            return False

        if not os.access(dir_path, os.W_OK):
            logger.info("%s is not writable.", dir_path)
            return False

        return True

    @staticmethod
    def dialog_select_dir(dir_path: str = os.getcwd()) -> str:
        """
        Create a dialog for directory selection.

        Parameters
        ----------
        dir_path : str, default 'os.getcwd()'
            Path to the starting folder.

        Returns
        -------
        str
            Path to the selected directory.
        """
        # Initialize method variables
        qt_app  = QApplication([])
        if not GenericDir.test_dir(dir_path):
            err_msg = "No valid initial directory path was provided."
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

        # Show dialog box and return path
        title = "Select a folder"
        path = QFileDialog.getExistingDirectory(None, title, dir_path)

        # Return path
        qt_app.closeAllWindows()
        logger.info("Directory %s was selected.", path)
        return path

    @staticmethod
    def list_files(
        dir_path  : str,
        recur     : bool   = False,
        file_class: object =  GenericFile
    ) -> list[str]:
        """
        Lists all files in folder.

        Parameters
        ----------
        dir_path : str
            Path to folder to test. Path must exist and be writable.
        recur : bool, default False
            If True, searches recursively.
        file_class : class, default GenericFile
            Supported file class.

        Returns
        -------
        list[str]
            List of all supported files.
        """
        # Initialize method variables
        filelist = []

        # Build files list
        if file_class.test_file(dir_path):    # file path
            return dir_path

        if os.path.isdir(dir_path):     # folder path
            # Loop over all files within the folder
            for file in os.listdir(dir_path):
                file_path = dir_path + os.sep + file

                if os.path.isfile(file_path):   # file path
                    # if file_class.test_file(file_path):
                    #     filelist.append(file_path)
                    filelist.append(file_path)
                elif recur:                     # recursive search
                    filelist.extend(GenericDir.list_files(file_path, recur, file_class))

        else:   # path is not a file or a directory
            err_msg = f"{dir_path} is not a file or a directory."
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

        return filelist
