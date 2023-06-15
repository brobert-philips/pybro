"""
File: tests/test_dicom.py
"""

# Import packages and submodules

# Import submodules, classes and methods
from pybro.dicom    import DicomFile, DicomDir


def test_dicom_file():
    """
    Test the `DicomFile` class.
    """
    # Anonymize a DICOM file
    dicom_file = DicomFile("ext/data/dicom/supported_file.dcm")
    print(dicom_file)
    dicom_file.anonymize()

def test_dicom_folder():
    """
    Test the `DicomFolder` class.
    """
    # Anonymize a DICOM file
    dicom_dir = DicomDir("ext/data/dicom/dicom_exam")
    print(dicom_dir)
    dicom_dir.anonymize()
