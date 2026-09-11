import customtkinter as ctk

from services.access_control import has_permission


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_logout, on_employee_management):
        super().__init__(master)

        self.user = user
        self.on_logout = on_logout
        self.on_employee_management = on_employee_management

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
        )

        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Employee\nManagement\nSystem",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.logo_label.pack(
            padx=20,
            pady=(30, 35),
        )

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard_message,
        )
        self.dashboard_button.pack(
            fill="x",
            padx=20,
            pady=8,
        )

        if has_permission(self.user, "view_employees"):
            self.employee_button = ctk.CTkButton(
                self.sidebar,
                text="Employee Management",
                command=self.on_employee_management,
            )
            self.employee_button.pack(
                fill="x",
                padx=20,
                pady=8,
            )

        if has_permission(self.user, "manage_users"):
            self.user_button = ctk.CTkButton(
                self.sidebar,
                text="User Management",
                state="disabled",
            )
            self.user_button.pack(
                fill="x",
                padx=20,
                pady=8,
            )

        if has_permission(self.user, "view_audit_logs"):
            self.audit_button = ctk.CTkButton(
                self.sidebar,
                text="Audit Logs",
                state="disabled",
            )
            self.audit_button.pack(
                fill="x",
                padx=20,
                pady=8,
            )

        if has_permission(self.user, "manage_backups"):
            self.backup_button = ctk.CTkButton(
                self.sidebar,
                text="Backup & Recovery",
                state="disabled",
            )
            self.backup_button.pack(
                fill="x",
                padx=20,
                pady=8,
            )

        self.logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            command=self.handle_logout,
        )
        self.logout_button.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=20,
        )

    def create_content(self):
        self.content = ctk.CTkFrame(self)
        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.content.grid_columnconfigure(0, weight=1)

        self.heading_label = ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        self.heading_label.grid(
            row=0,
            column=0,
            padx=40,
            pady=(50, 10),
            sticky="w",
        )

        self.welcome_label = ctk.CTkLabel(
            self.content,
            text=f"Welcome, {self.user['username']}",
            font=ctk.CTkFont(size=20),
        )
        self.welcome_label.grid(
            row=1,
            column=0,
            padx=40,
            pady=10,
            sticky="w",
        )

        self.role_label = ctk.CTkLabel(
            self.content,
            text=f"Role: {self.user['role']}",
            font=ctk.CTkFont(size=17),
        )
        self.role_label.grid(
            row=2,
            column=0,
            padx=40,
            pady=(5, 30),
            sticky="w",
        )

        self.info_label = ctk.CTkLabel(
            self.content,
            text="Select an option from the navigation panel.",
            font=ctk.CTkFont(size=15),
        )
        self.info_label.grid(
            row=3,
            column=0,
            padx=40,
            pady=10,
            sticky="w",
        )

    def show_dashboard_message(self):
        self.info_label.configure(
            text="You are currently viewing the Dashboard."
        )

    def handle_logout(self):
        self.on_logout()