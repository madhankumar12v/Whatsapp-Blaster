import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from login import LoginWindow
from sender import start_whatsapp_blast
import pandas as pd
import datetime
import logs
import os

class WhatsAppBlasterApp:
    def __init__(self, root, user_type, name):
        self.root = root
        self.user_type = user_type
        self.name = name
        self.root.title("MRSA WhatsApp Blaster - Premium")
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e2f")
        self.contact_df = None
        self.file_path = None
        self.attachment_path = None
        self.create_ui()

    def create_ui(self):
        # Left Frame for Contacts
        left_frame = ttk.Frame(self.root, width=400, padding=20)
        left_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(left_frame, text="Upload Contact File (CSV/Excel)", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Button(left_frame, text="Upload Contacts", command=self.upload_contacts).pack(pady=5)

        self.tree = ttk.Treeview(left_frame, columns=("Name", "Phone"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.pack(pady=5, fill="x")

        # Right Frame for Message and Log
        right_frame = ttk.Frame(self.root, width=600, padding=20)
        right_frame.grid(row=0, column=1, sticky="nsew")

        ttk.Label(right_frame, text=f"Logged in as: {self.name} ({self.user_type})", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(right_frame, text="Message Template", font=("Arial", 12, "bold")).pack(pady=10)

        self.message_box = tk.Text(right_frame, height=4, width=50)
        self.message_box.pack(pady=5)

        ttk.Label(right_frame, text="Attach File (Optional)", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Button(right_frame, text="Upload Attachment", command=self.upload_attachment).pack(pady=5)

        self.attachment_label = ttk.Label(right_frame, text="No file attached", font=("Arial", 10))
        self.attachment_label.pack(pady=5)

        self.progress = ttk.Progressbar(right_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.log_box = tk.Text(right_frame, height=10, width=50, bg="#252526", fg="white")
        self.log_box.pack(pady=5)

        ttk.Button(right_frame, text="Start Blasting", command=self.start_blasting).pack(pady=5)

    def upload_contacts(self):
        """Upload contacts from a CSV or Excel file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")])
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    self.contact_df = pd.read_csv(file_path)
                else:
                    self.contact_df = pd.read_excel(file_path)

                self.tree.delete(*self.tree.get_children())
                for _, row in self.contact_df.iterrows():
                    self.tree.insert('', 'end', values=(row['Name'], row['Phone']))

                self.file_path = file_path
                messagebox.showinfo("Uploaded", f"Successfully loaded {len(self.contact_df)} contacts.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def upload_attachment(self):
        """Select and display an attachment."""
        attachment_file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if attachment_file:
            self.attachment_path = attachment_file
            self.attachment_label.config(text=f"Attached: {os.path.basename(attachment_file)}")
            messagebox.showinfo("Attachment", f"File {attachment_file} selected for upload.")

    def log(self, text):
        """Append log message to the log box."""
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def start_blasting(self):
        """Start the WhatsApp blasting process."""
        message = self.message_box.get("1.0", tk.END).strip()
        if self.contact_df is None or not message:
            messagebox.showwarning("Input Missing", "Please upload contacts and enter a message.")
            return

        self.log_box.delete("1.0", tk.END)
        self.progress["value"] = 0
        self.root.update_idletasks()

        self.log("\n🚀 Starting WhatsApp Blasting...")
        total = len(self.contact_df)
        success_count = 0
        failed_count = 0
        log_entries = []

        # Get list of phone numbers
        phones = self.contact_df['Phone'].astype(str).tolist()

        # Send messages using sender.py function
        status = start_whatsapp_blast(self.file_path, message, self.attachment_path)

        # Process the status of each contact
        for i, row in self.contact_df.iterrows():
            name, Phone = row['Name'], str(row['Phone'])
            if status == "Success":
                self.log(f"✅ Sent to {name} ({Phone})")
                success_count += 1
            else:
                self.log(f"❌ Failed for {name} ({Phone})")
                failed_count += 1

            log_entries.append({"Name": name, "Phone": Phone, "Status": status, "Time": str(datetime.datetime.now())})
            self.progress["value"] = (i + 1) / total * 100
            self.root.update_idletasks()

        self.log("\n📊 Summary:")
        self.log(f"✅ Success: {success_count}")
        self.log(f"❌ Failed: {failed_count}")

        logs.save_log(log_entries)
        messagebox.showinfo("Completed", f"Blasting finished. Success: {success_count}, Failed: {failed_count}")


def open_main_panel(user_type, name):
    """Open the main WhatsApp Blaster UI."""
    root = tk.Tk()
    app = WhatsAppBlasterApp(root, user_type, name)
    root.mainloop()

if __name__ == '__main__':
    def launch_main_app(role, name):
        """Launch the main application after login."""
        open_main_panel(role, name)

    root_login = tk.Tk()
    login_app = LoginWindow(root_login, on_success=launch_main_app)
    root_login.mainloop()