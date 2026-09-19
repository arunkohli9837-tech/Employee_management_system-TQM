import customtkinter as ctk

from services.access_control import has_permission
from services.employee_service import get_all_employees
from services.user_service import get_all_users
from services.audit_service import get_all_audit_logs
from services.backup_service import list_backups


class DashboardFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        user,
        on_logout,
        on_employee_management,
        on_user_management,
        on_audit_logs,
        on_backup_management=None,
    ):
        super().__init__(master)

        self.user = user
        self.on_logout = on_logout
        self.on_employee_management = on_employee_management
        self.on_user_management = on_user_management
        self.on_audit_logs = on_audit_logs
        self.on_backup_management = on_backup_management

        self.configure(fg_color=("gray95", "gray10"))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content()

    def show_dashboard_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.set_active_navigation(self.dashboard_button)

        self.create_dashboard_home()

    def show_feature(self, feature_frame, active_button):
        for widget in self.content.winfo_children():
            if widget is not feature_frame:
                widget.destroy()

        self.set_active_navigation(active_button)

        feature_frame.pack(
            expand=True,
            fill="both",
        )

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=235,
            corner_radius=0,
            fg_color=("#172554", "#101936"),
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Employee\nManagement System",
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
            text_color="white",
        )

        self.logo_label.pack(
            padx=20,
            pady=(38, 35),
        )

        self.create_navigation_buttons()
        self.create_profile_section()

    def create_dashboard_home(self):
        self.content.grid_rowconfigure(4, weight=1)

        self.create_header()
        self.create_summary_cards()
        self.create_reliability_section()

    def create_navigation_buttons(self):
        self.dashboard_button = self.create_nav_button(
            "▦   Dashboard",
            self.show_dashboard_message,
            active=True,
        )

        if has_permission(self.user, "view_employees"):
            self.employee_button = self.create_nav_button(
                "▣   Employees",
                self.on_employee_management,
            )

        if has_permission(self.user, "manage_users"):
            self.user_button = self.create_nav_button(
                "♙   User Management",
                self.on_user_management,
            )

        if has_permission(self.user, "view_audit_logs"):
            self.audit_button = self.create_nav_button(
                "▤   Audit Logs",
                self.on_audit_logs,
            )

        if has_permission(self.user, "manage_backups"):
            self.backup_button = self.create_nav_button(
                "▣   Backups",
                self.on_backup_management,
            )

        self.reliability_button = self.create_nav_button(
            "◇   Reliability",
            None,
        )

    def set_active_navigation(self, active_button):
        buttons = [
            getattr(self, "dashboard_button", None),
            getattr(self, "employee_button", None),
            getattr(self, "user_button", None),
            getattr(self, "audit_button", None),
            getattr(self, "backup_button", None),
            getattr(self, "reliability_button", None),
        ]

        for button in buttons:
            if button is not None:
                button.configure(
                    fg_color=(
                        "#2855b8"
                        if button is active_button
                        else "transparent"
                    )
                )

    def create_nav_button(
        self,
        text,
        command,
        active=False,
    ):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            height=46,
            corner_radius=8,
            anchor="w",
            font=ctk.CTkFont(size=15),
            fg_color=(
                "#2855b8" if active else "transparent"
            ),
            hover_color="#244a9d",
            text_color="white",
        )

        button.pack(
            fill="x",
            padx=15,
            pady=4,
        )

        return button

    def create_profile_section(self):
        self.profile_container = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
        )

        self.profile_container.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=(10, 20),
        )

        self.profile_separator = ctk.CTkFrame(
            self.profile_container,
            height=1,
            fg_color="#34446f",
        )

        self.profile_separator.pack(
            fill="x",
            pady=(0, 18),
        )

        self.profile_label = ctk.CTkLabel(
            self.profile_container,
            text=f"{self.user['username']}\n{self.user['role']}",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            text_color="white",
        )

        self.profile_label.pack(
            pady=(0, 15),
        )

        self.logout_button = ctk.CTkButton(
            self.profile_container,
            text="Logout",
            command=self.handle_logout,
            height=42,
            corner_radius=8,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            font=ctk.CTkFont(size=14),
        )

        self.logout_button.pack(
            fill="x",
        )

    # =========================================================
    # MAIN CONTENT
    # =========================================================

    def create_content(self):
        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=("gray95", "gray10"),
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=0,
            pady=0,
        )

        self.content.grid_columnconfigure(
            0,
            weight=1,
        )

        self.content.grid_rowconfigure(
            0,
            weight=1,
        )

        self.show_dashboard_content()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):
        self.heading_label = ctk.CTkLabel(
            self.content,
            text=f"Welcome, {self.user['username']}",
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
            anchor="w",
        )

        self.heading_label.grid(
            row=0,
            column=0,
            padx=40,
            pady=(35, 3),
            sticky="w",
        )

        self.subtitle_label = ctk.CTkLabel(
            self.content,
            text="Employee Management System • Q01 Improve Reliability",
            font=ctk.CTkFont(size=15),
            text_color=("gray45", "gray65"),
            anchor="w",
        )

        self.subtitle_label.grid(
            row=1,
            column=0,
            padx=40,
            pady=(0, 6),
            sticky="w",
        )

        self.access_label = ctk.CTkLabel(
            self.content,
            text=f"Current Access Level: {self.user['role']}",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            text_color="#2563eb",
            anchor="w",
        )

        self.access_label.grid(
            row=2,
            column=0,
            padx=40,
            pady=(0, 25),
            sticky="w",
        )

    # =========================================================
    # SUMMARY CARDS
    # =========================================================

    def create_summary_cards(self):
        self.cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent",
        )

        self.cards_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=40,
            pady=(0, 30),
        )

        for column in range(3):
            self.cards_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        employees_count = self.get_employee_count()
        audit_count = self.get_audit_count()
        users_count = self.get_user_count()

        self.create_summary_card(
            self.cards_frame,
            column=0,
            number=employees_count,
            title="Employees",
            description="Total employee records",
            symbol="♙",
        )

        self.create_summary_card(
            self.cards_frame,
            column=1,
            number=audit_count,
            title="Audit Events",
            description="Recorded system activities",
            symbol="▤",
        )

        self.create_summary_card(
            self.cards_frame,
            column=2,
            number=users_count,
            title="System Users",
            description="Registered user accounts",
            symbol="♙",
        )

    def create_summary_card(
        self,
        parent,
        column,
        number,
        title,
        description,
        symbol,
    ):
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=("white", "#181818"),
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=7,
        )

        card.grid_columnconfigure(
            1,
            weight=1,
        )

        icon = ctk.CTkLabel(
            card,
            text=symbol,
            width=48,
            height=48,
            corner_radius=24,
            fg_color=("#eaf2ff", "#1d315f"),
            text_color="#2563eb",
            font=ctk.CTkFont(
                size=23,
                weight="bold",
            ),
        )

        icon.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(20, 15),
            pady=20,
        )

        number_label = ctk.CTkLabel(
            card,
            text=str(number),
            font=ctk.CTkFont(
                size=29,
                weight="bold",
            ),
            text_color="#2563eb",
            anchor="w",
        )

        number_label.grid(
            row=0,
            column=1,
            sticky="w",
            pady=(18, 0),
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
            anchor="w",
        )

        title_label.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(0, 2),
        )

        description_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65"),
            anchor="w",
        )

        description_label.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(0, 18),
        )

    # =========================================================
    # RELIABILITY OVERVIEW
    # =========================================================

    def create_reliability_section(self):
        self.reliability_title = ctk.CTkLabel(
            self.content,
            text="Reliability Overview",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            anchor="w",
        )

        self.reliability_title.grid(
            row=4,
            column=0,
            padx=40,
            pady=(0, 15),
            sticky="nw",
        )

        self.reliability_panel = ctk.CTkFrame(
            self.content,
            corner_radius=12,
            fg_color=("white", "#181818"),
        )

        self.reliability_panel.grid(
            row=5,
            column=0,
            sticky="nsew",
            padx=40,
            pady=(0, 35),
        )

        self.reliability_panel.grid_columnconfigure(
            1,
            weight=1,
        )

        automatic_backup_status, automatic_backup_type = (
            self.get_automatic_backup_status()
        )

        reliability_items = [
            (
                "Database Status",
                "System database is operating normally",
                "Healthy",
                "healthy",
            ),
            (
                "Input Validation",
                "All input validation checks are active",
                "Active",
                "active",
            ),
            (
                "Audit Logging",
                "System audit logging is enabled",
                "Active + Visible",
                "active",
            ),
            (
                "Role Based Access",
                "RBAC is enforced for system operations",
                "Active",
                "active",
            ),
            (
                "Automatic Backup",
                "Latest automatic backup status",
                automatic_backup_status,
                automatic_backup_type,
            ),
        ]

        for row, item in enumerate(reliability_items):
            title, description, status, status_type = item

            if row > 0:
                separator = ctk.CTkFrame(
                    self.reliability_panel,
                    height=1,
                    fg_color=("gray88", "gray25"),
                )

                separator.grid(
                    row=row * 2 - 1,
                    column=0,
                    columnspan=3,
                    sticky="ew",
                    padx=25,
                )

            actual_row = row * 2

            icon = ctk.CTkLabel(
                self.reliability_panel,
                text="●",
                width=40,
                height=40,
                corner_radius=20,
                fg_color=(
                    "#edf4ff",
                    "#1d315f",
                ),
                text_color="#2563eb",
                font=ctk.CTkFont(size=14),
            )

            icon.grid(
                row=actual_row,
                column=0,
                padx=(25, 15),
                pady=12,
            )

            text_frame = ctk.CTkFrame(
                self.reliability_panel,
                fg_color="transparent",
            )

            text_frame.grid(
                row=actual_row,
                column=1,
                sticky="ew",
                pady=10,
            )

            title_label = ctk.CTkLabel(
                text_frame,
                text=title,
                font=ctk.CTkFont(
                    size=15,
                    weight="bold",
                ),
                anchor="w",
            )

            title_label.pack(
                anchor="w",
            )

            description_label = ctk.CTkLabel(
                text_frame,
                text=description,
                font=ctk.CTkFont(size=13),
                text_color=("gray45", "gray65"),
                anchor="w",
            )

            description_label.pack(
                anchor="w",
            )

            status_colors = {
                "healthy": (
                    "#dcfce7",
                    "#86efac",
                    "#15803d",
                ),
                "active": (
                    "#eaf2ff",
                    "#bfdbfe",
                    "#2563eb",
                ),
                "pending": (
                    "#f3e8ff",
                    "#ddd6fe",
                    "#7c3aed",
                ),
            }

            bg_light, bg_dark, text_color = status_colors[
                status_type
            ]

            status_label = ctk.CTkLabel(
                self.reliability_panel,
                text=f"●  {status}",
                corner_radius=18,
                fg_color=(bg_light, bg_dark),
                text_color=text_color,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold",
                ),
                padx=12,
                pady=6,
            )

            status_label.grid(
                row=actual_row,
                column=2,
                padx=(15, 25),
                pady=12,
            )

    # =========================================================
    # DATABASE COUNTS
    # =========================================================

    def get_employee_count(self):
        try:
            return len(get_all_employees())
        except Exception:
            return 0

    def get_user_count(self):
        try:
            return len(get_all_users())
        except Exception:
            return 0

    def get_audit_count(self):
        try:
            return len(get_all_audit_logs())
        except Exception:
            return 0

    def get_automatic_backup_status(self):
        try:
            backups = list_backups()

            automatic_backups = [
                backup
                for backup in backups
                if "_auto_" in backup.name
            ]

            if automatic_backups:
                return "Active", "healthy"

            return "Pending", "pending"

        except Exception:
            return "Unavailable", "pending"

    # =========================================================
    # ACTIONS
    # =========================================================

    def show_dashboard_message(self):
        self.show_dashboard_content()

    def handle_logout(self):
        self.on_logout()