import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import add_member, get_all_members, get_member_borrowing_history

class MemberManagementFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_member_id = None
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Member Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Form Frame
        form_frame = tk.LabelFrame(self, text="Member Details", font=("Arial", 12))
        form_frame.pack(fill="x", padx=20, pady=10)

        # Membership Number
        tk.Label(form_frame, text="Membership Number:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.number_entry = tk.Entry(form_frame, width=20)
        self.number_entry.grid(row=0, column=1, padx=5, pady=2)

        # First Name
        tk.Label(form_frame, text="First Name:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.fname_entry = tk.Entry(form_frame, width=20)
        self.fname_entry.grid(row=1, column=1, padx=5, pady=2)

        # Last Name
        tk.Label(form_frame, text="Last Name:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.lname_entry = tk.Entry(form_frame, width=20)
        self.lname_entry.grid(row=2, column=1, padx=5, pady=2)

        # Email
        tk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=3, column=1, padx=5, pady=2)

        # Phone
        tk.Label(form_frame, text="Phone:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.phone_entry = tk.Entry(form_frame, width=20)
        self.phone_entry.grid(row=4, column=1, padx=5, pady=2)

        # Address
        tk.Label(form_frame, text="Address:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.address_entry = tk.Entry(form_frame, width=50)
        self.address_entry.grid(row=5, column=1, padx=5, pady=2)

        # Membership Type
        tk.Label(form_frame, text="Membership Type:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.type_var = tk.StringVar(value="Standard")
        type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, values=["Standard", "Premium", "VIP"], state="readonly", width=17)
        type_combo.grid(row=6, column=1, padx=5, pady=2, sticky="w")

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Register Member", command=self.register_member).pack(side="left", padx=5)

        # Member List
        list_frame = tk.LabelFrame(self, text="Members", font=("Arial", 12))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.member_tree = ttk.Treeview(list_frame, columns=("ID", "Number", "Name", "Email", "Phone", "Type"), show="headings", height=10)
        self.member_tree.heading("ID", text="ID")
        self.member_tree.heading("Number", text="Number")
        self.member_tree.heading("Name", text="Name")
        self.member_tree.heading("Email", text="Email")
        self.member_tree.heading("Phone", text="Phone")
        self.member_tree.heading("Type", text="Type")

        self.member_tree.bind("<<TreeviewSelect>>", self.on_member_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.member_tree.yview)
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        self.member_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Borrowing History
        history_frame = tk.LabelFrame(self, text="Borrowing History", font=("Arial", 12))
        history_frame.pack(fill="x", padx=20, pady=10)

        self.history_tree = ttk.Treeview(history_frame, columns=("Book", "Issue Date", "Due Date", "Return Date", "Fine", "Status"), show="headings", height=5)
        self.history_tree.heading("Book", text="Book")
        self.history_tree.heading("Issue Date", text="Issue Date")
        self.history_tree.heading("Due Date", text="Due Date")
        self.history_tree.heading("Return Date", text="Return Date")
        self.history_tree.heading("Fine", text="Fine")
        self.history_tree.heading("Status", text="Status")

        scrollbar_history = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar_history.set)
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar_history.pack(side="right", fill="y")

        self.refresh_member_list()

    def register_member(self):
        number = self.number_entry.get().strip()
        fname = self.fname_entry.get().strip()
        lname = self.lname_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        mtype = self.type_var.get()

        if not (number and fname and lname and email):
            messagebox.showerror("Error", "Membership number, first name, last name, and email are required")
            return

        add_member(number, fname, lname, email, phone, address, mtype)
        messagebox.showinfo("Success", "Member registered successfully")
        self.clear_form()
        self.refresh_member_list()

    def clear_form(self):
        self.number_entry.delete(0, tk.END)
        self.fname_entry.delete(0, tk.END)
        self.lname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.type_var.set("Standard")

    def refresh_member_list(self):
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)

        for member in get_all_members():
            name = f"{member[2]} {member[3]}"
            self.member_tree.insert("", "end", values=(member[0], member[1], name, member[4], member[5], member[8]))

    def on_member_select(self, event):
        selected_item = self.member_tree.selection()
        if selected_item:
            item = self.member_tree.item(selected_item)
            values = item['values']
            self.selected_member_id = values[0]

            # Refresh borrowing history
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            history = get_member_borrowing_history(self.selected_member_id)
            for record in history:
                self.history_tree.insert("", "end", values=record)