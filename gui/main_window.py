import tkinter as tk
from tkinter import ttk
from gui.dashboard import DashboardFrame
from gui.book_management import BookManagementFrame
from gui.member_management import MemberManagementFrame
from gui.transaction_ui import TransactionFrame


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x700")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create frames
        self.dashboard_frame = DashboardFrame(self.notebook)
        self.book_frame = BookManagementFrame(self.notebook)
        self.member_frame = MemberManagementFrame(self.notebook)
        self.transaction_frame = TransactionFrame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.book_frame, text="Books")
        self.notebook.add(self.member_frame, text="Members")
        self.notebook.add(self.transaction_frame, text="Transactions")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()