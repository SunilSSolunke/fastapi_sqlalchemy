from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,status, APIRouter,Response
from .database import get_db

# Define router.
router = APIRouter()

# [..note..] get all notes
@router.get(path='/')
def get_notes(
    db: Session = Depends(dependency=get_db),
    limit: int = 10,
    page: int = 1,
    search: str = ''
):
    '''
    # get all notes function.
    This returns all notes based on provided search criteria for titles if any. 
    '''
    try:
        skip = (page - 1) * limit
        notes = db.query(entities=models.Note).filter(models.Note.title.contains(other=search)).limit(limit=limit).offset(offset=skip).all()
        return { 'status':'success', 'results': len(notes), 'notes': notes}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry ,I can not give you notes!")
    
# [note] create a new note.
@router.post(path='/', status_code = status.HTTP_201_CREATED)
def create_note(
    payload : schemas.NoteBaseSchema,
    db: Session = Depends(dependency=get_db)
    ):
    '''
    # create a new note function.
    This creates a new note based on provided payload. 
    '''
    try:
        new_note = models.Note(**payload.dict())
        db.add(instance=new_note)
        db.commit()
        db.refresh(instance=new_note)
        return { 'status':'success',  'note': new_note}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry ,I can not create note!")

# [note] update an existing note.
@router.patch(path='/{noteId}')
def update_note(noteId: str,
                payload: schemas.NoteBaseSchema,
                db: Session = Depends(dependency=get_db)
                ):
    # prepare and execute query to execute towards database
    note_query = db.query(entities=models.Note).filter(models.Note.id == noteId)
    # get first element from above result
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No note with this id: {noteId} found')
    
    # get new data from payload
    update_data = payload.dict(exclude_unset=True)

    # start database transactio now
    note_query.filter(models.Note.id == noteId).update(
        values=update_data,
        synchronize_session= False
    )
    db.commit()
    db.refresh(db_note)

    return {"status": "success", "note": db_note}

# [note] get a note
@router.get(path='/{noteId}')
def get_note(
    noteId: str,
    db: Session = Depends(dependency=get_db),
):
    '''
    # get a note function.
    This returns a note based on provided note id. 
    '''
    try:
        # check in the db is such note id exists.        
        note = db.query(entities=models.Note).filter(models.Note.id ==  noteId).first()        
        if not note:
            # as note does not exists in database raising 404. 
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail="No note with this id: {noteId} found")
        return { 'status':'success', 'note': note}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry ,I can not give you this note!")
    

# [note] delete a note
@router.delete(path='/{noteId}')
def delete_note(
    noteId: str,
    db: Session = Depends(dependency=get_db),
):
    '''
    # delete a note function.
    This deletes provided note id. 
    '''
    try:
        # check in the db is such note id exists.
        note_query = db.query(entities=models.Note).filter(models.Note.id ==  noteId)      
        note = note_query.first()        
        if not note:
            # as note does not exists in raising 404. 
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail="No note with this id: {noteId} found")
        else:
            note_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code = status.HTTP_204_NO_CONTENT) 
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry ,I can not delete {noteId} note!")
    