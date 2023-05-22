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
        logger.info("All checks are passed now.")
        return {"message": "All set now!!"}
