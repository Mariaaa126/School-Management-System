import tkinter as tk
import os
import sys

# Ensure the app module can be found when running from this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.style import *
from app.services.database import init_db
from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.views.student import StudentView
from app.views.teacher import TeacherView
from app.views.schedule import ScheduleView
from app.views.attendance import AttendanceView
from app.views.fee import FeeView
from app.views.reports import ReportsView

class SchoolManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("School Management System")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=BG_COLOR)
        
        # Initialize Database
        init_db()

        # State
        self.current_user = None

        # Container for frames
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginView, DashboardView, StudentView, TeacherView, ScheduleView, AttendanceView, FeeView, ReportsView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = SchoolManagementApp()
    app.mainloop()
