import tkinter as tk
from tkinter import messagebox
from app.utils.style import *
from app.services.auth import authenticate

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        
        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="School Management System", font=FONT_TITLE, bg=BG_COLOR, fg=PRIMARY_COLOR)
        title_label.pack(pady=(100, 50))

        # Login Frame
        login_frame = tk.Frame(self, bg=WHITE, padx=40, pady=40, relief=tk.RAISED, bd=2)
        login_frame.pack()

        # Username
        username_label = tk.Label(login_frame, text="Username", font=FONT_BOLD, bg=WHITE, fg=TEXT_COLOR)
        username_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        self.username_entry = tk.Entry(login_frame, font=FONT_NORMAL, width=30)
        self.username_entry.grid(row=1, column=0, pady=(0, 20))

        # Password
        password_label = tk.Label(login_frame, text="Password", font=FONT_BOLD, bg=WHITE, fg=TEXT_COLOR)
        password_label.grid(row=2, column=0, pady=(0, 5), sticky="w")
        self.password_entry = tk.Entry(login_frame, font=FONT_NORMAL, width=30, show="*")
        self.password_entry.grid(row=3, column=0, pady=(0, 30))

        # Login Button
        login_btn = tk.Button(login_frame, text="Login", font=FONT_BOLD, bg=SECONDARY_COLOR, fg=WHITE, width=28, command=self.login)
        login_btn.grid(row=4, column=0)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        user = authenticate(username, password)
        if user:
            self.controller.current_user = user
            self.controller.show_frame("DashboardView")
        else:
            messagebox.showerror("Error", "Invalid credentials")
