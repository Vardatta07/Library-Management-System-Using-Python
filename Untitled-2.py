import tkinter as tk
from tkinter import messagebox, simpledialog

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")
        
        # In-memory storage for 
        #         self.books = []
        
        # Main frame for better organization
        main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label with styling
        self.title_label = tk.Label(main_frame, text="Library Management System", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)
        
        # Button frame for grouping buttons
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Styled buttons
        button_style = {"font": ("Arial", 10), "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED, "bd": 2, "width": 15}
        
        self.add_button = tk.Button(button_frame, text="Add Book", command=self.add_book, **button_style)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.remove_button = tk.Button(button_frame, text="Remove Book", command=self.remove_book, **button_style)
        self.remove_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.search_button = tk.Button(button_frame, text="Search Book", command=self.search_book, **button_style)
        self.search_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.display_button = tk.Button(button_frame, text="Display All Books", command=self.display_books, **button_style)
        self.display_button.grid(row=1, column=1, padx=5, pady=5)
        
        self.borrow_button = tk.Button(button_frame, text="Borrow Book", command=self.borrow_book, **button_style)
        self.borrow_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.return_button = tk.Button(button_frame, text="Return Book", command=self.return_book, **button_style)
        self.return_button.grid(row=2, column=1, padx=5, pady=5)
        
        self.quit_button = tk.Button(button_frame, text="Quit", command=root.quit, bg="#f44336", fg="white", font=("Arial", 10), relief=tk.RAISED, bd=2, width=15)
        self.quit_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Text area with styling
        self.text_area = tk.Text(main_frame, height=12, width=80, font=("Courier", 10), bg="#ffffff", fg="#333", relief=tk.SUNKEN, bd=2)
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
