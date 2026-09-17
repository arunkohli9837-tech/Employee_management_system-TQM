import customtkinter as ctk

from services.session import Session
from ui.login import LoginFrame
from ui.dashboard import DashboardFrame
from ui.employees import EmployeeManagementFrame
from ui.users import UserManagementFrame
from ui.audit_logs import AuditLogsFrame

class EmployeeManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Employee Management System")
        self.geometry("1000x650")
        self.minsize(900, 600)

        self.session = Session()

        self.show_login()

    def clear_current_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_current_frame()

        self.login_frame = LoginFrame(
            self,
            on_login_success=self.handle_login_success,
        )

        self.login_frame.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20,
        )

    def handle_login_success(self, user):
        self.session.login(user)

        current_user = self.session.get_current_user()

        self.show_dashboard(current_user)

    def show_dashboard(self, user=None):
        self.clear_current_frame()

        current_user = user or self.session.get_current_user()

        self.dashboard_frame = DashboardFrame(
            self,
            user=current_user,
            on_logout=self.handle_logout,
            on_employee_management=self.show_employee_management,
            on_user_management=self.show_user_management,
            on_audit_logs=self.show_audit_logs,
        )

        self.dashboard_frame.pack(
            expand=True,
            fill="both",
        )

    def show_employee_management(self):
        self.clear_current_frame()

        current_user = self.session.get_current_user()

        self.employee_frame = EmployeeManagementFrame(
            self,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.employee_frame.pack(
            expand=True,
            fill="both",
        )

    def show_user_management(self):
        self.clear_current_frame()

        current_user = self.session.get_current_user()

        self.user_frame = UserManagementFrame(
            self,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.user_frame.pack(
            expand=True,
            fill="both",
        )

    def show_audit_logs(self):
        self.clear_current_frame()

        current_user = self.session.get_current_user()

        self.audit_frame = AuditLogsFrame(
            self,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.audit_frame.pack(
            expand=True,
            fill="both",
        )

    def handle_logout(self):
        self.session.logout()
        self.show_login()


def main():
    app = EmployeeManagementApp()
    app.mainloop()


if __name__ == "__main__":
    main()