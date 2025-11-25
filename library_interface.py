"""
Library Management System - Interactive Menu Interface
"""

from library_management import Library
from datetime import datetime

def display_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print(f"{'LIBRARY MANAGEMENT SYSTEM - MAIN MENU':^60}")
    print("="*60)
    print("1.  Add Book")
    print("2.  View All Books")
    print("3.  Search Book by Title")
    print("4.  Search Book by Author")
    print("5.  Register Member")
    print("6.  View All Members")
    print("7.  Borrow Book")
    print("8.  Return Book")
    print("9.  View Member's Borrowed Books")
    print("10. View Overdue Books")
    print("11. View Library Statistics")
    print("12. Save Data")
    print("13. Load Data")
    print("14. Exit")
    print("="*60)

def add_book(library):
    """Add a new book"""
    print("\n--- Add New Book ---")
    book_id = input("Enter Book ID (e.g., B001): ").strip()
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()
    isbn = input("Enter ISBN: ").strip()
    try:
        copies = int(input("Enter Number of Copies (default 1): ").strip() or "1")
    except ValueError:
        copies = 1
    
    library.add_book(book_id, title, author, isbn, copies)

def search_book_by_title(library):
    """Search books by title"""
    print("\n--- Search Books by Title ---")
    title = input("Enter book title (or part of it): ").strip()
    results = library.search_book_by_title(title)
    
    if results:
        print(f"\nFound {len(results)} book(s):")
        for book in results:
            print(f"  {book}")
    else:
        print("No books found with that title.")

def search_book_by_author(library):
    """Search books by author"""
    print("\n--- Search Books by Author ---")
    author = input("Enter author name (or part of it): ").strip()
    results = library.search_book_by_author(author)
    
    if results:
        print(f"\nFound {len(results)} book(s):")
        for book in results:
            print(f"  {book}")
    else:
        print("No books found by that author.")

def register_member(library):
    """Register a new member"""
    print("\n--- Register New Member ---")
    member_id = input("Enter Member ID (e.g., M001): ").strip()
    name = input("Enter Member Name: ").strip()
    email = input("Enter Email: ").strip()
    phone = input("Enter Phone Number: ").strip()
    
    library.register_member(member_id, name, email, phone)

def borrow_book(library):
    """Member borrows a book"""
    print("\n--- Borrow Book ---")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()
    
    library.borrow_book(member_id, book_id)

def return_book(library):
    """Member returns a book"""
    print("\n--- Return Book ---")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()
    
    library.return_book(member_id, book_id)

def view_member_books(library):
    """View books borrowed by a member"""
    print("\n--- View Member's Borrowed Books ---")
    member_id = input("Enter Member ID: ").strip()
    
    library.display_member_borrowed_books(member_id)

def main():
    """Main interactive menu loop"""
    library = Library("City Public Library")
    
    # Try to load existing data
    try:
        library.load_from_file("library_data.json")
    except:
        print("Starting with empty library...")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-14): ").strip()
        
        if choice == "1":
            add_book(library)
        elif choice == "2":
            library.display_all_books()
        elif choice == "3":
            search_book_by_title(library)
        elif choice == "4":
            search_book_by_author(library)
        elif choice == "5":
            register_member(library)
        elif choice == "6":
            library.display_all_members()
        elif choice == "7":
            borrow_book(library)
        elif choice == "8":
            return_book(library)
        elif choice == "9":
            view_member_books(library)
        elif choice == "10":
            library.display_overdue_report()
        elif choice == "11":
            library.display_statistics()
        elif choice == "12":
            filename = input("Enter filename to save (default: library_data.json): ").strip() or "library_data.json"
            library.save_to_file(filename)
        elif choice == "13":
            filename = input("Enter filename to load (default: library_data.json): ").strip() or "library_data.json"
            library.load_from_file(filename)
        elif choice == "14":
            save_choice = input("Save data before exiting? (y/n): ").strip().lower()
            if save_choice == 'y':
                library.save_to_file("library_data.json")
            print("\nThank you for using Library Management System!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 14.")

if __name__ == "__main__":
    main()
