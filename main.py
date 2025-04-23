import json
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table

# Initialize colorama
init()

class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self): 
        """Initialize a new book collection with an empty list and set up file storage."""
        self.book_list = []
        self.storage_file = "books_data.json"
        self.console = Console()
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory."""
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        """Store the current book collection to a JSON file for permanent storage."""
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def create_new_book(self):
        """Add a new book to the collection by gathering information from the user."""
        self.console.print("\n[bold cyan]Add New Book[/bold cyan]")
        book_title = input(f"{Fore.CYAN}Enter book title: {Style.RESET_ALL}")
        book_author = input(f"{Fore.CYAN}Enter author: {Style.RESET_ALL}")
        publication_year = input(f"{Fore.CYAN}Enter publication year: {Style.RESET_ALL}")
        book_genre = input(f"{Fore.CYAN}Enter genre: {Style.RESET_ALL}")
        is_book_read = input(f"{Fore.CYAN}Have you read this book? (yes/no): {Style.RESET_ALL}").strip().lower() == "yes"

        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
        }

        self.book_list.append(new_book)
        self.save_to_file()
        self.console.print("[bold green]Book added successfully![/bold green]\n")

    def delete_book(self):
        """Remove a book from the collection using its title."""
        self.console.print("\n[bold red]Delete Book[/bold red]")
        book_title = input(f"{Fore.RED}Enter the title of the book to remove: {Style.RESET_ALL}")

        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                self.book_list.remove(book)
                self.save_to_file()
                self.console.print("[bold green]Book removed successfully![/bold green]\n")
                return
        self.console.print("[bold red]Book not found![/bold red]\n")

    def find_book(self):
        """Search for books in the collection by title or author name."""
        self.console.print("\n[bold yellow]Search Books[/bold yellow]")
        search_type = input(f"{Fore.YELLOW}Search by:\n1. Title\n2. Author\nEnter your choice: {Style.RESET_ALL}")
        search_text = input(f"{Fore.YELLOW}Enter search term: {Style.RESET_ALL}").lower()
        found_books = [
            book
            for book in self.book_list
            if search_text in book["title"].lower()
            or search_text in book["author"].lower()
        ]

        if found_books:
            table = Table(title="Matching Books")
            table.add_column("No.", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Author", style="green")
            table.add_column("Year", style="blue")
            table.add_column("Genre", style="yellow")
            table.add_column("Status", style="red")

            for index, book in enumerate(found_books, 1):
                reading_status = "Read" if book["read"] else "Unread"
                table.add_row(
                    str(index),
                    book["title"],
                    book["author"],
                    book["year"],
                    book["genre"],
                    reading_status
                )
            self.console.print(table)
        else:
            self.console.print("[bold red]No matching books found.[/bold red]\n")

    def update_book(self):
        """Modify the details of an existing book in the collection."""
        self.console.print("\n[bold blue]Update Book[/bold blue]")
        book_title = input(f"{Fore.BLUE}Enter the title of the book you want to edit: {Style.RESET_ALL}")
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                self.console.print("[bold yellow]Leave blank to keep existing value.[/bold yellow]")
                book["title"] = input(f"{Fore.BLUE}New title ({book['title']}): {Style.RESET_ALL}") or book["title"]
                book["author"] = input(f"{Fore.BLUE}New author ({book['author']}): {Style.RESET_ALL}") or book["author"]
                book["year"] = input(f"{Fore.BLUE}New year ({book['year']}): {Style.RESET_ALL}") or book["year"]
                book["genre"] = input(f"{Fore.BLUE}New genre ({book['genre']}): {Style.RESET_ALL}") or book["genre"]
                book["read"] = input(f"{Fore.BLUE}Have you read this book? (yes/no): {Style.RESET_ALL}").strip().lower() == "yes"
                self.save_to_file()
                self.console.print("[bold green]Book updated successfully![/bold green]\n")
                return
        self.console.print("[bold red]Book not found![/bold red]\n")

    def show_all_books(self):
        """Display all books in the collection with their details."""
        if not self.book_list:
            self.console.print("[bold red]Your collection is empty.[/bold red]\n")
            return

        table = Table(title="Your Book Collection")
        table.add_column("No.", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Year", style="blue")
        table.add_column("Genre", style="yellow")
        table.add_column("Status", style="red")

        for index, book in enumerate(self.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            table.add_row(
                str(index),
                book["title"],
                book["author"],
                book["year"],
                book["genre"],
                reading_status
            )
        self.console.print(table)
        print()

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        
        self.console.print("\n[bold cyan]Reading Progress[/bold cyan]")
        self.console.print(f"[bold]Total books in collection:[/bold] {total_books}")
        self.console.print(f"[bold]Books read:[/bold] {completed_books}")
        self.console.print(f"[bold]Reading progress:[/bold] {completion_rate:.2f}%\n")

    def start_application(self):
        """Run the main application loop with a user-friendly menu interface."""
        while True:
            self.console.print("[bold magenta]📚 Welcome to Your Book Collection Manager! 📚[/bold magenta]")
            self.console.print("[cyan]1.[/cyan] Add a new book")
            self.console.print("[cyan]2.[/cyan] Remove a book")
            self.console.print("[cyan]3.[/cyan] Search for books")
            self.console.print("[cyan]4.[/cyan] Update book details")
            self.console.print("[cyan]5.[/cyan] View all books")
            self.console.print("[cyan]6.[/cyan] View reading progress")
            self.console.print("[cyan]7.[/cyan] Exit")
            
            user_choice = input(f"{Fore.CYAN}Please choose an option (1-7): {Style.RESET_ALL}")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.save_to_file()
                self.console.print("[bold green]Thank you for using Book Collection Manager. Goodbye![/bold green]")
                break
            else:
                self.console.print("[bold red]Invalid choice. Please try again.[/bold red]\n")


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()