from pydantic import BaseModel, Field
from typing import  Optional
from uuid import UUID
from datetime import datetime
from management.shared.enums import BorrowStatus

class LibraryBase(BaseModel):
    name: str = Field(..., description="The name of the library")
    city: str = Field(..., description="The city where the library is located")

class LibraryCreate(LibraryBase):
    pass

class Library(LibraryBase):
    Id: UUID

    class Config:
        form_attributes = True

class BookBase(BaseModel):
    title: str = Field(..., description="The title of the book")
    author: str = Field(..., description="The author of the book")
    isbn: str = Field(..., description="The ISBN number of the book/unique")
    copies_available: int = Field(..., ge=0, description="The number of copies available")

class BookCreate(BookBase):
    pass

class Book(BookBase):
    Id: UUID

    class Config:
        form_attributes = True
#################################################
class MemberBase(BaseModel):
    name: str = Field(..., description="The name of the member")
    email: str = Field(..., description="The email address of the member")

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    Id: UUID

    class Config:
        form_attributes = True
###############################################################
class BorrowRecordBase(BaseModel):
    book_id: UUID = Field(..., description="book_id being borrowed")
    member_id: UUID = Field(..., description="member_id borrowing the book")
    library_id: UUID = Field(..., description="library_id where the book is located")
    borrowed_at: datetime = Field(..., description="date of borrowing the book")
    due_date: datetime = Field(..., description="due date for returning the book")
    returned_at: Optional[datetime] = Field(None, description="date/time when the book was returned")
    status: BorrowStatus = Field(..., description="status of the borrowed book")
class BorrowRecordCreate(BorrowRecordBase):
    pass
class BorrowRecord(BorrowRecordBase):
    Id: UUID

    class Config:
        form_attributes = True
        use_enum_values = True

class BorrowRecordUpdate(BaseModel):
    returned_at: Optional[datetime] = Field(None, description=" date/time when the book was returned")
    status: Optional[BorrowStatus] = Field(None, description="status of the borrow ")
    class Config:
        use_enum_values = True