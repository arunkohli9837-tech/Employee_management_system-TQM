import customtkinter as ctk

from services.access_control import has_permission, has_role
from ui.login import LoginFrame
from services.session import Session

class EmployeeManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Employee Management System")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.session = Session()

        self.show_login()

    def show_login(self):
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

        print(
            f"Login successful: "
            f"{current_user['username']} "
            f"({current_user['role']})"
        )
    from services.access_control import has_permission, has_role

    def handle_login_success(self, user):
        self.session.login(user)

        current_user = self.session.get_current_user()

        print(
            f"Login successful: "
            f"{current_user['username']} "
            f"({current_user['role']})"
            )

        print(
            f"Admin role: {has_role(current_user, 'Admin')}"
        )

        print(
            f"Can manage users: {has_permission(current_user, 'manage_users')}"
        )

        print(
            f"Can manage employees: {has_permission(current_user, 'manage_employees')}"
    )

def main():
    app = EmployeeManagementApp()
    app.mainloop()


if __name__ == "__main__":
    main()