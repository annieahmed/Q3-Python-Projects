import streamlit as st
import json
from rich.console import Console
from rich.table import Table
import re

class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self): 
        """Initialize a new book collection with an empty list and set up file storage."""
        if 'book_list' not in st.session_state:
            st.session_state.book_list = []
        self.storage_file = "books_data.json"
        self.console = Console()
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory."""
        try:
            with open(self.storage_file, "r") as file:
                st.session_state.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            st.session_state.book_list = []

    def save_to_file(self):
        """Store the current book collection to a JSON file for permanent storage."""
        with open(self.storage_file, "w") as file:
            json.dump(st.session_state.book_list, file, indent=4)

    def validate_year(self, year):
        """Validate the publication year format."""
        if not year.isdigit():
            return False
        year = int(year)
        return 1000 <= year <= 2100

    def create_new_book(self):
        """Add a new book to the collection by gathering information from the user."""
        st.subheader("Add New Book")
        col1, col2 = st.columns(2)
        
        with col1:
            book_title = st.text_input("Book Title")
            book_author = st.text_input("Author")
            publication_year = st.text_input("Publication Year")
        
        with col2:
            book_genre = st.text_input("Genre")
            is_book_read = st.checkbox("I have read this book")

        if st.button("Add Book"):
            with st.spinner("Adding book..."):
                if not all([book_title, book_author, publication_year, book_genre]):
                    st.error("Please fill in all fields!")
                    return
                
                if not self.validate_year(publication_year):
                    st.error("Please enter a valid year between 1000 and 2100")
                    return

                new_book = {
                    "title": book_title,
                    "author": book_author,
                    "year": publication_year,
                    "genre": book_genre,
                    "read": is_book_read,
                }
                st.session_state.book_list.append(new_book)
                self.save_to_file()
                st.success("Book added successfully!")
                st.balloons()

    def delete_book(self):
        """Remove a book from the collection using its title."""
        st.subheader("Delete Book")
        book_title = st.text_input("Enter the title of the book to remove")
        
        if st.button("Delete"):
            with st.spinner("Deleting book..."):
                for book in st.session_state.book_list:
                    if book["title"].lower() == book_title.lower():
                        st.session_state.book_list.remove(book)
                        self.save_to_file()
                        st.success("Book removed successfully!")
                        return
                st.error("Book not found!")

    def find_book(self):
        """Search for books in the collection by title or author name."""
        st.subheader("Search Books")
        search_type = st.radio("Search by:", ["Title", "Author"])
        search_text = st.text_input("Enter search term").lower()
        
        if st.button("Search"):
            with st.spinner("Searching..."):
                found_books = [
                    book
                    for book in st.session_state.book_list
                    if search_text in book["title"].lower()
                    or search_text in book["author"].lower()
                ]

                if found_books:
                    st.write("Matching Books:")
                    for book in found_books:
                        reading_status = "Read" if book["read"] else "Unread"
                        st.write(f"""
                            **{book['title']}** by {book['author']}  
                            Year: {book['year']} | Genre: {book['genre']} | Status: {reading_status}
                        """)
                else:
                    st.warning("No matching books found.")

    def update_book(self):
        """Modify the details of an existing book in the collection."""
        st.subheader("Update Book")
        book_title = st.text_input("Enter the title of the book you want to edit")
        
        if st.button("Find Book"):
            with st.spinner("Searching..."):
                for book in st.session_state.book_list:
                    if book["title"].lower() == book_title.lower():
                        st.write("Leave blank to keep existing value.")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_title = st.text_input("New title", book["title"])
                            new_author = st.text_input("New author", book["author"])
                            new_year = st.text_input("New year", book["year"])
                        
                        with col2:
                            new_genre = st.text_input("New genre", book["genre"])
                            new_read = st.checkbox("I have read this book", book["read"])

                        if st.button("Update Book"):
                            with st.spinner("Updating..."):
                                if new_year and not self.validate_year(new_year):
                                    st.error("Please enter a valid year between 1000 and 2100")
                                    return

                                book["title"] = new_title or book["title"]
                                book["author"] = new_author or book["author"]
                                book["year"] = new_year or book["year"]
                                book["genre"] = new_genre or book["genre"]
                                book["read"] = new_read
                                self.save_to_file()
                                st.success("Book updated successfully!")
                                st.balloons()
                        return
                st.error("Book not found!")

    def show_all_books(self):
        """Display all books in the collection with their details."""
        st.subheader("Your Book Collection")
        if not st.session_state.book_list:
            st.warning("Your collection is empty.")
            return

        for book in st.session_state.book_list:
            reading_status = "Read" if book["read"] else "Unread"
            st.write(f"""
                **{book['title']}** by {book['author']}  
                Year: {book['year']} | Genre: {book['genre']} | Status: {reading_status}
            """)

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        st.subheader("Reading Progress")
        total_books = len(st.session_state.book_list)
        completed_books = sum(1 for book in st.session_state.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", total_books)
        with col2:
            st.metric("Books Read", completed_books)
        with col3:
            st.metric("Completion Rate", f"{completion_rate:.2f}%")
        
        if total_books > 0:
            st.progress(completion_rate / 100)

def main():
    st.set_page_config(
        page_title="Personal Library Manager",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Personal Library Manager")
    
    # Initialize session state
    if 'book_manager' not in st.session_state:
        st.session_state.book_manager = BookCollection()
    
    book_manager = st.session_state.book_manager
    
    menu = ["Add Book", "Delete Book", "Search Books", "Update Book", "View All Books", "Reading Progress"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add Book":
        book_manager.create_new_book()
    elif choice == "Delete Book":
        book_manager.delete_book()
    elif choice == "Search Books":
        book_manager.find_book()
    elif choice == "Update Book":
        book_manager.update_book()
    elif choice == "View All Books":
        book_manager.show_all_books()
    elif choice == "Reading Progress":
        book_manager.show_reading_progress()

if __name__ == "__main__":
    main()