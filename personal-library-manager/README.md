# Personal Library Manager

A command-line application to manage your personal book collection.

## Features

- Add new books to your collection
- Remove books from your collection
- Search for books by title or author
- Update book details
- View all books in your collection
- Track reading progress
- Persistent storage using JSON

## Installation

1. Clone the repository:
```bash
git clone https://github.com/annieahmed/Q3-Python-Projects.git
cd Q3-Python-Projects/personal-library-manager
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

Run the application:
```bash
python main.py
```

## Features in Detail

1. **Add a new book**
   - Enter book title, author, publication year, genre
   - Mark if you've read the book

2. **Remove a book**
   - Remove books by title

3. **Search for books**
   - Search by title or author
   - Case-insensitive search

4. **Update book details**
   - Modify any book information
   - Keep existing values by leaving fields blank

5. **View all books**
   - See your complete collection
   - View reading status for each book

6. **View reading progress**
   - See total number of books
   - Check completion percentage

## Data Storage

- Books are stored in `books_data.json`
- Data persists between sessions
- Automatic backup of your collection
