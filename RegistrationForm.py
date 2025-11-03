import tkinter as tk
from tkinter import messagebox



class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Membership Registration Form")

        tk.Label(root, text="Member Number:").grid(row=0, column=0, padx=10, pady=5)
        self.member_number = tk.Entry(root)
        self.member_number.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="First Name:").grid(row=1, column=0, padx=10, pady=5)
        self.first_name = tk.Entry(root)
        self.first_name.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
        self.last_name = tk.Entry(root)
        self.last_name.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Email:").grid(row=3, column=0, padx=10, pady=5)
        self.email = tk.Entry(root)
        self.email.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Phone:").grid(row=4, column=0, padx=10, pady=5)
        self.phone = tk.Entry(root)
        self.phone.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(root, text="Address:").grid(row=5, column=0, padx=10, pady=5)
        self.address = tk.Entry(root)
        self.address.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(root, text="Membership Type:").grid(row=6, column=0, padx=10, pady=5)
        self.membership_type = tk.Entry(root)
        self.membership_type.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(root, text="Status:").grid(row=7, column=0, padx=10, pady=5)
        self.status = tk.Entry(root)
        self.status.grid(row=7, column=1, padx=10, pady=5)

        tk.Button(root, text="Register Member", command=self.register_member).grid(row=8, column=1, pady=10)

    def register_member(self):
        member_number = self.member_number.get()
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        email = self.email.get()
        phone = self.phone.get()
        address = self.address.get()
        membership_type = self.membership_type.get()
        status = self.status.get()

        if not all([member_number, first_name, last_name, email]):
            messagebox.showerror("Please fill in all required fields")


root = tk.Tk()
app = RegistrationForm(root)
root.mainloop()