"""
File: dicom/files.py

This file defines several classes and methods to ease DICOM file and
DICOM directory management in pybro package.
"""

# Import packages and submodules
import os
import platform
import re
import logging
import pydicom

# Import submodules, classes and methods
from datetime       import datetime
# from pybro          import libdicom
from pybro.utils    import GenericFile, GenericDir

# Initialize logging in this file
logger = logging.getLogger(__name__)


"""Constant containing all cleared DICOM tags."""
CLEAR_TAGS = [
    "InstitutionName",
    "InstitutionAddress",
    "ReferringPhysicianName",
    "ReferringPhysicianAddress",
    "ReferringPhysicianTelephoneNumbers",
    "InstitutionalDepartmentName",
    "PhysiciansOfRecord",
    "PerformingPhysicianName",
    "NameOfPhysiciansReadingStudy",
    "OperatorsName",
    "AdmittingDiagnosesDescription",
    "OtherPatientIDs",
    "OtherPatientNames",
    "MedicalRecordLocator",
    "EthnicGroup",
    "Occupation",
    "AdditionalPatientHistory",
    "PatientComments",
    "RequestingPhysician",
    "RequestingService",
    "RequestedProcedureDescription",
    "ScheduledPerformingPhysicianName",
    "PerformedStationAETitle",
    "RequestAttributesSequence",
    "RequestedProcedureID",
    "IssueDateOfImagingServiceRequest",
    "ContentSequence",
]


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

    TODO: implement DICOM file anonymization
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

    @staticmethod
    def get_dicom_tags(
        dataset: pydicom.Dataset,
        tags: (list[str] | list[list[int]])
    ) -> dict[str, str]:
        """
        Get DICOM tag values from a DICOM dataset.

        Parameters
        ----------
        dataset : pydicom.Dataset
            DICOM dataset.
        tags : list[str] | list[list[int]]
            List of DICOM tag addresses (keywords or hexadecimal values).

        Returns
        -------
        dict[str, str]
            Dictionary where keys are requested DICOM tags and values are
            the DICOM tags values.
        """
        # Check if tags variable is a list of DICOM tags
        if not isinstance(tags, list):
            err_msg = f"Tags variable should be a list of tags, not a {type(tags)}."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Loop over all DICOM tags
        out_value = {}
        for tag in tags:

            # Check DICOM existence and get processed value
            if tag in dataset:
                out_value[tag] = dataset[tag].value

            else:
                out_value[tag] =  ""

            # Format out_value
            if dataset[tag].VR == "UI":
                out_value[tag] = out_value[tag].replace(".","+")
                out_value[tag] = sum(map(int, re.findall(r'[+-]?\d+', out_value[tag])))
                out_value[tag] = str(hex(int(out_value[tag]))).upper()[2:]

        return out_value

    @staticmethod
    def set_dicom_tags(
        dataset: pydicom.Dataset,
        tags: (list[str] | list[list[int]]),
        values: list[str]
    ) -> pydicom.Dataset:
        """
        Clear a DICOM tag value from a DICOM dataset.

        Parameters
        ----------
        dataset : pydicom.Dataset
            DICOM dataset.
        tags : list[str] | list[list[int]]
            List of DICOM tag addresses (keywords or hexadecimal values).
        values : list[str]
            List of DICOM tag values.

        Returns
        -------
        pydicom.Dataset
            DICOM dataset with cleared DICOM tags.
        """
        # Check if tags variable is a list of DICOM tags
        if not isinstance(tags, list):
            err_msg = f"Tags variable should be a list of tags, not a {type(tags)}."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Check if values variable is a list of string values
        if not isinstance(values, list):
            err_msg = f"Tags values should be a list of strings, not a {type(values)}."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Loop over all DICOM tags
        for tag, value in zip(tags, values):

            # Check if tag exists in DICOM dataset
            if tag in dataset:
                logger.info("Set tag %s to %s.", tag, value)
                dataset[tag].value = value

            else:
                logger.info("DICOM dataset has no %s tag.", tag)

        return dataset

    @staticmethod
    def clear_dicom_tags(
        dataset: pydicom.Dataset,
        tags: (list[str] | list[list[int]])
    ) -> pydicom.Dataset:
        """
        Clear a DICOM tag value from a DICOM dataset.

        Parameters
        ----------
        dataset : pydicom.Dataset
            DICOM dataset.
        tags : list[str] | list[list[int]]
            List of DICOM tag addresses (keywords or hexadecimal values).

        Returns
        -------
        pydicom.Dataset
            DICOM dataset with cleared DICOM tags.
        """
        # Check if tags variable is a list of DICOM tags
        if not isinstance(tags, list):
            err_msg = f"Tags variable should be a list of tags, not a {type(tags)}."
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Loop over all DICOM tags
        for tag in tags:

            # Check if tag exists in DICOM dataset
            if tag in dataset:
                logger.info("Clear tag %s.", tag)
                dataset[tag].clear()

            else:
                logger.info("DICOM dataset has no %s tag.", tag)

        return dataset

    def anonymize(self, new_dir_path: str = None) -> bool:
        """
        Anonymize a DICOM file.

        This method applies the `_anonymize_dataset` private method to
        the DICOM file dataset.

        If `new_dir_path` is given, the anonymized file is saved in the
        `new_dir_path` directory according to the following convention:
        * anonymized subdirectory is [PID]/[STUDY_UID]/[SERIES_UID]
        * anonymized file name is [MODALITY]_[IMG_TYPE]_[IMG_NUM].dcm

        If `new_dir_path` is not given, the anonymized file is saved
        in the same directory with `_anonymized.dcm` suffix.

        Parameters
        ----------
        new_dir_path : str
            Absolute path to the new anonymized DICOM file.
        """
        # Check if new directory path is given
        if new_dir_path is None:
            new_path  = self.file_dir + os.sep
            new_path += self.file_name[:-len(self.file_ext)] + "_anonymized.dcm"

        else:
            if GenericDir.test_dir(new_dir_path):
                new_path = new_dir_path
            else:
                logger.info("Directory %s does not exist.", new_dir_path)
                return False

        # Anonymize DICOM dataset and save to new file
        new_dataset = self._anonymize_dataset()
        new_dataset.save_as(new_path)
        # libdicom.anonymize_dicom(path=self.file_path, new_path=self.file_dir)
        return True

    def _anonymize_dataset(self) -> pydicom.Dataset:
        """
        Anonymize DICOM dataset.

        Returns
        -------
        pydicom.Dataset
            Anonymized DICOM dataset.
        """
        # Retrieve DICOM tags
        tags = [
            0x00181000, 0x00080020, 0x00080030, 0x0020000D, 0x00080008, 0x00100030,
        ]
        values       = DicomFile.get_dicom_tags(self.dataset, tags)
        serial_num   = values[0x00181000]
        study_date   = values[0x00080020]
        study_time   = values[0x00080030]
        study_uid    = values[0x0020000D]
        img_type     = values[0x00080008]
        img_type     = img_type[2] if len(img_type) > 2 else "UNK"

        # Control and reformat values
        if not serial_num.isnumeric():
            serial_num = datetime.today().strftime("%y%m%d")

        # Create new values
        new_pid        = serial_num + study_date[2:] + study_time[:4]
        new_pid        = str(hex(int(new_pid))).upper()[2:]
        new_study_date = study_date[:-4] + "0101"
        new_birth_date = values[0x00100030]
        new_birth_date = new_birth_date[:-4] + "0101"
        new_station    = platform.node().upper()

        # Anonymize tags
        tags = [
            0x00081010, 0x00080012, 0x00080020, 0x00080021,
            0x00080022, 0x00080023, 0x00080050, 0x00100010,
            0x00100020, 0x00100030, 0x00200010,
        ]
        values = [
            new_station   , new_study_date, new_study_date  , new_study_date,
            new_study_date, new_study_date, study_uid [-16:], new_pid       ,
            new_pid       , new_birth_date, study_uid[-16:] ,
        ]
        dataset = DicomFile.set_dicom_tags(self.dataset, tags, values)

        # Delete tags
        dataset = DicomFile.clear_dicom_tags(dataset=dataset, tags = CLEAR_TAGS)

        return dataset


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
