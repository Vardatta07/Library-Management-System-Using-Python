import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#e8f4f8")  # Light blue background for a library theme
        
        # In-memory storage for books: list of dicts with title, author, available status
        self.books = []
        
        # Style configuration for ttk widgets
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TLabel", font=("Arial", 12), background="#e8f4f8")
        style.configure("Header.TLabel", font=("Arial", 20, "bold"), foreground="#2c3e50", background="#e8f4f8")
        
        # Main container
        main_frame = tk.Frame(root, bg="#e8f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg="#3498db", height=100)  # Blue header
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        logo_label = ttk.Label(header_frame, text="📚 Library Management System", style="Header.TLabel")
        logo_label.pack(pady=30)
        
        # Content frame (split into sidebar and main area)
        content_frame = tk.Frame(main_frame, bg="#e8f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar for buttons
        sidebar_frame = tk.Frame(content_frame, bg="#bdc3c7", width=200)  # Gray sidebar
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)
        
        sidebar_title = ttk.Label(sidebar_frame, text="Menu", font=("Arial", 14, "bold"))
        sidebar_title.pack(pady=10)
        
        self.add_button = ttk.Button(sidebar_frame, text="➕ Add Book", command=self.add_book)
        self.add_button.pack(pady=5, fill=tk.X, padx=10)
        
        self.remove_button = ttk.Button(sidebar_frame, text="➖ Remove Book", command=self.remove_book)
        self.remove_button.pack(pady=5, fill=tk.X, padx=10)
        
        self.search_button = ttk.Button(sidebar_frame, text="🔍 Search Book", command=self.search_book)
        self.search_button.pack(pady=5, fill=tk.X, padx=10)
        
        self.display_button = ttk.Button(sidebar_frame, text="📋 Display All", command=self.display_books)
        self.display_button.pack(pady=5, fill=tk.X, padx=10)
        
        self.borrow_button = ttk.Button(sidebar_frame, text="📖 Borrow Book", command=self.borrow_book)
        self.borrow_button.pack(pady=5, fill=tk.X, padx=10)
        
        self.return_button = ttk.Button(sidebar_frame, text="🔄 Return Book", command=self.return_book)
        self.return_button.pack(pady=5, fill=tk.X, padx=10)
        
        self.quit_button = ttk.Button(sidebar_frame, text="❌ Quit", command=root.quit)
        self.quit_button.pack(pady=20, fill=tk.X, padx=10)
        
        # Main display area
        display_frame = tk.Frame(content_frame, bg="#e8f4f8")
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        display_title = ttk.Label(display_frame, text="Book List & Details")
        display_title.pack(pady=5)
        
        # Text area with scrollbar
        text_frame = tk.Frame(display_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        self.text_area = tk.Text(text_frame, height=15, width=60, font=("Courier", 10), bg="#ffffff", fg="#2c3e50", relief=tk.SUNKEN, bd=2)
        scrollbar = tk.Scrollbar(text_frame, command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Footer status bar
        footer_frame = tk.Frame(main_frame, bg="#34495e", height=30)  # Dark blue footer
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        self.status_label = ttk.Label(footer_frame, text="Ready. Total books: 0", foreground="white", background="#34495e")
        self.status_label.pack(pady=5)
        
        # Update status on init
        self.update_status()
    
    def update_status(self):
        self.status_label.config(text=f"Ready. Total books: {len(self.books)}")
    
    def add_book(self):
        title = simpledialog.askstring("Add Book", "Enter book title:")
        author = simpledialog.askstring("Add Book", "Enter author name:")
        if title and author:
            self.books.append({"title": title, "author": author, "available": True})
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.update_status()
        else:
            messagebox.showerror("Error", "Title and author are required.")
    
    def remove_book(self):
        title = simpledialog.askstring("Remove Book", "Enter book title to remove:")
        if title:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    self.books.remove(book)
                    messagebox.showinfo("Success", f"Book '{title}' removed successfully!")
                    self.update_status()
                    return
            messagebox.showerror("Error", f"Book '{title}' not found.")
        else:
            messagebox.showerror("Error", "Title is required.")
    
    def search_book(self):
        title = simpledialog.askstring("Search Book", "Enter book title to search:")
        if title:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    status = "Available" if book["available"] else "Borrowed"
                    messagebox.showinfo("Book Found", f"Title: {book['title']}\nAuthor: {book['author']}\nStatus: {status}")
                    return
            messagebox.showerror("Error", f"Book '{title}' not found.")
        else:
            messagebox.showerror("Error", "Title is required.")
    
    def display_books(self):
        self.text_area.delete(1.0, tk.END)
        if not self.books:
            self.text_area.insert(tk.END, "No books in the library.\n")
        else:
            for book in self.books:
                status = "Available" if book["available"] else "Borrowed"
                self.text_area.insert(tk.END, f"📖 Title: {book['title']}, Author: {book['author']}, Status: {status}\n")
    
    def borrow_book(self):
        title = simpledialog.askstring("Borrow Book", "Enter book title to borrow:")
        if title:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    if book["available"]:
                        book["available"] = False
                        messagebox.showinfo("Success", f"Book '{title}' borrowed successfully!")
                        self.update_status()
                    else:
                        messagebox.showerror("Error", f"Book '{title}' is already borrowed.")
                    return
            messagebox.showerror("Error", f"Book '{title}' not found.")
        else:
            messagebox.showerror("Error", "Title is required.")
    
    def return_book(self):
        title = simpledialog.askstring("Return Book", "Enter book title to return:")
        if title:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    if not book["available"]:
                        book["available"] = True
                        messagebox.showinfo("Success", f"Book '{title}' returned successfully!")
                        self.update_status()
                    else:
                        messagebox.showerror("Error", f"Book '{title}' was not borrowed.")
                    return
            messagebox.showerror("Error", f"Book '{title}' not found.")
        else:
            messagebox.showerror("Error", "Title is required.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
