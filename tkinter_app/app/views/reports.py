import tkinter as tk
from app.utils.style import *
from app.services.database import fetch_one

class ReportsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        
        back_btn = tk.Button(header_frame, text="Back", font=FONT_BOLD, bg=SECONDARY_COLOR, fg=WHITE, command=lambda: self.controller.show_frame("DashboardView"))
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="Reports Dashboard", font=FONT_SUBTITLE, bg=PRIMARY_COLOR, fg=WHITE)
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.content_frame = tk.Frame(self, bg=BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.generate_reports()

    def generate_reports(self):
        # Clear existing
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Get Stats
        student_count = fetch_one("SELECT COUNT(*) as count FROM students")["count"]
        teacher_count = fetch_one("SELECT COUNT(*) as count FROM teachers")["count"]
        total_fees = fetch_one("SELECT SUM(amount) as total FROM fees WHERE status='Paid'")["total"]
        if total_fees is None: total_fees = 0

        # Display Cards
        self.create_stat_card("Total Students", student_count, 0, 0)
        self.create_stat_card("Total Teachers", teacher_count, 0, 1)
        self.create_stat_card("Fees Collected", f"${total_fees:,.2f}", 1, 0)

    def create_stat_card(self, title, value, row, col):
        card = tk.Frame(self.content_frame, bg=WHITE, padx=20, pady=20, relief=tk.RAISED, bd=2)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        tk.Label(card, text=title, font=FONT_SUBTITLE, bg=WHITE, fg=TEXT_COLOR).pack(pady=(0, 10))
        tk.Label(card, text=str(value), font=FONT_TITLE, bg=WHITE, fg=SECONDARY_COLOR).pack()
