"""
File: utils/helpers.py

This file defines several methods and decorators to ease configuration
and implementation of classes and methods in pybro package.
"""

# Import packages and submodules
import os
import logging
import logging.config
import time

# Import classes and methods
from datetime           import datetime
from pybro.utils.files  import GenericFile

# Initialize logging in this file
logger = logging.getLogger(__name__)


def setup_logging(log_type= "prod", output="file") -> None:
    """
    Load a logging configuration file.

    Parameters
    ----------
    log_type : {"prod", "dev"}
        Type of logging.
    output : {"file", "stdout"}
        Output of logging.
    """
    # Default folders
    package_dir = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
    package_dir = f"{os.sep}".join(package_dir[:-3])
    config_dir  = f"{package_dir}{os.sep}config"
    logs_dir    = f"{package_dir}{os.sep}logs"

    # Select configuration file
    config_path = f"{config_dir}{os.sep}logging.{log_type}.{output}.ini"
    if not GenericFile.test_file(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    # Setup logging configuration
    timestamp   = datetime.now().strftime("%Y%m%d-%H%M%S")
    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{logs_dir}{os.sep}{timestamp}.log"}
    )
    logger.info("Loaded logging configuration from %s", config_path)


def method_exec_dur(func):
    """
    Measure execution duration of a method.

    Parameters
    ----------
    func : function
        Function for which results are cached.

    Returns
    -------
    result
        Result of the method.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result     = func(*args, **kwargs)
        end_time   = time.perf_counter()

        logger.info(
            "Method (%s) was executed in %.2f sec.",
            func.__name__,
            (end_time - start_time)
        )
        return result

    return wrapper
