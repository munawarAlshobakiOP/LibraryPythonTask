# Library Management API

A comprehensive REST API for managing library operations built with FastAPI and SQLAlchemy.


### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/munawarAlshobakiOP/LibraryPythonTask.git
   cd LibraryPythonTask
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Create a PostgreSQL database
   - Update database connection settings in your environment

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```



## API Endpoints

### Books
- `POST /books/` - Create a new book
- `GET /books/` - Get all books
- `GET /books/{id}` - Get book by ID

### Members
- `POST /members/` - Create a new member
- `GET /members/` - Get all members
- `GET /members/{id}` - Get member by ID

### Libraries
- `POST /libraries/` - Create a new library
- `GET /libraries/` - Get all libraries
- `GET /libraries/{id}` - Get library by ID

### Borrow Records
- `POST /borrow-records/` - Create a borrow record
- `GET /borrow-records/` - Get all borrow records
- `GET /borrow-records/{id}` - Get borrow record by ID
- `PUT /borrow-records/{id}/return` - Mark book as returned

## Database Models

- **Library**: Name and city information
- **Book**: Title, author, ISBN, available copies
- **Member**: Name and email
- **BorrowRecord**: Links books, members, and libraries with borrow/return dates and status
