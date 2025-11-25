"""
Library Management System
A comprehensive system to manage books, members, and borrowing operations
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class Book:
    """Represents a book in the library"""
    def __init__(self, book_id: str, title: str, author: str, isbn: str, copies: int = 1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_by = []  # List of member IDs who borrowed this book
    
    def __str__(self):
        return f"[{self.book_id}] {self.title} by {self.author} (Available: {self.available_copies}/{self.total_copies})"
    
    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'borrowed_by': self.borrowed_by
        }


class Member:
    """Represents a library member"""
    def __init__(self, member_id: str, name: str, email: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []  # List of (book_id, borrow_date, due_date)
        self.join_date = datetime.now()
    
    def __str__(self):
        return f"[{self.member_id}] {self.name} - {self.email} (Borrowed: {len(self.borrowed_books)})"
    
    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'join_date': self.join_date.isoformat(),
            'borrowed_books': self.borrowed_books
        }


class Library:
    """Main Library Management System"""
    def __init__(self, name: str = "Central Library"):
        self.name = name
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.borrow_history: List[Dict] = []
        self.loan_duration_days = 14
    
    # ============ BOOK OPERATIONS ============
    def add_book(self, book_id: str, title: str, author: str, isbn: str, copies: int = 1) -> bool:
        """Add a new book to the library"""
        if book_id in self.books:
            print(f"Error: Book ID '{book_id}' already exists!")
            return False
        self.books[book_id] = Book(book_id, title, author, isbn, copies)
        print(f"✓ Book added: {self.books[book_id]}")
        return True
    
    def search_book_by_title(self, title: str) -> List[Book]:
        """Search books by title (partial match)"""
        results = [book for book in self.books.values() if title.lower() in book.title.lower()]
        return results
    
    def search_book_by_author(self, author: str) -> List[Book]:
        """Search books by author (partial match)"""
        results = [book for book in self.books.values() if author.lower() in book.author.lower()]
        return results
    
    def display_all_books(self):
        """Display all books in the library"""
        if not self.books:
            print("No books in the library.")
            return
        print("\n" + "="*60)
        print(f"{'LIBRARY CATALOG - ' + self.name:^60}")
        print("="*60)
        for book in self.books.values():
            print(book)
        print("="*60 + "\n")
    
    # ============ MEMBER OPERATIONS ============
    def register_member(self, member_id: str, name: str, email: str, phone: str) -> bool:
        """Register a new member"""
        if member_id in self.members:
            print(f"Error: Member ID '{member_id}' already exists!")
            return False
        self.members[member_id] = Member(member_id, name, email, phone)
        print(f"✓ Member registered: {self.members[member_id]}")
        return True
    
    def display_all_members(self):
        """Display all registered members"""
        if not self.members:
            print("No members registered.")
            return
        print("\n" + "="*60)
        print(f"{'REGISTERED MEMBERS':^60}")
        print("="*60)
        for member in self.members.values():
            print(member)
        print("="*60 + "\n")
    
    def get_member(self, member_id: str) -> Optional[Member]:
        """Get member by ID"""
        return self.members.get(member_id)
    
    # ============ BORROWING OPERATIONS ============
    def borrow_book(self, member_id: str, book_id: str) -> bool:
        """Member borrows a book"""
        if member_id not in self.members:
            print(f"Error: Member '{member_id}' not found!")
            return False
        
        if book_id not in self.books:
            print(f"Error: Book '{book_id}' not found!")
            return False
        
        book = self.books[book_id]
        member = self.members[member_id]
        
        if book.available_copies <= 0:
            print(f"Error: No copies of '{book.title}' available!")
            return False
        
        # Check if member already has this book
        for borrowed in member.borrowed_books:
            if borrowed['book_id'] == book_id:
                print(f"Error: Member already has a copy of '{book.title}'!")
                return False
        
        # Process borrowing
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=self.loan_duration_days)
        
        book.available_copies -= 1
        book.borrowed_by.append(member_id)
        
        borrow_record = {
            'book_id': book_id,
            'borrow_date': borrow_date.isoformat(),
            'due_date': due_date.isoformat(),
            'returned': False
        }
        member.borrowed_books.append(borrow_record)
        
        self.borrow_history.append({
            'action': 'borrow',
            'member_id': member_id,
            'book_id': book_id,
            'date': borrow_date.isoformat()
        })
        
        print(f"✓ {member.name} borrowed '{book.title}'")
        print(f"  Due date: {due_date.strftime('%Y-%m-%d')}")
        return True
    
    def return_book(self, member_id: str, book_id: str) -> bool:
        """Member returns a borrowed book"""
        if member_id not in self.members:
            print(f"Error: Member '{member_id}' not found!")
            return False
        
        if book_id not in self.books:
            print(f"Error: Book '{book_id}' not found!")
            return False
        
        member = self.members[member_id]
        book = self.books[book_id]
        
        # Find the borrowed book record
        borrow_record = None
        for record in member.borrowed_books:
            if record['book_id'] == book_id and not record['returned']:
                borrow_record = record
                break
        
        if not borrow_record:
            print(f"Error: {member.name} hasn't borrowed '{book.title}'!")
            return False
        
        # Process return
        book.available_copies += 1
        if member_id in book.borrowed_by:
            book.borrowed_by.remove(member_id)
        borrow_record['returned'] = True
        borrow_record['return_date'] = datetime.now().isoformat()
        
        # Check for overdue
        due_date = datetime.fromisoformat(borrow_record['due_date'])
        if datetime.now() > due_date:
            days_overdue = (datetime.now() - due_date).days
            print(f"⚠ Book returned {days_overdue} days late!")
        
        self.borrow_history.append({
            'action': 'return',
            'member_id': member_id,
            'book_id': book_id,
            'date': datetime.now().isoformat()
        })
        
        print(f"✓ {member.name} returned '{book.title}'")
        return True
    
    # ============ REPORTING ============
    def display_member_borrowed_books(self, member_id: str):
        """Display books currently borrowed by a member"""
        if member_id not in self.members:
            print(f"Error: Member '{member_id}' not found!")
            return
        
        member = self.members[member_id]
        active_borrows = [b for b in member.borrowed_books if not b['returned']]
        
        print(f"\n{'Books borrowed by ' + member.name:^60}")
        if not active_borrows:
            print("  No active borrowings")
        else:
            for borrow in active_borrows:
                book = self.books[borrow['book_id']]
                due_date = datetime.fromisoformat(borrow['due_date'])
                status = "📅 Due"
                if datetime.now() > due_date:
                    days = (datetime.now() - due_date).days
                    status = f"🔴 OVERDUE ({days} days)"
                print(f"  • {book.title} - {status}: {due_date.strftime('%Y-%m-%d')}")
        print()
    
    def check_overdue_books(self) -> List[Dict]:
        """Find all overdue books"""
        overdue = []
        for member_id, member in self.members.items():
            for borrow in member.borrowed_books:
                if not borrow['returned']:
                    due_date = datetime.fromisoformat(borrow['due_date'])
                    if datetime.now() > due_date:
                        book = self.books[borrow['book_id']]
                        days_overdue = (datetime.now() - due_date).days
                        overdue.append({
                            'member': member.name,
                            'book': book.title,
                            'days_overdue': days_overdue,
                            'due_date': due_date.isoformat()
                        })
        return overdue
    
    def display_overdue_report(self):
        """Display overdue books report"""
        overdue = self.check_overdue_books()
        print("\n" + "="*60)
        print(f"{'OVERDUE BOOKS REPORT':^60}")
        print("="*60)
        if not overdue:
            print("No overdue books!")
        else:
            for item in overdue:
                print(f"👤 {item['member']}")
                print(f"   📚 {item['book']}")
                print(f"   ⏰ {item['days_overdue']} days overdue (Due: {item['due_date'][:10]})")
                print()
        print("="*60 + "\n")
    
    def get_library_stats(self) -> Dict:
        """Get library statistics"""
        total_books = sum(book.total_copies for book in self.books.values())
        available_books = sum(book.available_copies for book in self.books.values())
        borrowed_books = total_books - available_books
        
        return {
            'total_book_titles': len(self.books),
            'total_copies': total_books,
            'available_copies': available_books,
            'borrowed_copies': borrowed_books,
            'total_members': len(self.members),
            'overdue_count': len(self.check_overdue_books())
        }
    
    def display_statistics(self):
        """Display library statistics"""
        stats = self.get_library_stats()
        print("\n" + "="*60)
        print(f"{'LIBRARY STATISTICS':^60}")
        print("="*60)
        print(f"Total Book Titles:    {stats['total_book_titles']}")
        print(f"Total Copies:         {stats['total_copies']}")
        print(f"Available Copies:     {stats['available_copies']}")
        print(f"Borrowed Copies:      {stats['borrowed_copies']}")
        print(f"Total Members:        {stats['total_members']}")
        print(f"Overdue Books:        {stats['overdue_count']}")
        print("="*60 + "\n")
    
    # ============ FILE OPERATIONS ============
    def save_to_file(self, filename: str = "library_data.json"):
        """Save library data to JSON file"""
        data = {
            'name': self.name,
            'books': {bid: book.to_dict() for bid, book in self.books.items()},
            'members': {mid: member.to_dict() for mid, member in self.members.items()},
            'borrow_history': self.borrow_history,
            'loan_duration_days': self.loan_duration_days
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Library data saved to {filename}")
    
    def load_from_file(self, filename: str = "library_data.json"):
        """Load library data from JSON file"""
        if not os.path.exists(filename):
            print(f"File {filename} not found!")
            return False
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.name = data.get('name', 'Central Library')
        self.loan_duration_days = data.get('loan_duration_days', 14)
        
        # Load books
        for book_data in data.get('books', {}).values():
            book = Book(book_data['book_id'], book_data['title'], 
                       book_data['author'], book_data['isbn'], book_data['total_copies'])
            book.available_copies = book_data['available_copies']
            book.borrowed_by = book_data['borrowed_by']
            self.books[book.book_id] = book
        
        # Load members
        for member_data in data.get('members', {}).values():
            member = Member(member_data['member_id'], member_data['name'],
                          member_data['email'], member_data['phone'])
            member.join_date = datetime.fromisoformat(member_data['join_date'])
            member.borrowed_books = member_data['borrowed_books']
            self.members[member.member_id] = member
        
        self.borrow_history = data.get('borrow_history', [])
        print(f"✓ Library data loaded from {filename}")
        return True


# ============ DEMO & USAGE ============
def main():
    """Demonstration of the Library Management System"""
    
    # Create library
    library = Library("City Public Library")
    
    print("\n" + "="*60)
    print(f"{'LIBRARY MANAGEMENT SYSTEM':^60}")
    print("="*60 + "\n")
    
    # Add sample books
    print("📚 Adding books to the library...")
    library.add_book("B001", "The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 2)
    library.add_book("B002", "To Kill a Mockingbird", "Harper Lee", "978-0061120084", 3)
    library.add_book("B003", "1984", "George Orwell", "978-0451524935", 2)
    library.add_book("B004", "Pride and Prejudice", "Jane Austen", "978-0141439518", 2)
    library.add_book("B005", "The Catcher in the Rye", "J.D. Salinger", "978-0316769174", 1)
    
    # Register members
    print("\n👥 Registering members...")
    library.register_member("M001", "Alice Johnson", "alice@email.com", "555-0101")
    library.register_member("M002", "Bob Smith", "bob@email.com", "555-0102")
    library.register_member("M003", "Carol White", "carol@email.com", "555-0103")
    
    # Display catalog
    library.display_all_books()
    
    # Display members
    library.display_all_members()
    
    # Borrow books
    print("📖 Members borrowing books...")
    library.borrow_book("M001", "B001")
    library.borrow_book("M001", "B003")
    library.borrow_book("M002", "B002")
    library.borrow_book("M003", "B004")
    
    # Display member's borrowed books
    library.display_member_borrowed_books("M001")
    
    # Return a book
    print("🔄 Returning a book...")
    library.return_book("M001", "B001")
    
    # Display statistics
    library.display_statistics()
    
    # Search functionality
    print("🔍 Searching for books by author 'Jane Austen':")
    results = library.search_book_by_author("Jane Austen")
    for book in results:
        print(f"  {book}")
    
    # Save data
    print("\n💾 Saving library data...")
    library.save_to_file("library_data.json")


if __name__ == "__main__":
    main()
