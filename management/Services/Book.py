from fastapi import HTTPException, Depends, APIRouter, Form
from sqlalchemy.orm import Session as DbSession
from typing import List
from uuid import UUID
from Database import  Session
import management.Models as Models
from management.Schemas import BookCreate, Book
router = APIRouter()

@router.post("/books/", response_model=Book)
def create_book(book: BookCreate=Form(...), db: DbSession = Depends(Session.get_db)):
    if db.query(Models.Book).filter(Models.Book.isbn == book.isbn).first():
        raise HTTPException(status_code=400, detail="ISBN already exists")
    if book.copies_available < 0:
        raise HTTPException(status_code=400, detail="Copies available should be non-negative")
    db_book = Models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/books/", response_model=List[Book])
def read_books(db: DbSession = Depends(Session.get_db)):
    books = db.query(Models.Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

@router.get("/books/{id}", response_model=Book)
def read_book(id: UUID, db: DbSession = Depends(Session.get_db)):
    book = db.query(Models.Book).filter(Models.Book.Id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
