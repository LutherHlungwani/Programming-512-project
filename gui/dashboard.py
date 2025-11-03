import tkinter as tk
from tkinter import ttk
from database.db_manager import get_all_books, get_all_members, get_overdue_transactions, get_recent_transactions, get_popular_books

class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Dashboard", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Stats Frame
        stats_frame = tk.Frame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)

        # Total Books
        total_books = len(get_all_books())
        total_books_label = tk.Label(stats_frame, text=f"Total Books: {total_books}", font=("Arial", 12))
        total_books_label.pack(side="left", padx=20)

        # Total Members
        total_members = len(get_all_members())
        total_members_label = tk.Label(stats_frame, text=f"Total Members: {total_members}", font=("Arial", 12))
        total_members_label.pack(side="left", padx=20)

        # Overdue Books
        overdue_count = len(get_overdue_transactions())
        overdue_label = tk.Label(stats_frame, text=f"Overdue Books: {overdue_count}", font=("Arial", 12))
        overdue_label.pack(side="left", padx=20)

        # Recent Transactions
        recent_frame = tk.LabelFrame(self, text="Recent Transactions", font=("Arial", 12))
        recent_frame.pack(fill="x", padx=20, pady=10)

        recent_tree = ttk.Treeview(recent_frame, columns=("ID", "Member", "Book", "Date", "Status"), show="headings", height=5)
        recent_tree.heading("ID", text="ID")
        recent_tree.heading("Member", text="Member")
        recent_tree.heading("Book", text="Book")
        recent_tree.heading("Date", text="Date")
        recent_tree.heading("Status", text="Status")

        for trans in get_recent_transactions():
            recent_tree.insert("", "end", values=trans)

        scrollbar_recent = ttk.Scrollbar(recent_frame, orient="vertical", command=recent_tree.yview)
        recent_tree.configure(yscrollcommand=scrollbar_recent.set)
        recent_tree.pack(side="left", fill="both", expand=True)
        scrollbar_recent.pack(side="right", fill="y")

        # Popular Books
        popular_frame = tk.LabelFrame(self, text="Popular Books", font=("Arial", 12))
        popular_frame.pack(fill="x", padx=20, pady=10)

        popular_tree = ttk.Treeview(popular_frame, columns=("Title", "Times Borrowed"), show="headings", height=5)
        popular_tree.heading("Title", text="Title")
        popular_tree.heading("Times Borrowed", text="Times Borrowed")

        for book in get_popular_books():
            popular_tree.insert("", "end", values=book)

        scrollbar_popular = ttk.Scrollbar(popular_frame, orient="vertical", command=popular_tree.yview)
        popular_tree.configure(yscrollcommand=scrollbar_popular.set)
        popular_tree.pack(side="left", fill="both", expand=True)
        scrollbar_popular.pack(side="right", fill="y")