from Database import  Session
from sqlalchemy.orm import Session as DbSession
from fastapi import Depends, HTTPException,APIRouter, Form
from uuid import UUID
from typing import List
from management.Schemas import LibraryCreate, Library
import management.Models as Models
router = APIRouter()

@router.post("/libraries/", response_model=Library)
def create_library(library: LibraryCreate=Form(...), db: DbSession = Depends(Session.get_db)):
    db_library = Models.Library(**library.dict())
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library

@router.get("/libraries/", response_model=List[Library])
def read_libraries(db: DbSession = Depends(Session.get_db)):
    libraries = db.query(Models.Library).all()
    if not libraries:
        raise HTTPException(status_code=404, detail="No libraries found")
    return libraries

@router.get("/libraries/{id}", response_model=Library)
def read_library(id: UUID, db: DbSession = Depends(Session.get_db)):
    library = db.query(Models.Library).filter(Models.Library.Id == id).first()
    if library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return library

