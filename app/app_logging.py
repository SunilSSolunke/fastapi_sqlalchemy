import logging
from google.cloud import logging as gcp_logging

# Create a Cloud Logging client
logging_client = gcp_logging.Client()

# Create a logger
logger = logging_client.logger("notes-service")

# Create a custom logger
# logger = logging.getLogger('notes-service')

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("file.log")
# logger.setLevel(logging.DEBUG)
# Create formatters and add it to handlers
c_format = logging.Formatter(
    "%(asctime)s:%(name)s:%(module)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s"
)
f_format = logging.Formatter(
    "%(asctime)s|%(name)s|%(module)s|%(filename)s|%(funcName)s|%(lineno)d|%(levelname)s|%(message)s"
)
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)
