import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database.db_manager import get_all_members, get_all_books, issue_book, return_book, get_all_transactions
from notifications.email_sender import send_due_reminder, send_overdue_notification
from utils.helpers import calculate_fine

class TransactionFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Transaction Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Issue Book Section
        issue_frame = tk.LabelFrame(self, text="Issue Book", font=("Arial", 12))
        issue_frame.pack(fill="x", padx=20, pady=10)

        # Member Selection
        tk.Label(issue_frame, text="Select Member:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.member_var = tk.StringVar()
        self.member_combo = ttk.Combobox(issue_frame, textvariable=self.member_var, state="readonly", width=30)
        self.member_combo.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_member_combo()

        # Book Selection
        tk.Label(issue_frame, text="Select Book:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.book_var = tk.StringVar()
        self.book_combo = ttk.Combobox(issue_frame, textvariable=self.book_var, state="readonly", width=30)
        self.book_combo.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_book_combo()

        # Issue Button
        tk.Button(issue_frame, text="Issue Book", command=self.issue_book).grid(row=2, column=0, columnspan=2, pady=10)

        # Return Book Section
        return_frame = tk.LabelFrame(self, text="Return Book", font=("Arial", 12))
        return_frame.pack(fill="x", padx=20, pady=10)

        # Transaction Selection
        tk.Label(return_frame, text="Select Transaction:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.transaction_var = tk.StringVar()
        self.transaction_combo = ttk.Combobox(return_frame, textvariable=self.transaction_var, state="readonly", width=50)
        self.transaction_combo.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_transaction_combo()

        # Return Button
        tk.Button(return_frame, text="Return Book", command=self.return_book).grid(row=1, column=0, columnspan=2, pady=10)

        # All Transactions
        list_frame = tk.LabelFrame(self, text="All Transactions", font=("Arial", 12))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.transaction_tree = ttk.Treeview(list_frame, columns=("ID", "Member", "Book", "Issue Date", "Due Date", "Return Date", "Fine", "Status"), show="headings", height=10)
        self.transaction_tree.heading("ID", text="ID")
        self.transaction_tree.heading("Member", text="Member")
        self.transaction_tree.heading("Book", text="Book")
        self.transaction_tree.heading("Issue Date", text="Issue Date")
        self.transaction_tree.heading("Due Date", text="Due Date")
        self.transaction_tree.heading("Return Date", text="Return Date")
        self.transaction_tree.heading("Fine", text="Fine")
        self.transaction_tree.heading("Status", text="Status")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        self.transaction_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_transaction_list()

    def refresh_member_combo(self):
        members = get_all_members()
        member_list = [f"{m[1]} - {m[2]} {m[3]}" for m in members]
        self.member_combo['values'] = member_list

    def refresh_book_combo(self):
        books = get_all_books()
        book_list = [f"{b[1]} - {b[2]}" for b in books if b[12] > 0]  # Only available books
        self.book_combo['values'] = book_list

    def refresh_transaction_combo(self):
        transactions = get_all_transactions()
        trans_list = [f"{t[0]} - {t[1]} - {t[2]}" for t in transactions if t[7] == 'Issued']
        self.transaction_combo['values'] = trans_list

    def issue_book(self):
        member_selection = self.member_combo.get()
        book_selection = self.book_combo.get()

        if not (member_selection and book_selection):
            messagebox.showwarning("Warning", "Please select both member and book")
            return

        # Extract IDs from selection strings
        member_id = int(member_selection.split(" - ")[0])
        book_id = int(book_selection.split(" - ")[0])

        success = issue_book(member_id, book_id)
        if success:
            messagebox.showinfo("Success", "Book issued successfully")
            self.refresh_book_combo()
            self.refresh_transaction_combo()
            self.refresh_transaction_list()
        else:
            messagebox.showerror("Error", "Book is not available")

    def return_book(self):
        trans_selection = self.transaction_combo.get()
        if not trans_selection:
            messagebox.showwarning("Warning", "Please select a transaction to return")
            return

        transaction_id = int(trans_selection.split(" - ")[0])
        return_book(transaction_id)
        messagebox.showinfo("Success", "Book returned successfully")
        self.refresh_book_combo()
        self.refresh_transaction_combo()
        self.refresh_transaction_list()

    def refresh_transaction_list(self):
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        for trans in get_all_transactions():
            self.transaction_tree.insert("", "end", values=trans)