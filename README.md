run command -> 
uvicorn app.main:app --host localhost --port 8000 --reload

requirement.txt :->
```
anyio==3.6.2
cachetools==5.3.0
certifi==2023.5.7
charset-normalizer==3.1.0
click==8.1.3
colorama==0.4.6
dnspython==2.3.0
email-validator==2.0.0.post2
fastapi==0.95.2
fastapi-utils==0.2.1
google-api-core==2.11.0
google-auth==2.18.1
google-cloud-appengine-logging==1.3.0
google-cloud-audit-log==0.2.5
google-cloud-core==2.3.2
google-cloud-logging==3.5.0
googleapis-common-protos==1.59.0
greenlet==2.0.2
grpc-google-iam-v1==0.12.6
grpcio==1.54.2
grpcio-status==1.54.2
h11==0.14.0
httpcore==0.17.1
httptools==0.5.0
httpx==0.24.1
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.2
orjson==3.8.12
proto-plus==1.22.2
protobuf==4.23.1
pyasn1==0.5.0
pyasn1-modules==0.3.0
pydantic==1.10.7
python-dotenv==1.0.0
python-multipart==0.0.6
PyYAML==6.0
requests==2.30.0
rsa==4.9
six==1.16.0
sniffio==1.3.0
SQLAlchemy==1.4.48
starlette==0.27.0
typing_extensions==4.5.0
ujson==5.7.0
urllib3==1.26.15
uvicorn==0.22.0
watchfiles==0.19.0
websockets==11.0.3
```


Logger ENV file :->

```
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

```

app folder ->

app/__init__.py
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
This file is kept empty to convert app directory into python module
__author__ = "Sunil S S"
__date__ = "2023/05/20"
"""

```
app/app_logging.py ->

```
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

```

app/database.py :->

```
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define location of notes sqllite database.
SQLITE_DATABASE_URL = "sqlite:///./note.db"

# Create SQLAlchemy engine and provided it with the database URL.
engine = create_engine(SQLITE_DATABASE_URL,echo=True, connect_args={"check_same_thread": False})

# Create SQLAlchemy session with earlier defined engine.
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Define base so that SQLAlchemy can pick up tables from defined models.
Base = declarative_base()

# Create a new database session and close same after applciation is closed.
def get_db():
    '''
    # get database session function.
      input parameters = none.
      response = db connection.       
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

app/main.py

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Entry point for Notes Application
"""

__author__ = "Sunil S S"
__date__ = "2023/05/20"

from .app_logging import logger
from fastapi import FastAPI
from app import models, notes
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db

# Create tables/object strcuture as defined in the models.add()

models.Base.metadata.create_all(bind=engine)

# Initialize the app.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, tags=["Notes"], prefix="/api/notes")


# GET Methoed for healh checking.
@app.get("/api/healthchecker")
def health_checker():
    """
    # health_checker function.
    This is a healthchecker.
    """
    test_db_connection = get_db()
    if test_db_connection is None:
        logger.critical("Unable to connect to database.", stack_info=True, stacklevel=2)
    # Test GCS Connection also like this one..
    else:
        logger.info("All checks are passed now from INFO Level.")
        logger.debug("All checks are passed now from DEBUG Level.")
        return {"message": "All set now!!"}

```
app/models.py

```
from .database import Base
from sqlalchemy import TIMESTAMP,Column,String,Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

class Note(Base):
    '''
    # Database Schema for notes table.    
    '''
    __tablename__ = 'notes'
    id = Column(GUID, primary_key = True,default = GUID_DEFAULT_SQLITE)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    category = Column(String, nullable= True)
    publsihed = Column(Boolean, nullable = False, default = True)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt =Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

```

app/notes.py

```
# -*- coding: utf-8 -*-

""" 
Notes API Router and related CRUD implementation.
"""

__author__ = "Sunil S S"
__date__ = "2023/05/22"

from .app_logging import logger
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

# Define router.
router = APIRouter()


# [..note..] get all notes
@router.get(path="/")
def get_notes(
    db: Session = Depends(dependency=get_db),
    limit: int = 10,
    page: int = 1,
    search: str = "",
):
    """
    # get all notes function.
    This returns all notes based on provided search criteria for titles if any.
    """
    try:
        skip = (page - 1) * limit
        notes = (
            db.query(models.Note)
            .filter(models.Note.title.contains(other=search))
            .limit(limit=limit)
            .offset(offset=skip)
            .all()
        )
        logger.debug(f"Total Number of Notes retrived are {len(notes)}")
        return {"status": "success", "results": len(notes), "notes": notes}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry ,I can not give you notes!",
        )


# [note] create a new note.
@router.post(path="/", status_code=status.HTTP_201_CREATED)
def create_note(
    payload: schemas.NoteBaseSchema, db: Session = Depends(dependency=get_db)
):
    """
    # create a new note function.
    This creates a new note based on provided payload.
    """
    try:
        new_note = models.Note(**payload.dict())
        db.add(new_note)
        db.commit()
        db.refresh(instance=new_note)
        logger.debug(f"New note created with note id {new_note.id}")
        return {"status": "success", "note": new_note}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry ,I can not create note!",
        )


# [note] update an existing note.
@router.patch(path="/{noteId}")
def update_note(
    noteId: str,
    payload: schemas.NoteBaseSchema,
    db: Session = Depends(dependency=get_db),
):
    # prepare and execute query to execute towards database
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    # get first element from above result
    db_note = note_query.first()

    if not db_note:
        logger.debug(f"No Note found with note id {noteId}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No note with id: {noteId} found",
        )

    # get new data from payload
    update_data = payload.dict(exclude_unset=True)

    # start database transactio now
    note_query.filter(models.Note.id == noteId).update(
        values=update_data, synchronize_session=False
    )
    db.commit()
    db.refresh(db_note)
    logger.debug(f"Updated Note with note id {noteId}")
    return {"status": "success", "note": db_note}


# [note] get a note
@router.get(path="/{noteId}")
def get_note(
    noteId: str,
    db: Session = Depends(dependency=get_db),
):
    """
    # get a note function.
    This returns a note based on provided note id.
    """
    try:
        # check in the db is such note id exists.
        note = db.query(models.Note).filter(models.Note.id == noteId).first()
        if not note:
            # as note does not exists in database raising 404.
            logger.debug(f"No Note found with note id {noteId}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="No note with this id: {noteId} found"
            )
        logger.debug(f"Returning Note with note id {noteId}")
        return {"status": "success", "note": note}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry ,I can not give you this note!",
        )


# [note] delete a note
@router.delete(path="/{noteId}")
def delete_note(
    noteId: str,
    db: Session = Depends(dependency=get_db),
):
    """
    # delete a note function.
    This deletes provided note id.
    """
    try:
        # check in the db is such note id exists.
        note_query = db.query(models.Note).filter(models.Note.id == noteId)
        note = note_query.first()
        if not note:
            # as note does not exists in raising 404.
            logger.debug(f"No Note found with note id {noteId}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="No Note with this id: {noteId} found"
            )
        else:
            note_query.delete(synchronize_session=False)
            db.commit()
            logger.debug(f"Note with note id {noteId} is deleted now.")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry ,I can not delete {noteId} Note!",
        )

```

app/schemas.py
```
from datetime import datetime
from typing import List
from pydantic import BaseModel

class NoteBaseSchema(BaseModel):
    '''
    # Pydantic Schema for a note object for auto-conversion and auto-validation.    
    '''
    id: str | None = None
    title: str
    content: str
    category: str | None = None
    publsihed: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListNoteResponse(BaseModel):
    '''
    # Pydantic Schema for list of note object/s for auto-conversion and auto-validation.    
    '''
    status : str
    results: int
    notes : List[NoteBaseSchema]     
```

![logging_screenshot](https://github.com/SunilSSolunke/fastapi_sqlalchemy/assets/93458668/9d356f51-ca03-4dde-89fa-990b8ca400a3)


