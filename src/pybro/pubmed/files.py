"""
File: pubmed/files.py

This file defines several classes and methods to ease PUBMED files
management in pybro package.
"""

# Import packages and submodules
import logging
import pandas

# Import submodules, classes and methods
from pybro.utils    import GenericFile

# Initialize logging in this file
logger = logging.getLogger(__name__)


class PubmedFile(GenericFile):
    """
    PUBMED file class inheriting from GenericFile.

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
        ".pubmed": "PUBMED files",
    }
    """Supported file extensions."""

    AUTHOR_FIELDS = [
        "FAU",
        "AU",
        "AUID",
        "AD",
    ]

    def __init__(self, file_path: str = None) -> None:
        """
        Initialize a PUBMED file object.

        This method first initializes the GenericFile attributes and
        then extracts PUBMED data from file to generate a PUBMED
        database.

        Parameters
        ----------
        file_path : str
            Path to the DICOM file.
        """
        # Initialize parent attributes
        super().__init__(file_path)

        # Read PUBMED file to build PUBMED database
        articles = []
        authors  = []
        keywords = []
        tmp_pmid = {}
        tmp_auid = {}
        tmp_tag  = ""

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                # Extract line info
                tag  = line[:4].strip()
                line = line[5:].strip()

                # New bibliography entry
                if tag == "PMID":
                    if tmp_pmid:
                        articles.append(tmp_pmid)
                    tmp_pmid = {tag: line}

                # New author entry
                if tag == "FAU":
                    if tmp_auid:
                        authors.append(tmp_auid)
                    tmp_auid = {"PMID": tmp_pmid["PMID"], tag: line}

                # Check if tag is defined
                if not tag:
                    tag = tmp_tag
                else:
                    tmp_tag = tag

                if tag in self.AUTHOR_FIELDS:
                    tmp_auid[tag] = tmp_auid[tag] + line if tag in tmp_auid else line
                elif tag == "MH":
                    keywords.append({"PMID": tmp_pmid["PMID"], tag: line})
                else:
                    tmp_pmid[tag] = tmp_pmid[tag] + line if tag in tmp_pmid else line

            # Append last article entry
            articles.append(tmp_pmid)

        # Create DataFrames
        articles = pandas.DataFrame(articles)
        authors  = pandas.DataFrame(authors)
        keywords = pandas.DataFrame(keywords)

        # Clean up all dataframes
        articles.fillna("", inplace=True)
        authors.fillna("", inplace=True)
        keywords.fillna("", inplace=True)

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

        # Control if there is at least one PUBMED entry
        try:
            tags = []
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Extract tag info
                    tag  = line[:4].strip()

                    # Extract all tags from PUBMED file
                    if (tag not in tags) and tag:
                        tags.append(tag)

            # There should be at least one PMID tag
            if "PMID" not in tags:
                raise IOError

        except IOError:
            return False

        return True
