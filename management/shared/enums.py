import enum

class BorrowStatus(str, enum.Enum):
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"
    