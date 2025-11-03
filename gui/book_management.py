import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
from database.db_manager import add_book, get_book_by_isbn, get_all_books, update_book, delete_book
from api.google_books import fetch_book_by_isbn as api_fetch
from api.openlibrary_api import fetch_book_by_isbn_openlib
from utils.helpers import is_valid_isbn

class BookManagementFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_book_id = None
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Book Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # ISBN Lookup
        isbn_frame = tk.Frame(self)
        isbn_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(isbn_frame, text="ISBN:").pack(side="left")
        self.isbn_entry = tk.Entry(isbn_frame, width=20)
        self.isbn_entry.pack(side="left", padx=5)
        tk.Button(isbn_frame, text="Lookup", command=self.lookup_isbn).pack(side="left", padx=5)

        # Form Frame
        form_frame = tk.LabelFrame(self, text="Book Details", font=("Arial", 12))
        form_frame.pack(fill="x", padx=20, pady=10)

        # Title
        tk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Author
        tk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.author_entry = tk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        # Publisher
        tk.Label(form_frame, text="Publisher:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.publisher_entry = tk.Entry(form_frame, width=40)
        self.publisher_entry.grid(row=2, column=1, padx=5, pady=2)

        # Publication Year
        tk.Label(form_frame, text="Year:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.year_entry = tk.Entry(form_frame, width=10)
        self.year_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # Category
        tk.Label(form_frame, text="Category:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.category_entry = tk.Entry(form_frame, width=40)
        self.category_entry.grid(row=4, column=1, padx=5, pady=2)

        # Description
        tk.Label(form_frame, text="Description:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.description_text = tk.Text(form_frame, width=40, height=4)
        self.description_text.grid(row=5, column=1, padx=5, pady=2)

        # Cover Image
        tk.Label(form_frame, text="Cover:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.cover_label = tk.Label(form_frame, text="No image", width=100, height=120)
        self.cover_label.grid(row=6, column=1, padx=5, pady=2)

        # Copies
        tk.Label(form_frame, text="Total Copies:").grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.copies_entry = tk.Entry(form_frame, width=10)
        self.copies_entry.grid(row=7, column=1, padx=5, pady=2, sticky="w")

        # Shelf Location
        tk.Label(form_frame, text="Shelf Location:").grid(row=8, column=0, sticky="w", padx=5, pady=2)
        self.shelf_entry = tk.Entry(form_frame, width=40)
        self.shelf_entry.grid(row=8, column=1, padx=5, pady=2)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Book", command=self.add_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Book", command=self.update_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Book", command=self.delete_book).pack(side="left", padx=5)

        # Search
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", self.search_books)
        tk.Button(search_frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)

        # Book List
        list_frame = tk.LabelFrame(self, text="Books", font=("Arial", 12))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.book_tree = ttk.Treeview(list_frame, columns=("ID", "Title", "Author", "Available", "Total"), show="headings", height=10)
        self.book_tree.heading("ID", text="ID")
        self.book_tree.heading("Title", text="Title")
        self.book_tree.heading("Author", text="Author")
        self.book_tree.heading("Available", text="Available")
        self.book_tree.heading("Total", text="Total")

        self.book_tree.bind("<<TreeviewSelect>>", self.on_book_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        self.book_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_book_list()

    def lookup_isbn(self):
        isbn = self.isbn_entry.get().strip()
        if not isbn:
            messagebox.showwarning("Warning", "Please enter an ISBN")
            return

        if not is_valid_isbn(isbn):
            messagebox.showerror("Error", "Invalid ISBN format")
            return

        book_data = api_fetch(isbn)
        if not book_data:
            book_data = fetch_book_by_isbn_openlib(isbn)

        if book_data:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, book_data.get('title', ''))
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, book_data.get('author', ''))
            self.publisher_entry.delete(0, tk.END)
            self.publisher_entry.insert(0, book_data.get('publisher', ''))
            if book_data.get('publication_year'):
                self.year_entry.delete(0, tk.END)
                self.year_entry.insert(0, book_data.get('publication_year'))
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, book_data.get('category', ''))
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, book_data.get('description', ''))
            self.copies_entry.delete(0, tk.END)
            self.copies_entry.insert(0, "1")  # Default
            self.shelf_entry.delete(0, tk.END)
            self.shelf_entry.insert(0, "A-1")  # Default

            # Load cover image
            cover_url = book_data.get('cover_image_url')
            if cover_url:
                try:
                    response = requests.get(cover_url)
                    img_data = Image.open(BytesIO(response.content))
                    img_data = img_data.resize((100, 120), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img_data)
                    self.cover_label.configure(image=photo, text="")
                    self.cover_label.image = photo  # Keep a reference
                except Exception as e:
                    print(f"Error loading image: {e}")
        else:
            messagebox.showerror("Error", "Book not found in API")

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required")
            return

        isbn = self.isbn_entry.get().strip()
        publisher = self.publisher_entry.get().strip()
        year = self.year_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        cover_url = self.cover_label.image if hasattr(self.cover_label, 'image') else ''
        copies = self.copies_entry.get().strip()
        shelf = self.shelf_entry.get().strip()

        try:
            year = int(year) if year else None
            copies = int(copies) if copies else 1
        except ValueError:
            messagebox.showerror("Error", "Year and Copies must be numbers")
            return

        add_book(isbn, title, author, publisher, year, category, description, cover_url, 0, 'English', copies, shelf)
        messagebox.showinfo("Success", "Book added successfully")
        self.clear_form()
        self.refresh_book_list()

    def update_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Warning", "Please select a book to update")
            return

        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required")
            return

        isbn = self.isbn_entry.get().strip()
        publisher = self.publisher_entry.get().strip()
        year = self.year_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        cover_url = self.cover_label.image if hasattr(self.cover_label, 'image') else ''
        copies = self.copies_entry.get().strip()
        shelf = self.shelf_entry.get().strip()

        try:
            year = int(year) if year else None
            copies = int(copies) if copies else 1
        except ValueError:
            messagebox.showerror("Error", "Year and Copies must be numbers")
            return

        update_book(self.selected_book_id, isbn, title, author, publisher, year, category, description, cover_url, 0, 'English', copies, shelf)
        messagebox.showinfo("Success", "Book updated successfully")
        self.clear_form()
        self.refresh_book_list()

    def delete_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            delete_book(self.selected_book_id)
            messagebox.showinfo("Success", "Book deleted successfully")
            self.clear_form()
            self.refresh_book_list()

    def clear_form(self):
        self.isbn_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.publisher_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_text.delete(1.0, tk.END)
        self.copies_entry.delete(0, tk.END)
        self.shelf_entry.delete(0, tk.END)
        self.cover_label.configure(image="", text="No image")
        self.selected_book_id = None

    def refresh_book_list(self):
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for book in get_all_books():
            self.book_tree.insert("", "end", values=book)

    def search_books(self, event):
        query = self.search_var.get().lower()
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for book in get_all_books():
            if query in book[2].lower() or query in book[1].lower():  # Search in title or author
                self.book_tree.insert("", "end", values=book)

    def clear_search(self):
        self.search_var.set("")
        self.refresh_book_list()

    def on_book_select(self, event):
        selected_item = self.book_tree.selection()
        if selected_item:
            item = self.book_tree.item(selected_item)
            values = item['values']
            self.selected_book_id = values[0]
            self.isbn_entry.delete(0, tk.END)
            self.isbn_entry.insert(0, values[1] or "")
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[2])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, values[3])
            self.publisher_entry.delete(0, tk.END)
            self.publisher_entry.insert(0, values[4])
            if values[5]:
                self.year_entry.delete(0, tk.END)
                self.year_entry.insert(0, str(values[5]))
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, values[6])
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, values[7])
            self.copies_entry.delete(0, tk.END)
            self.copies_entry.insert(0, str(values[11]))
            self.shelf_entry.delete(0, tk.END)
            self.shelf_entry.insert(0, values[13])