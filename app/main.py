#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Entry point for Notes Application
"""

__author__ = "Sunil S S"
__date__ = "2023/05/20"

from fastapi import FastAPI, APIRouter, status

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

# Define router.
router = APIRouter()

@router.get('/')
def get_notes():
    '''
    # get all notes function.
    This is a dummy get all notes function. 
    '''
    return "retrun a list of note items"

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_note():
    '''
    # create a note function.
    This is a dummy create note function. 
    '''
    return "created note item"

@router.patch('/{noteId}')
def update_note(noteId: str):
    '''
    # update a note function.
    This is a dummy update note function. 
    '''
    return f"update note item with id {noteId}"

@router.get('/{noteId}')
def get_note(noteId: str):
    '''
    # get a note function.
    This is a dummy get note function. 
    '''
    return f"get note item with id {noteId}"

@router.delete('/{noteId}')
def delete_note(noteId: str):
    '''
    # delete a note function.
    This is a dummy delete note function. 
    '''
    return f"delete note item with id {noteId}"

# Add tag and prefix for router to include in documentation.
app.include_router(router, tags=['Notes'], prefix='/api/notes')