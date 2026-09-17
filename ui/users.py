import customtkinter as ctk
from tkinter import messagebox

from services.user_service import (
    get_all_users,
    activate_user,
    deactivate_user,
)


class UserManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back
        self.selected_user_id = None

        self.configure(fg_color=("gray95", "gray10"))

        self.grid_columnconfigure(0, weight=0, minsize=390)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_account_panel()
        self.create_records_panel()

        self.load_users()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):
        self.header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(25, 15),
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text="User Roles & Access Control",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
            anchor="w",
        )

        self.title_label.pack(
            side="left",
        )

    # =========================================================
    # LEFT ACCOUNT PANEL
    # =========================================================

    def create_account_panel(self):
        self.account_panel = ctk.CTkFrame(self)

        self.account_panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(30, 12),
            pady=(0, 30),
        )

        self.account_panel.grid_columnconfigure(
            0,
            weight=1,
        )

        self.account_panel.grid_rowconfigure(
            1,
            weight=1,
        )

        self.account_title = ctk.CTkLabel(
            self.account_panel,
            text="User Account",
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
        )

        self.account_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(25, 15),
        )

        self.account_scroll = ctk.CTkScrollableFrame(
            self.account_panel,
            fg_color="transparent",
        )

        self.account_scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10),
        )

        self.account_scroll.grid_columnconfigure(
            0,
            weight=1,
        )

        # Username
        self.username_label = ctk.CTkLabel(
            self.account_scroll,
            text="Username",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            anchor="w",
        )

        self.username_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(5, 5),
        )

        self.username_entry = ctk.CTkEntry(
            self.account_scroll,
            height=38,
        )

        self.username_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 12),
        )

        # Role
        self.role_label = ctk.CTkLabel(
            self.account_scroll,
            text="User Role",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            anchor="w",
        )

        self.role_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=15,
            pady=(5, 5),
        )

        self.role_entry = ctk.CTkEntry(
            self.account_scroll,
            height=38,
        )

        self.role_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 12),
        )

        # Status
        self.status_label = ctk.CTkLabel(
            self.account_scroll,
            text="Account Status",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            anchor="w",
        )

        self.status_label.grid(
            row=4,
            column=0,
            sticky="w",
            padx=15,
            pady=(5, 5),
        )

        self.status_entry = ctk.CTkEntry(
            self.account_scroll,
            height=38,
        )

        self.status_entry.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 20),
        )

        # Information
        self.info_label = ctk.CTkLabel(
            self.account_scroll,
            text=(
                "Select a user from the records panel "
                "to manage the account status."
            ),
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65"),
            wraplength=300,
            justify="left",
            anchor="w",
        )

        self.info_label.grid(
            row=6,
            column=0,
            sticky="w",
            padx=15,
            pady=(5, 20),
        )

        # Action buttons
        self.action_frame = ctk.CTkFrame(
            self.account_panel,
            fg_color="transparent",
        )

        self.action_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(5, 25),
        )

        self.action_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.activate_button = ctk.CTkButton(
            self.action_frame,
            text="Activate User",
            height=40,
            state="disabled",
            command=self.activate_selected_user,
        )

        self.activate_button.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 8),
        )

        self.deactivate_button = ctk.CTkButton(
            self.action_frame,
            text="Deactivate User",
            height=40,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            state="disabled",
            command=self.deactivate_selected_user,
        )

        self.deactivate_button.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=4,
        )

        self.clear_button = ctk.CTkButton(
            self.action_frame,
            text="Clear Selection",
            height=40,
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.clear_selection,
        )

        self.clear_button.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(8, 0),
        )

    # =========================================================
    # RIGHT RECORDS PANEL
    # =========================================================

    def create_records_panel(self):
        self.records_panel = ctk.CTkFrame(self)

        self.records_panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(12, 30),
            pady=(0, 30),
        )

        self.records_panel.grid_columnconfigure(
            0,
            weight=1,
        )

        self.records_panel.grid_rowconfigure(
            1,
            weight=1,
        )

        # Search
        self.search_frame = ctk.CTkFrame(
            self.records_panel,
            fg_color="transparent",
        )

        self.search_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(20, 10),
        )

        self.search_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search by username, role or status",
            height=38,
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10),
        )

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=90,
            height=38,
            command=self.search_users,
        )

        self.search_button.grid(
            row=0,
            column=1,
            padx=(0, 8),
        )

        self.refresh_button = ctk.CTkButton(
            self.search_frame,
            text="Refresh",
            width=90,
            height=38,
            command=self.load_users,
        )

        self.refresh_button.grid(
            row=0,
            column=2,
        )

        # Records title
        self.records_title = ctk.CTkLabel(
            self.records_panel,
            text="User Accounts",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        )

        self.records_title.grid(
            row=1,
            column=0,
            sticky="nw",
            padx=25,
            pady=(5, 10),
        )

        self.records_scroll = ctk.CTkScrollableFrame(
            self.records_panel,
        )

        self.records_scroll.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20),
        )

        self.records_panel.grid_rowconfigure(
            2,
            weight=1,
        )

        self.records_scroll.grid_columnconfigure(
            0,
            weight=1,
        )

    # =========================================================
    # LOAD USERS
    # =========================================================

    def load_users(self):
        try:
            users = get_all_users()

            self.selected_user_id = None
            self.clear_account_fields()
            self.set_action_buttons_disabled()

            self.display_users(users)

        except Exception as error:
            messagebox.showerror(
                "User Management",
                f"Unable to load users:\n{error}",
            )

    # =========================================================
    # SEARCH USERS
    # =========================================================

    def search_users(self):
        search_text = self.search_entry.get().strip().lower()

        if not search_text:
            self.load_users()
            return

        try:
            users = get_all_users()

            filtered_users = []

            for user in users:
                status = (
                    "active"
                    if user["is_active"]
                    else "inactive"
                )

                if (
                    search_text in user["username"].lower()
                    or search_text in user["role"].lower()
                    or search_text in status
                ):
                    filtered_users.append(user)

            self.display_users(filtered_users)

        except Exception as error:
            messagebox.showerror(
                "User Search",
                f"Unable to search users:\n{error}",
            )

    # =========================================================
    # DISPLAY USERS
    # =========================================================

    def display_users(self, users):
        for widget in self.records_scroll.winfo_children():
            widget.destroy()

        if not users:
            empty_label = ctk.CTkLabel(
                self.records_scroll,
                text="No user records found.",
                font=ctk.CTkFont(size=15),
            )

            empty_label.grid(
                row=0,
                column=0,
                padx=20,
                pady=30,
            )

            return

        header = ctk.CTkFrame(
            self.records_scroll,
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=(0, 5),
        )

        columns = [
            ("ID", 0),
            ("Username", 1),
            ("Role", 2),
            ("Status", 3),
        ]

        for text, column in columns:
            header.grid_columnconfigure(
                column,
                weight=1,
            )

            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
                anchor="w",
            )

            label.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=8,
                pady=8,
            )

        for row_index, user in enumerate(
            users,
            start=1,
        ):
            self.create_user_row(
                row_index,
                user,
            )

    # =========================================================
    # USER ROW
    # =========================================================

    def create_user_row(self, row_index, user):
        row_frame = ctk.CTkFrame(
            self.records_scroll,
            fg_color=("gray92", "gray17"),
        )

        row_frame.grid(
            row=row_index,
            column=0,
            sticky="ew",
            padx=5,
            pady=3,
        )

        for column in range(4):
            row_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        status = (
            "Active"
            if user["is_active"]
            else "Inactive"
        )

        values = [
            user["id"],
            user["username"],
            user["role"],
            status,
        ]

        for column, value in enumerate(values):
            label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                anchor="w",
                font=ctk.CTkFont(size=12),
            )

            label.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=8,
                pady=9,
            )

            label.bind(
                "<Button-1>",
                lambda event, selected=user:
                self.select_user(selected),
            )

        row_frame.bind(
            "<Button-1>",
            lambda event, selected=user:
            self.select_user(selected),
        )

    # =========================================================
    # SELECT USER
    # =========================================================

    def select_user(self, user):
        self.selected_user_id = user["id"]

        status = (
            "Active"
            if user["is_active"]
            else "Inactive"
        )

        self.set_field_value(
            self.username_entry,
            user["username"],
        )

        self.set_field_value(
            self.role_entry,
            user["role"],
        )

        self.set_field_value(
            self.status_entry,
            status,
        )

        self.info_label.configure(
            text=(
                f"Selected User: {user['username']}\n"
                f"Role: {user['role']}\n"
                f"Account status: {status}"
            ),
        )

        if user["is_active"]:
            self.activate_button.configure(
                state="disabled",
            )

            self.deactivate_button.configure(
                state="normal",
            )

        else:
            self.activate_button.configure(
                state="normal",
            )

            self.deactivate_button.configure(
                state="disabled",
            )

    # =========================================================
    # ACTIVATE USER
    # =========================================================

    def activate_selected_user(self):
        if self.selected_user_id is None:
            return

        confirmation = messagebox.askyesno(
            "Confirm Activation",
            "Are you sure you want to activate this user?",
        )

        if not confirmation:
            return

        try:
            activated = activate_user(
                self.selected_user_id,
            )

            if not activated:
                messagebox.showwarning(
                    "Activate User",
                    "User could not be activated.",
                )
                return

            messagebox.showinfo(
                "Success",
                "User activated successfully.",
            )

            self.load_users()

        except Exception as error:
            messagebox.showerror(
                "Activate User",
                f"Unable to activate user:\n{error}",
            )

    # =========================================================
    # DEACTIVATE USER
    # =========================================================

    def deactivate_selected_user(self):
        if self.selected_user_id is None:
            return

        if self.selected_user_id == self.user["id"]:
            messagebox.showwarning(
                "Action Not Allowed",
                "You cannot deactivate your own account.",
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Deactivation",
            "Are you sure you want to deactivate this user?",
        )

        if not confirmation:
            return

        try:
            deactivated = deactivate_user(
                self.selected_user_id,
            )

            if not deactivated:
                messagebox.showwarning(
                    "Deactivate User",
                    "User could not be deactivated.",
                )
                return

            messagebox.showinfo(
                "Success",
                "User deactivated successfully.",
            )

            self.load_users()

        except Exception as error:
            messagebox.showerror(
                "Deactivate User",
                f"Unable to deactivate user:\n{error}",
            )

    # =========================================================
    # CLEAR SELECTION
    # =========================================================

    def clear_selection(self):
        self.selected_user_id = None

        self.clear_account_fields()
        self.set_action_buttons_disabled()

        self.info_label.configure(
            text=(
                "Select a user from the records panel "
                "to manage the account status."
            ),
        )

    def clear_account_fields(self):
        self.username_entry.delete(0, "end")
        self.role_entry.delete(0, "end")
        self.status_entry.delete(0, "end")

    def set_field_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value))

    def set_action_buttons_disabled(self):
        self.activate_button.configure(
            state="disabled",
        )

        self.deactivate_button.configure(
            state="disabled",
        )