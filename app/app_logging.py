# import google cloud logging
import google.cloud.logging

# Create a Cloud Logging client
logging_client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
logging_client.setup_logging(
    log_level=10, excluded_loggers=("sqlalchemy.engine.Engine",)
)
# [END logging_handler_setup]

# Now importing standard logging
import logging


# Create a custom logger
logger = logging.getLogger("notes-service")

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("file.log")
logger.setLevel(logging.DEBUG)

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
logger.addHandler(c_handler)
logger.addHandler(f_handler)
