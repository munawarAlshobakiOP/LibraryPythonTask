from uuid import uuid4,UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from Database.Base import Base
from management.shared.enums import BorrowStatus
from sqlalchemy import Enum as SqlEnum

class Library(Base):
    __tablename__ = "Library"
    Id: UUID=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: str = Column(String)
    city: str = Column(String)


class Book(Base):
    __tablename__ = "Book"
    Id: UUID=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: str = Column(String)
    author: str = Column(String)
    isbn: str = Column(String, unique=True)
    copies_available: int = Column(Integer)

class Member(Base):
    __tablename__ = "Member"
    Id: UUID=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: str = Column(String)
    email: str = Column(String, unique=True)

class BorrowRecord(Base):
    __tablename__ = "BorrowRecord"
    Id: UUID=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    book_id: UUID = Column(UUID(as_uuid=True), ForeignKey("Book.Id"))
    member_id: UUID = Column(UUID(as_uuid=True), ForeignKey("Member.Id"))
    library_id: UUID = Column(UUID(as_uuid=True), ForeignKey("Library.Id"))
    borrowed_at: DateTime = Column(DateTime)
    due_date: DateTime = Column(DateTime)
    returned_at: DateTime = Column(DateTime, nullable=True)
    status = Column(SqlEnum(BorrowStatus), default=BorrowStatus.borrowed)
