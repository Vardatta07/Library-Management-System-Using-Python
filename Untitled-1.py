import tkinter as tk
from tkinter import messagebox, simpledialog

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")
        
        # In-memory storage for books: list of dicts with title, author, available status
        self.books = []
        
        # GUI Elements
        self.title_label = tk.Label(root, text="Library Management System", font=("Arial", 16))
        self.title_label.pack(pady=10)
        
        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.add_button.pack(pady=5)
        
        self.remove_button = tk.Button(root, text="Remove Book", command=self.remove_book)
        self.remove_button.pack(pady=5)
        
        self.search_button = tk.Button(root, text="Search Book", command=self.search_book)
        self.search_button.pack(pady=5)
        
        self.display_button = tk.Button(root, text="Display All Books", command=self.display_books)
        self.display_button.pack(pady=5)
        
        self.borrow_button = tk.Button(root, text="Borrow Book", command=self.borrow_book)
        self.borrow_button.pack(pady=5)
        
        self.return_button = tk.Button(root, text="Return Book", command=self.return_book)
        self.return_button.pack(pady=5)
        
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=5)
        
        # Text area for displaying results
        self.text_area = tk.Text(root, height=10, width=70)
        self.text_area.pack(pady=10)
    
    def add_book(self):
        title = simpledialog.askstring("Add Book", "Enter book title:")
        author = simpledialog.askstring("Add Book", "Enter author name:")
        if title and author:
            self.books.append({"title": title, "author": author, "available": True})
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        else:
            messagebox.showerror("Error", "Title and author are required.")
    
    def remove_book(self):
        title = simpledialog.askstring("Remove Book", "Enter book title to remove:")
        if title:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    self.books.remove(book)
                    messagebox.showinfo("Success", f"Book '{title}' removed successfully!")
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
                self.text_area.insert(tk.END, f"Title: {book['title']}, Author: {book['author']}, Status: {status}\n")
    
    def borrow_book(self):
        title = simpledialog.askstring("Borrow Book", "Enter book title to borrow:")
        if title:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    if book["available"]:
                        book["available"] = False
                        messagebox.showinfo("Success", f"Book '{title}' borrowed successfully!")
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
