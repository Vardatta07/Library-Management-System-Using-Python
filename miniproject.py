import streamlit as st
import json
import os
from datetime import datetime

# File to store library data
DATA_FILE = 'library_data.json'

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'books': [], 'borrowers': []}

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize data
data = load_data()

# Streamlit app
st.title("Library Management System")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Add Book", "View Books", "Borrow Book", "Return Book", "View Borrowers"])

if menu == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    
    if st.button("Add Book"):
        if title and author and isbn:
            # Check if book already exists
            existing = next((b for b in data['books'] if b['isbn'] == isbn), None)
            if existing:
                existing['quantity'] += quantity
                # also increase the available count when adding copies
                existing['available'] = existing.get('available', 0) + quantity
            else:
                data['books'].append({
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'quantity': quantity,
                    'available': quantity
                })
            save_data(data)
            st.success("Book added successfully!")
        else:
            st.error("Please fill all fields.")

elif menu == "View Books":
    st.header("Book Catalog")
    if data['books']:
        import pandas as pd
        df = pd.DataFrame(data['books'])
        st.dataframe(df)
    else:
        st.info("No books in the library yet.")

elif menu == "Borrow Book":
    st.header("Borrow a Book")
    borrower_name = st.text_input("Borrower Name")
    # List only books that have available copies
    available_books = [b for b in data['books'] if b.get('available', 0) > 0]
    if not available_books:
        st.info("No books available to borrow.")
    else:
        isbn = st.selectbox("Select Book ISBN", [b['isbn'] for b in available_books])

        if st.button("Borrow"):
            if borrower_name and isbn:
                book = next((b for b in data['books'] if b['isbn'] == isbn), None)
                if book and book.get('available', 0) > 0:
                    book['available'] -= 1
                    data['borrowers'].append({
                        'name': borrower_name,
                        'isbn': isbn,
                        'borrow_date': str(datetime.now())
                    })
                    save_data(data)
                    st.success(f"Book borrowed by {borrower_name}!")
                else:
                    st.error("Book not available.")
            else:
                st.error("Please enter borrower name and select a book.")

elif menu == "Return Book":
    st.header("Return a Book")
    borrower_name = st.text_input("Borrower Name")
    isbn = st.text_input("Book ISBN")
    
    if st.button("Return"):
        if borrower_name and isbn:
            borrower = next((b for b in data['borrowers'] if b['name'] == borrower_name and b['isbn'] == isbn), None)
            if borrower:
                book = next((b for b in data['books'] if b['isbn'] == isbn), None)
                if book:
                    book['available'] += 1
                data['borrowers'].remove(borrower)
                save_data(data)
                st.success("Book returned successfully!")
            else:
                st.error("No matching borrow record found.")
        else:
            st.error("Please fill all fields.")

elif menu == "View Borrowers":
    st.header("Current Borrowers")
    if data['borrowers']:
        import pandas as pd
        df = pd.DataFrame(data['borrowers'])
        st.dataframe(df)
    else:
        st.info("No books are currently borrowed.")
