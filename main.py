import customtkinter as ctk

from services.session import Session
from services.error_handler import handle_exception

from ui.login import LoginFrame
from ui.dashboard import DashboardFrame
from ui.employees import EmployeeManagementFrame
from ui.users import UserManagementFrame
from ui.audit_logs import AuditLogsFrame
from ui.backup import BackupManagementFrame


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
        current_user = user or self.session.get_current_user()

        if (
            hasattr(self, "dashboard_frame")
            and self.dashboard_frame.winfo_exists()
        ):
            self.dashboard_frame.show_dashboard_content()
            return

        self.clear_current_frame()

        self.dashboard_frame = DashboardFrame(
            self,
            user=current_user,
            on_logout=self.handle_logout,
            on_employee_management=self.show_employee_management,
            on_user_management=self.show_user_management,
            on_audit_logs=self.show_audit_logs,
            on_backup_management=self.show_backup_management,
        )

        self.dashboard_frame.pack(
            expand=True,
            fill="both",
        )

    def show_employee_management(self):
        current_user = self.session.get_current_user()

        self.employee_frame = EmployeeManagementFrame(
            self.dashboard_frame.content,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.dashboard_frame.show_feature(
            self.employee_frame,
            self.dashboard_frame.employee_button,
        )

    def show_user_management(self):
        current_user = self.session.get_current_user()

        self.user_frame = UserManagementFrame(
            self.dashboard_frame.content,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.dashboard_frame.show_feature(
            self.user_frame,
            self.dashboard_frame.user_button,
        )

    def show_audit_logs(self):
        current_user = self.session.get_current_user()

        self.audit_logs_frame = AuditLogsFrame(
            self.dashboard_frame.content,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.dashboard_frame.show_feature(
            self.audit_logs_frame,
            self.dashboard_frame.audit_button,
        )

    def show_backup_management(self):
        current_user = self.session.get_current_user()

        self.backup_frame = BackupManagementFrame(
            self.dashboard_frame.content,
            user=current_user,
            on_back=self.show_dashboard,
        )

        self.dashboard_frame.show_feature(
            self.backup_frame,
            self.dashboard_frame.backup_button,
        )

    def handle_logout(self):
        self.session.logout()
        self.show_login()


def main():
    try:
        app = EmployeeManagementApp()
        app.mainloop()

    except Exception as error:
        message = handle_exception(
            "Application startup/runtime error",
            error,
        )

        print(message)


if __name__ == "__main__":
    main()