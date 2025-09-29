from fastapi import HTTPException, Depends, APIRouter, Form
from sqlalchemy.orm import Session as DbSession
from typing import Optional
from typing import List
from uuid import UUID
from Database import Session
import management.Models as Models
from management.Schemas import BorrowRecordCreate, BorrowRecord, BorrowRecordUpdate
from datetime import datetime
from management.shared.enums import BorrowStatus

router = APIRouter()

@router.post("/borrow/", response_model=BorrowRecord)
def create_borrow_record(borrow_record: BorrowRecordCreate=Form(...), db: DbSession = Depends(Session.get_db)):
    if borrow_record.member_id is None or borrow_record.book_id is None or borrow_record.library_id is None:
        raise HTTPException(status_code=400, detail="Member ID, Book ID, and Library ID are required")
    book = db.query(Models.Book).filter(Models.Book.Id == borrow_record.book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if borrow_record.due_date <= borrow_record.borrowed_at:
        raise HTTPException(status_code=400, detail="Due date must be after borrowed date")
    if borrow_record.status not in [BorrowStatus.borrowed, BorrowStatus.returned, BorrowStatus.overdue]:
        raise HTTPException(status_code=400, detail="Invalid borrow status")
    if borrow_record.status == BorrowStatus.returned :
        book.copies_available += 1
    elif borrow_record.status == BorrowStatus.borrowed:
        if book.copies_available <= 0:
            raise HTTPException(status_code=400, detail="No copies available for this book")
        book.copies_available -= 1
    db_borrow_record = Models.BorrowRecord(**borrow_record.dict())
    db.add(db_borrow_record)
    db.commit()
    db.refresh(db_borrow_record)
    return db_borrow_record

@router.get("/borrow/{id}", response_model=BorrowRecord)
def read_borrow_record(id: UUID, db: DbSession = Depends(Session.get_db)):
    borrow_record = db.query(Models.BorrowRecord).filter(Models.BorrowRecord.Id == id).first()
    if borrow_record is None:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return borrow_record

@router.delete("/borrow/{id}", response_model=BorrowRecord)
def delete_borrow_record(id: UUID, db: DbSession = Depends(Session.get_db)):
    borrow_record = db.query(Models.BorrowRecord).filter(Models.BorrowRecord.Id == id).first()
    if borrow_record is None:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    db.delete(borrow_record)
    db.commit()
    return borrow_record

@router.put("/borrow/{id}", response_model=BorrowRecord)
def update_borrow_record(id: UUID, borrow_record_update: BorrowRecordUpdate=Form(...), db: DbSession = Depends(Session.get_db)):
    borrow_record = db.query(Models.BorrowRecord).filter(Models.BorrowRecord.Id == id).first()
    if borrow_record is None:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow_record_update.returned_at is not None:
        borrow_record.returned_at = borrow_record_update.returned_at
    if borrow_record_update.status is not None:
        if borrow_record_update.status not in [BorrowStatus.borrowed, BorrowStatus.returned, BorrowStatus.overdue]:
            raise HTTPException(status_code=400, detail="Invalid borrow status")
        if borrow_record.status != borrow_record_update.status:
            book = db.query(Models.Book).filter(Models.Book.Id == borrow_record.book_id).first()
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            if borrow_record_update.status == BorrowStatus.returned:
                book.copies_available += 1
                borrow_record.returned_at = datetime.utcnow()
            elif borrow_record_update.status == BorrowStatus.borrowed:
                if book.copies_available <= 0:
                    raise HTTPException(status_code=400, detail="No copies available for this book!!")
                book.copies_available -= 1
            borrow_record.status = borrow_record_update.status
    db.commit()
    db.refresh(borrow_record)
    return borrow_record


@router.get("/borrow/", response_model=List[BorrowRecord])
def read_borrow_records(db: DbSession = Depends(Session.get_db),status: Optional[BorrowStatus] = None,member: Optional[UUID] = None,library: Optional[UUID] = None,from_date: Optional[datetime] = None,to_date: Optional[datetime] = None):
    if status:
        borrow_records = db.query(Models.BorrowRecord).filter(Models.BorrowRecord.status == status).all()
    else:
        borrow_records = db.query(Models.BorrowRecord).all()
    if member:
        for record in borrow_records:
            if record.member_id == member:
                borrow_records = [record]
    if library:
        borrow_records = [record for record in borrow_records if record.library_id == library]
    if from_date:
        borrow_records = [record for record in borrow_records if record.borrowed_at >= from_date]
    if to_date:
        borrow_records = [record for record in borrow_records if record.borrowed_at <= to_date]
    if not borrow_records:
        raise HTTPException(status_code=404, detail="No borrow records found")
    return borrow_records

   