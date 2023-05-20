#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Entry point for Notes Application
"""

__author__ = "Sunil S S"
__date__ = "2023/05/20"

from fastapi import FastAPI

# Initialize the app.
app = FastAPI()

# GET Methoed for healh checking.
@app.get("/api/healthchecker")
def health_checker():
    '''
    # health_checker function.
    This is a dummy healthchecker. 
    '''

    return {"message":"All set now!!"}