import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("🔐 MRSA Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.on_success = on_success

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Login to MRSA Blaster", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame, text="Username").pack()
        tk.Entry(self.frame, textvariable=self.username_var).pack(pady=5)
        tk.Label(self.frame, text="Password").pack()
        tk.Entry(self.frame, textvariable=self.password_var, show="*").pack(pady=5)
        tk.Button(self.frame, text="🔓 Login", command=self.check_login).pack(pady=15)

    def check_login(self):
        """Verify login credentials."""
        username = self.username_var.get()
        password = self.password_var.get()

        # Google Sheet CSV as API
        SHEET_URL = "https://docs.google.com/spreadsheets/d/1pDga6BhC42S9hHKPcJivnmjNAaKQTJB5yxikDIJZN-I/export?format=csv"

        try:
            response = requests.get(SHEET_URL)
            if response.status_code != 200:
                messagebox.showerror("Error", "❌ Failed to connect to the authentication service.")
                return
            
            lines = response.text.splitlines()
            for line in lines[1:]:
                u, p, name, role = line.split(",")
                if u.strip() == username and p.strip() == password:
                    # Save session data for automatic login next time
                    with open("session.json", "w") as f:
                        json.dump({"role": role.strip(), "name": name.strip()}, f)
                    self.root.destroy()  # Close login panel
                    self.on_success(role.strip(), name.strip())  # Transition to main panel
                    return
            
            # Invalid login credentials
            messagebox.showerror("Error", "❌ Invalid credentials")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to check login: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
