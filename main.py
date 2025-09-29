from fastapi import FastAPI
from management.Services import Book, Members, Library, BorrowRecords
app = FastAPI()
app.include_router(Book.router)
app.include_router(Members.router)
app.include_router(Library.router)
app.include_router(BorrowRecords.router)