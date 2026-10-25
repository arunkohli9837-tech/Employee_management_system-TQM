import customtkinter as ctk
from tkinter import messagebox

from services.user_service import (
    get_all_users,
    activate_user,
    deactivate_user,
    update_user,
)
from services.auth_service import create_user


class UserManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back
        self.selected_user_id = None

        self.configure(fg_color=("gray95", "gray10"))

        self.grid_columnconfigure(0, weight=0, minsize=0)
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
        """Create a compact account editor embedded on the left of the table."""
        self.account_panel = ctk.CTkFrame(self, corner_radius=14, width=260)
        self.account_panel.grid(
            row=1, column=0, sticky="nsew", padx=(24, 8), pady=(0, 24)
        )
        self.account_panel.grid_propagate(False)
        self.account_panel.grid_columnconfigure(0, weight=1)
        self.account_panel.grid_remove()

        self.account_title = ctk.CTkLabel(
            self.account_panel, text="Add User",
            font=ctk.CTkFont(size=21, weight="bold")
        )
        self.account_title.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 6))

        self.account_fields = ctk.CTkScrollableFrame(self.account_panel, fg_color="transparent")
        self.account_fields.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 4))
        self.account_fields.grid_columnconfigure(0, weight=1)
        self.account_panel.grid_rowconfigure(1, weight=1)

        self.username_entry = self._create_labeled_entry(0, "Username", "Enter username")
        self.role_entry = self._create_labeled_entry(1, "User Role", "e.g. admin, hr, employee")
        self.password_entry = self._create_labeled_entry(2, "Password", "Enter password", show="*")
        self.status_entry = self._create_labeled_entry(3, "Account Status", "Status appears when selected")
        self.status_entry.configure(state="disabled")

        self.info_label = ctk.CTkLabel(
            self.account_panel,
            text="Add a new user or select a user to update.",
            text_color=("gray45", "gray65"), anchor="w", justify="left", wraplength=260,
        )
        self.info_label.grid(row=2, column=0, sticky="ew", padx=14, pady=(4, 8))

        self.action_frame = ctk.CTkFrame(self.account_panel, fg_color="transparent")
        self.action_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(4, 14))
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=1)
        self.add_button = ctk.CTkButton(self.action_frame, text="Add User", height=35, command=self.add_user)
        self.add_button.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.update_button = ctk.CTkButton(
            self.action_frame, text="Update User", height=35, state="disabled",
            command=self.update_selected_user,
        )
        self.update_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(7, 0))
        self.clear_button = ctk.CTkButton(
            self.action_frame, text="Cancel / Hide", height=35,
            fg_color="#4b5563", hover_color="#374151", command=self.clear_selection,
        )
        self.clear_button.grid(row=0, column=1, sticky="ew", padx=(4, 0))

    def _create_labeled_entry(self, row, label_text, placeholder, show=None):
        field = ctk.CTkFrame(self.account_fields, fg_color="transparent")
        field.grid(row=row, column=0, sticky="ew", padx=4, pady=2)
        field.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(field, text=label_text, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).grid(
            row=0, column=0, sticky="ew", pady=(0, 3)
        )
        options = {"height": 30, "placeholder_text": placeholder}
        if show:
            options["show"] = show
        entry = ctk.CTkEntry(field, **options)
        entry.grid(row=1, column=0, sticky="ew")
        return entry

    def open_add_form(self):
        self.clear_account_fields()
        self.selected_user_id = None
        self.update_toolbar_button.configure(state="disabled")
        self.info_label.configure(text="Create a new user account.")
        self.account_title.configure(text="Add User")
        self.add_button.configure(state="normal")
        self.update_button.configure(state="disabled")
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.account_panel.grid()
        self.account_panel.lift()

    def open_update_form(self):
        if self.selected_user_id is None:
            messagebox.showwarning("No User Selected", "Please select a user before updating.")
            return
        self.account_title.configure(text="Update User")
        self.add_button.configure(state="disabled")
        self.update_button.configure(state="normal")
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.account_panel.grid()
        self.account_panel.lift()

    # =========================================================
    # RIGHT RECORDS PANEL
    # =========================================================

    def create_records_panel(self):
        self.records_panel = ctk.CTkFrame(self)

        self.records_panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 24),
            pady=(0, 24),
        )

        self.records_panel.grid_columnconfigure(
            0,
            weight=1,
        )

        self.records_panel.grid_rowconfigure(
            2,
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

        self.add_toolbar_button = ctk.CTkButton(
            self.search_frame, text="+ Add User", width=105, height=38,
            command=self.open_add_form,
        )
        self.add_toolbar_button.grid(row=0, column=3, padx=(8, 0))
        self.update_toolbar_button = ctk.CTkButton(
            self.search_frame, text="Update Selected", width=135, height=38,
            state="disabled", command=self.open_update_form,
        )
        self.update_toolbar_button.grid(row=0, column=4, padx=(8, 0))

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

            self.selected_user_id = None
            self.clear_account_fields()
            self.set_action_buttons_disabled()
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

        columns = [("ID", 0), ("Username", 1), ("Role", 2), ("Status / Action", 3)]
        # Use the same fixed column geometry for the header and every data row.
        # The compact table avoids spreading Username and Role across the full
        # window, which caused the previous excessive gap.
        widths = [60, 190, 150, 160]
        self.user_column_widths = widths
        for text, column in columns:
            header.grid_columnconfigure(column, weight=0, minsize=widths[column])

            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
                anchor="w",
                width=widths[column] - 16,
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

        # Match the header's exact column widths so each value stays beneath
        # its own heading without an oversized Username-to-Role gap.
        widths = self.user_column_widths
        for column, width in enumerate(widths):
            row_frame.grid_columnconfigure(column, weight=0, minsize=width)

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
            if column == 3:
                is_active = bool(user["is_active"])
                action = ctk.CTkOptionMenu(
                    row_frame,
                    values=["Active", "Deactivate"] if is_active else ["Inactive", "Activate"],
                    width=88, height=25,
                    fg_color="#2563a6" if is_active else "#b91c1c",
                    button_color="#1d4ed8" if is_active else "#991b1b",
                    button_hover_color="#1e40af" if is_active else "#7f1d1d",
                    command=lambda choice, selected=user: self._user_status_choice(selected, choice),
                )
                action.set("Active" if is_active else "Inactive")
                action.grid(row=0, column=column, sticky="w", padx=5, pady=5)
                continue
            label = ctk.CTkLabel(
                row_frame, text=str(value), anchor="w", width=widths[column] - 12,
                font=ctk.CTkFont(size=11),
            )
            label.grid(row=0, column=column, sticky="ew", padx=8, pady=9)
            label.bind("<Button-1>", lambda event, selected=user: self.select_user(selected))

        row_frame.bind(
            "<Button-1>",
            lambda event, selected=user:
            self.select_user(selected),
        )

    def _user_status_choice(self, user, choice):
        # Refresh the row from persisted data after the confirmation/action.
        # This resets the menu if the user cancels or the operation fails.
        if choice == "Activate":
            self._change_user_status(user, True)
        elif choice == "Deactivate":
            self._change_user_status(user, False)
        elif choice == "Active" or choice == "Inactive":
            self.load_users()

    def _change_user_status(self, user, activate):
        self.select_user(user)
        if activate:
            self.activate_selected_user()
        else:
            self.deactivate_selected_user()

    # =========================================================
    # SELECT USER
    # =========================================================

    def select_user(self, user):
        # Clicking a table record hides the editor; use Update Selected to reopen it.
        self.account_panel.grid_remove()
        self.grid_columnconfigure(0, weight=0, minsize=0)
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

        self.status_entry.configure(state="normal")
        self.set_field_value(self.status_entry, status)
        self.status_entry.configure(state="disabled")

        self.password_entry.delete(0, "end")

        self.info_label.configure(
            text=(
                f"Selected User: {user['username']}\n"
                f"Role: {user['role']}\n"
                f"Account status: {status}"
            ),
        )

        self.update_button.configure(state="normal")
        self.update_toolbar_button.configure(state="normal")

    # =========================================================
    # ADD USER
    # =========================================================

    def add_user(self):
        username = self.username_entry.get().strip()
        role = self.role_entry.get().strip()
        password = self.password_entry.get()

        try:
            create_user(
                username=username,
                password=password,
                role=role,
                performed_by=self.user,
            )

            messagebox.showinfo(
                "Success",
                "User created successfully.",
            )

            self.clear_selection()
            self.load_users()

        except ValueError as error:
            messagebox.showwarning(
                "Validation Error",
                str(error),
            )

        except Exception as error:
            messagebox.showerror(
                "User Creation",
                f"Unable to create user:\n{error}",
            )

    # =========================================================
    # UPDATE USER
    # =========================================================

    def update_selected_user(self):
        if self.selected_user_id is None:
            messagebox.showwarning(
                "No User Selected",
                "Please select a user before updating.",
            )
            return

        username = self.username_entry.get().strip()
        role = self.role_entry.get().strip()
        password = self.password_entry.get()

        try:
            updated = update_user(
                user_id=self.selected_user_id,
                username=username,
                role=role,
                password=password,
                performed_by=self.user,
            )

            if not updated:
                messagebox.showwarning(
                    "Update User",
                    "User could not be updated.",
                )
                self._restore_selected_user_role()
                return

            messagebox.showinfo(
                "Success",
                "User updated successfully.",
            )

            self.clear_selection()
            self.load_users()

        except ValueError as error:
            messagebox.showwarning(
                "Validation Error",
                str(error),
            )
            self._restore_selected_user_role()

        except Exception as error:
            messagebox.showerror(
                "User Update",
                f"Unable to update user:\n{error}",
            )
            self._restore_selected_user_role()

    def _restore_selected_user_role(self):
        """Restore the role field from persisted data after a rejected/failed update."""
        if self.selected_user_id is None:
            return
        try:
            persisted_user = next(
                (item for item in get_all_users() if item["id"] == self.selected_user_id),
                None,
            )
            if persisted_user is not None:
                self.set_field_value(self.role_entry, persisted_user["role"])
        except Exception:
            # Keep the original validation/error feedback if a refresh also fails.
            pass

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
            self.load_users()
            return

        try:
            activated = activate_user(
                self.selected_user_id,
                performed_by=self.user,
            )

            if not activated:
                messagebox.showwarning(
                    "Activate User",
                    "User could not be activated.",
                )
                self.load_users()
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
            self.load_users()

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
            self.load_users()
            return

        confirmation = messagebox.askyesno(
            "Confirm Deactivation",
            "Are you sure you want to deactivate this user?",
        )

        if not confirmation:
            self.load_users()
            return

        try:
            deactivated = deactivate_user(
                self.selected_user_id,
                performed_by=self.user,
            )

            if not deactivated:
                messagebox.showwarning(
                    "Deactivate User",
                    "User could not be deactivated.",
                )
                self.load_users()
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
            self.load_users()

    # =========================================================
    # CLEAR SELECTION
    # =========================================================

    def clear_selection(self):
        self.selected_user_id = None

        self.clear_account_fields()
        self.set_action_buttons_disabled()

        self.info_label.configure(text="Add a new user or update the selected account.")
        self.add_button.configure(state="normal")
        self.update_button.configure(state="disabled")
        self.update_toolbar_button.configure(state="disabled")
        if hasattr(self, "account_panel"):
            self.account_panel.grid_remove()
            self.grid_columnconfigure(0, weight=0, minsize=0)

    def clear_account_fields(self):
        self.username_entry.delete(0, "end")
        self.role_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.status_entry.configure(state="normal")
        self.status_entry.delete(0, "end")
        self.status_entry.configure(state="disabled")

    def set_field_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value))

    def set_action_buttons_disabled(self):
        self.update_button.configure(state="disabled")
        self.update_toolbar_button.configure(state="disabled")
