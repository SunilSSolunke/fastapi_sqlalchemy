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
