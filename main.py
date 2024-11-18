import tkinter as tk
from tkinter import messagebox
import json
from user import User
from outpass import Outpass

# Helper Functions
def load_users():
    with open('database.json') as file:
        data = json.load(file)
        return data['users']

def login():
    user_id = entry_user_id.get()
    password = entry_password.get()
    users = load_users()

    for user in users:
        if user['user_id'] == user_id and user['password'] == password:
            messagebox.showinfo("Login Success", f"Welcome, {user['name']}!")
            if user['role'] == "student":
                student_window(user)
            elif user['role'] == "staff":
                messagebox.showinfo("Info", "Staff functionalities are under development.")
            elif user['role'] == "admin":
                messagebox.showinfo("Info", "Admin functionalities are under development.")
            return

    messagebox.showerror("Error", "Invalid User ID or Password.")

def register():
    user_id = entry_user_id.get()
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()
    role = var_role.get()

    User.register(user_id, name, email, role, password)
    messagebox.showinfo("Registration Success", "You have registered successfully!")

def student_window(user):
    def apply_outpass():
        date = entry_date.get()
        time = entry_time.get()
        reason = entry_reason.get()

        outpass = Outpass(user['user_id'], date, time, reason)
        outpass.save_outpass()
        messagebox.showinfo("Success", "Outpass request submitted!")

    student_root = tk.Toplevel(root)
    student_root.title("Student Dashboard")

    tk.Label(student_root, text="Apply for Outpass").pack()
    tk.Label(student_root, text="Date (YYYY-MM-DD):").pack()
    entry_date = tk.Entry(student_root)
    entry_date.pack()

    tk.Label(student_root, text="Time (HH:MM):").pack()
    entry_time = tk.Entry(student_root)
    entry_time.pack()

    tk.Label(student_root, text="Reason:").pack()
    entry_reason = tk.Entry(student_root)
    entry_reason.pack()

    tk.Button(student_root, text="Submit Request", command=apply_outpass).pack()

# GUI Setup
root = tk.Tk()
root.title("Outpass Management System")

var_role = tk.StringVar(value="student")

tk.Label(root, text="User ID:").pack()
entry_user_id = tk.Entry(root)
entry_user_id.pack()

tk.Label(root, text="Name (For Registration):").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Email:").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Password:").pack()
entry_password = tk.Entry(root, show='*')
entry_password.pack()

tk.Label(root, text="Role:").pack()
tk.Radiobutton(root, text="Student", variable=var_role, value="student").pack()
tk.Radiobutton(root, text="Staff", variable=var_role, value="staff").pack()
tk.Radiobutton(root, text="Admin", variable=var_role, value="admin").pack()

tk.Button(root, text="Register", command=register).pack()
tk.Button(root, text="Login", command=login).pack()

root.mainloop()
