https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy/

run command -> 
uvicorn app.main:app --host localhost --port 8000 --reload

Logger ENV file :->

# Custom Logger Name
CUSTOM_LOGGER_NAME = notes-service
# Custom Logger Logging Level
LOGGING_LEVEL = DEBUG
# To check if running locally, if 1 then will generate logs in logs.log file.
# False = 0
# True = 1
LOGS_ON_LOCAL_FILE = 1
# Local log file name
LOCAL_LOG_FILE_NAME = notes-service.log
# Need LOGS over GCP
# False = 0
# True = 1
LOGS_ON_GCP = 0
# Exclude below loggers over GCP.
EXCLUDE_LOGGERS_ON_GCP=sqlalchemy.engine.Engine
# Log Format for GCP as well as local
LOG_FORMAT = %(asctime)s:%(name)s:%(module)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s

