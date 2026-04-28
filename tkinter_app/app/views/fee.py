import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import *
from app.services.database import execute_query, fetch_all
from datetime import date

class FeeView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        
        back_btn = tk.Button(header_frame, text="Back", font=FONT_BOLD, bg=SECONDARY_COLOR, fg=WHITE, command=lambda: self.controller.show_frame("DashboardView"))
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="Fee Management", font=FONT_SUBTITLE, bg=PRIMARY_COLOR, fg=WHITE)
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        content_frame = tk.Frame(self, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        form_frame = tk.LabelFrame(content_frame, text="Fee Details", font=FONT_BOLD, bg=BG_COLOR, padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        tk.Label(form_frame, text="Student ID", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=5)
        self.student_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
        self.student_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Amount", font=FONT_NORMAL, bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
        self.amount_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD)", font=FONT_NORMAL, bg=BG_COLOR).grid(row=2, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Status", font=FONT_NORMAL, bg=BG_COLOR).grid(row=3, column=0, sticky="w", pady=5)
        self.status_var = tk.StringVar()
        self.status_cb = ttk.Combobox(form_frame, textvariable=self.status_var, values=("Paid", "Pending", "Overdue"), font=FONT_NORMAL, state="readonly")
        self.status_cb.current(0)
        self.status_cb.grid(row=3, column=1, pady=5, padx=5)

        btn_frame = tk.Frame(form_frame, bg=BG_COLOR)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Record", font=FONT_BOLD, bg=SUCCESS_COLOR, fg=WHITE, width=10, command=self.record_fee).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", font=FONT_BOLD, bg=PRIMARY_COLOR, fg=WHITE, width=10, command=self.update_fee).grid(row=0, column=1, padx=5)

        list_frame = tk.Frame(content_frame)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("id", "student", "amount", "date", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("student", text="Student ID")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("date", text="Date")
        self.tree.heading("status", text="Status")
        
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
        records = fetch_all("SELECT * FROM fees ORDER BY payment_date DESC")
        for row in records:
            self.tree.insert("", tk.END, values=(row["id"], row["student_id"], row["amount"], row["payment_date"], row["status"]))

    def record_fee(self):
        student_id = self.student_entry.get()
        amount = self.amount_entry.get()
        payment_date = self.date_entry.get()
        status = self.status_var.get()
        
        if not student_id or not amount:
            messagebox.showerror("Error", "Student ID and Amount are required")
            return
            
        execute_query("INSERT INTO fees (student_id, amount, payment_date, status) VALUES (?, ?, ?, ?)", (student_id, amount, payment_date, status))
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Success", "Fee recorded successfully")

    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        self.selected_id = values[0]
        
        self.student_entry.delete(0, tk.END)
        self.student_entry.insert(0, values[1])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[2])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[3])
        self.status_cb.set(values[4])

    def update_fee(self):
        if not hasattr(self, 'selected_id'):
            return
        execute_query("UPDATE fees SET student_id=?, amount=?, payment_date=?, status=? WHERE id=?", 
                      (self.student_entry.get(), self.amount_entry.get(), self.date_entry.get(), self.status_var.get(), self.selected_id))
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Success", "Fee updated successfully")

    def clear_form(self):
        if hasattr(self, 'selected_id'):
            del self.selected_id
        self.student_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
