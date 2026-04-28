import tkinter as tk
from app.utils.style import *

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Dashboard", font=FONT_TITLE, bg=PRIMARY_COLOR, fg=WHITE)
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        logout_btn = tk.Button(header_frame, text="Logout", font=FONT_BOLD, bg=ERROR_COLOR, fg=WHITE, command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)

        # Content area (Grid for modules)
        content_frame = tk.Frame(self, bg=BG_COLOR)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)

        # Modules
        modules = [
            ("Students", "StudentView"),
            ("Teachers", "TeacherView"),
            ("Schedule", "ScheduleView"),
            ("Attendance", "AttendanceView"),
            ("Fees", "FeeView"),
            ("Reports", "ReportsView")
        ]

        row = 0
        col = 0
        for module_name, frame_name in modules:
            btn = tk.Button(content_frame, text=module_name, font=FONT_SUBTITLE, bg=SECONDARY_COLOR, fg=WHITE,
                            width=15, height=3, command=lambda f=frame_name: self.controller.show_frame(f))
            btn.grid(row=row, column=col, padx=20, pady=20)
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginView")
