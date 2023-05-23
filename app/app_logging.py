# -*- coding: utf-8 -*-

""" 
This is for setting up logging.
"""
__author__ = "Sunil S S"
__date__ = "2023/05/23"


# importing dotenv for .env file
import os
from dotenv import load_dotenv

# take env. variables from .env file
load_dotenv()

# Get all declared enviornment variables.

ENV_CUSTOM_LOGGER_NAME = os.environ.get("CUSTOM_LOGGER_NAME")
ENV_LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")
ENV_LOGS_ON_LOCAL_FILE = int(os.environ.get("LOGS_ON_LOCAL_FILE"))
ENV_LOCAL_LOG_FILE_NAME = os.environ.get("LOCAL_LOG_FILE_NAME")
ENV_LOGS_ON_GCP = int(os.environ.get("LOGS_ON_GCP"))
ENV_EXCLUDE_LOGGERS_ON_GCP = os.environ.get("EXCLUDE_LOGGERS_ON_GCP")
ENV_LOG_FORMAT = os.environ.get("LOG_FORMAT")

# check log destination for GCP and set config accordingly

if ENV_LOGS_ON_GCP == 1:
    print("starting config of logging on GCP now")
    # import google cloud logging
    import google.cloud.logging

    # Create a Cloud Logging client
    logging_client = google.cloud.logging.Client()

    # Setting up exclued loggers variable for GCP.
    ENV_EXCLUDE_LOGGERS_ON_GCP = tuple(ENV_EXCLUDE_LOGGERS_ON_GCP.split(","))

    # Setting up cloud logging now.
    logging_client.setup_logging(excluded_loggers=ENV_EXCLUDE_LOGGERS_ON_GCP)

# Setting normal python logging now
import logging

# Create a custom logger.
logger = logging.getLogger(ENV_CUSTOM_LOGGER_NAME)

# Set logging level for custom logger.
logger.setLevel(level=ENV_LOGGING_LEVEL)

# console handler and related config
c_handler = logging.StreamHandler()
c_format = logging.Formatter(ENV_LOG_FORMAT)
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

# check log destination for Local Run and set config accordingly
if ENV_LOGS_ON_LOCAL_FILE == 1:
    print("starting config of logging on local file now")
    f_handler = logging.FileHandler(ENV_LOCAL_LOG_FILE_NAME)
    f_format = logging.Formatter(ENV_LOG_FORMAT)
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
