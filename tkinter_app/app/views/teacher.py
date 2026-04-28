import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import *
from app.services.database import execute_query, fetch_all

class TeacherView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        
        back_btn = tk.Button(header_frame, text="Back", font=FONT_BOLD, bg=SECONDARY_COLOR, fg=WHITE, command=lambda: self.controller.show_frame("DashboardView"))
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="Manage Teachers", font=FONT_SUBTITLE, bg=PRIMARY_COLOR, fg=WHITE)
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Main Content Frame
        content_frame = tk.Frame(self, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Form Frame
        form_frame = tk.LabelFrame(content_frame, text="Teacher Details", font=FONT_BOLD, bg=BG_COLOR, padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # Form Fields
        labels = ["First Name", "Last Name", "Subject", "Contact Number", "Email"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(form_frame, text=label_text, font=FONT_NORMAL, bg=BG_COLOR).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label_text] = entry

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=BG_COLOR)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Add", font=FONT_BOLD, bg=SUCCESS_COLOR, fg=WHITE, width=8, command=self.add_teacher).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", font=FONT_BOLD, bg=PRIMARY_COLOR, fg=WHITE, width=8, command=self.update_teacher).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", font=FONT_BOLD, bg=ERROR_COLOR, fg=WHITE, width=8, command=self.delete_teacher).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", font=FONT_BOLD, bg=SECONDARY_COLOR, fg=WHITE, width=8, command=self.clear_form).grid(row=0, column=3, padx=5)

        # Treeview (Data Table)
        list_frame = tk.Frame(content_frame)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("id", "first_name", "last_name", "subject", "contact")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("contact", text="Contact")
        
        self.tree.column("id", width=50)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<ButtonRelease-1>", self.select_record)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = fetch_all("SELECT * FROM teachers")
        for row in records:
            self.tree.insert("", tk.END, values=(row["id"], row["first_name"], row["last_name"], row["subject"], row["contact_number"]))

    def add_teacher(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not data["First Name"] or not data["Last Name"]:
            messagebox.showerror("Error", "First and Last Name are required")
            return
            
        query = """INSERT INTO teachers (first_name, last_name, subject, contact_number, email) 
                   VALUES (?, ?, ?, ?, ?)"""
        execute_query(query, (data["First Name"], data["Last Name"], data["Subject"], data["Contact Number"], data["Email"]))
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Success", "Teacher added successfully")

    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        teacher_id = values[0]
        
        record = fetch_all("SELECT * FROM teachers WHERE id=?", (teacher_id,))[0]
        self.clear_form()
        self.selected_id = teacher_id
        
        self.entries["First Name"].insert(0, record["first_name"])
        self.entries["Last Name"].insert(0, record["last_name"])
        self.entries["Subject"].insert(0, record["subject"])
        self.entries["Contact Number"].insert(0, record["contact_number"])
        self.entries["Email"].insert(0, record["email"])

    def update_teacher(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showerror("Error", "Please select a record to update")
            return
            
        data = {k: v.get() for k, v in self.entries.items()}
        query = """UPDATE teachers SET first_name=?, last_name=?, subject=?, contact_number=?, email=? WHERE id=?"""
        execute_query(query, (data["First Name"], data["Last Name"], data["Subject"], data["Contact Number"], data["Email"], self.selected_id))
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Success", "Teacher updated successfully")

    def delete_teacher(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showerror("Error", "Please select a record to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this teacher?"):
            execute_query("DELETE FROM teachers WHERE id=?", (self.selected_id,))
            self.clear_form()
            self.load_data()
            messagebox.showinfo("Success", "Teacher deleted successfully")

    def clear_form(self):
        if hasattr(self, 'selected_id'):
            del self.selected_id
        for entry in self.entries.values():
            entry.delete(0, tk.END)
