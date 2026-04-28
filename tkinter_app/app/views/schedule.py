import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import *
from app.services.database import execute_query, fetch_all

class ScheduleView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        
        back_btn = tk.Button(header_frame, text="Back", font=FONT_BOLD, bg=SECONDARY_COLOR, fg=WHITE, command=lambda: self.controller.show_frame("DashboardView"))
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="Class Scheduling", font=FONT_SUBTITLE, bg=PRIMARY_COLOR, fg=WHITE)
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        content_frame = tk.Frame(self, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        form_frame = tk.LabelFrame(content_frame, text="Class Details", font=FONT_BOLD, bg=BG_COLOR, padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        tk.Label(form_frame, text="Class Name", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Teacher ID", font=FONT_NORMAL, bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=5)
        self.teacher_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
        self.teacher_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Time", font=FONT_NORMAL, bg=BG_COLOR).grid(row=2, column=0, sticky="w", pady=5)
        self.time_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=25)
        self.time_entry.grid(row=2, column=1, pady=5, padx=5)

        btn_frame = tk.Frame(form_frame, bg=BG_COLOR)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Add", font=FONT_BOLD, bg=SUCCESS_COLOR, fg=WHITE, width=8, command=self.add_class).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", font=FONT_BOLD, bg=PRIMARY_COLOR, fg=WHITE, width=8, command=self.update_class).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", font=FONT_BOLD, bg=ERROR_COLOR, fg=WHITE, width=8, command=self.delete_class).grid(row=0, column=2, padx=5)

        list_frame = tk.Frame(content_frame)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("id", "name", "teacher", "time")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Class Name")
        self.tree.heading("teacher", text="Teacher ID")
        self.tree.heading("time", text="Time")
        
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
        records = fetch_all("SELECT * FROM classes")
        for row in records:
            self.tree.insert("", tk.END, values=(row["id"], row["name"], row["teacher_id"], row["schedule_time"]))

    def add_class(self):
        name = self.name_entry.get()
        teacher = self.teacher_entry.get()
        time = self.time_entry.get()
        
        if not name or not teacher:
            messagebox.showerror("Error", "Name and Teacher ID are required")
            return
            
        execute_query("INSERT INTO classes (name, teacher_id, schedule_time) VALUES (?, ?, ?)", (name, teacher, time))
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Success", "Class added successfully")

    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        class_id = values[0]
        
        record = fetch_all("SELECT * FROM classes WHERE id=?", (class_id,))[0]
        self.clear_form()
        self.selected_id = class_id
        
        self.name_entry.insert(0, record["name"])
        self.teacher_entry.insert(0, str(record["teacher_id"]))
        self.time_entry.insert(0, record["schedule_time"])

    def update_class(self):
        if not hasattr(self, 'selected_id'):
            return
        execute_query("UPDATE classes SET name=?, teacher_id=?, schedule_time=? WHERE id=?", 
                      (self.name_entry.get(), self.teacher_entry.get(), self.time_entry.get(), self.selected_id))
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Success", "Class updated successfully")

    def delete_class(self):
        if not hasattr(self, 'selected_id'):
            return
        if messagebox.askyesno("Confirm", "Delete this class?"):
            execute_query("DELETE FROM classes WHERE id=?", (self.selected_id,))
            self.clear_form()
            self.load_data()
            messagebox.showinfo("Success", "Class deleted successfully")

    def clear_form(self):
        if hasattr(self, 'selected_id'):
            del self.selected_id
        self.name_entry.delete(0, tk.END)
        self.teacher_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
