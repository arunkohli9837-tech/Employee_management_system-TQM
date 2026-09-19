import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime

from services.backup_service import (
    create_backup,
    list_backups,
    validate_backup,
    restore_backup,
)


class BackupManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back=None):
        super().__init__(master)

        self.user = user
        self.on_back = on_back
        self.selected_backup = ctk.StringVar(value="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_actions()
        self.create_backup_list()

        self.refresh_backups()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):
        header = ctk.CTkFrame(self)
        header.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10),
            sticky="ew",
        )

        title = ctk.CTkLabel(
            header,
            text="Backup & Recovery",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )
        title.pack(
            side="left",
            padx=15,
            pady=15,
        )

    # =========================================================
    # ACTIONS
    # =========================================================

    def create_actions(self):
        action_frame = ctk.CTkFrame(self)
        action_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="ew",
        )

        for column in range(3):
            action_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        self.backup_button = ctk.CTkButton(
            action_frame,
            text="Create Backup",
            command=self.create_backup_action,
        )
        self.backup_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=15,
            sticky="ew",
        )

        self.refresh_button = ctk.CTkButton(
            action_frame,
            text="Refresh",
            command=self.refresh_backups,
        )
        self.refresh_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=15,
            sticky="ew",
        )

        self.restore_button = ctk.CTkButton(
            action_frame,
            text="Restore Selected",
            command=self.restore_selected,
        )
        self.restore_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=15,
            sticky="ew",
        )

    # =========================================================
    # BACKUP LIST
    # =========================================================

    def create_backup_list(self):
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Available Backups",
        )
        self.list_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=(10, 20),
            sticky="nsew",
        )

        self.list_frame.grid_columnconfigure(
            1,
            weight=1,
        )

    # =========================================================
    # BACKUP TYPE
    # =========================================================

    def get_backup_type(self, backup_path):
        name = backup_path.name.lower()

        if "_auto_" in name:
            return "Automatic"

        if "_safety_" in name:
            return "Safety"

        return "Manual"

    # =========================================================
    # DATE / TIME
    # =========================================================

    def get_backup_datetime(self, backup_path):
        try:
            modified_time = datetime.fromtimestamp(
                backup_path.stat().st_mtime
            )

            return modified_time.strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )

        except OSError:
            return "Unknown"

    # =========================================================
    # FILE SIZE
    # =========================================================

    def get_backup_size(self, backup_path):
        try:
            size = backup_path.stat().st_size

            if size < 1024:
                return f"{size} B"

            if size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"

            return f"{size / (1024 * 1024):.1f} MB"

        except OSError:
            return "Unknown"

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_backups(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.selected_backup.set("")

        backups = list_backups()

        if not backups:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No backups available.",
                font=ctk.CTkFont(size=14),
            )
            empty_label.grid(
                row=1,
                column=0,
                columnspan=6,
                padx=20,
                pady=30,
            )
            return

        # -----------------------------------------------------
        # TABLE HEADER
        # -----------------------------------------------------

        headers = [
            ("", 0),
            ("Type", 1),
            ("Backup File", 2),
            ("Date / Time", 3),
            ("Size", 4),
            ("Status", 5),
        ]

        for text, column in headers:
            label = ctk.CTkLabel(
                self.list_frame,
                text=text,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold",
                ),
                anchor="w",
            )

            label.grid(
                row=0,
                column=column,
                padx=8,
                pady=(5, 10),
                sticky="w",
            )

        # -----------------------------------------------------
        # BACKUP RECORDS
        # -----------------------------------------------------

        for row_index, backup_path in enumerate(
            backups,
            start=1,
        ):
            backup_type = self.get_backup_type(
                backup_path
            )

            backup_datetime = self.get_backup_datetime(
                backup_path
            )

            backup_size = self.get_backup_size(
                backup_path
            )

            is_valid = validate_backup(
                backup_path
            )

            status = "Valid" if is_valid else "Invalid"

            # Radio button
            radio = ctk.CTkRadioButton(
                self.list_frame,
                text="",
                variable=self.selected_backup,
                value=str(backup_path),
                width=25,
            )

            radio.grid(
                row=row_index,
                column=0,
                padx=8,
                pady=7,
            )

            # Type
            type_label = ctk.CTkLabel(
                self.list_frame,
                text=backup_type,
                anchor="w",
            )

            type_label.grid(
                row=row_index,
                column=1,
                padx=8,
                pady=7,
                sticky="w",
            )

            # File name
            file_label = ctk.CTkLabel(
                self.list_frame,
                text=backup_path.name,
                anchor="w",
            )

            file_label.grid(
                row=row_index,
                column=2,
                padx=8,
                pady=7,
                sticky="ew",
            )

            # Date / Time
            date_label = ctk.CTkLabel(
                self.list_frame,
                text=backup_datetime,
                anchor="w",
            )

            date_label.grid(
                row=row_index,
                column=3,
                padx=8,
                pady=7,
                sticky="w",
            )

            # Size
            size_label = ctk.CTkLabel(
                self.list_frame,
                text=backup_size,
                anchor="w",
            )

            size_label.grid(
                row=row_index,
                column=4,
                padx=8,
                pady=7,
                sticky="w",
            )

            # Status
            status_label = ctk.CTkLabel(
                self.list_frame,
                text=status,
                anchor="w",
            )

            status_label.grid(
                row=row_index,
                column=5,
                padx=8,
                pady=7,
                sticky="w",
            )

    # =========================================================
    # CREATE MANUAL BACKUP
    # =========================================================

    def create_backup_action(self):
        try:
            backup_path = create_backup()

            self.refresh_backups()

            messagebox.showinfo(
                "Backup Created",
                "Backup created successfully.\n\n"
                f"{backup_path.name}",
            )

        except Exception as error:
            messagebox.showerror(
                "Backup Failed",
                f"Unable to create backup.\n\n{error}",
            )

    # =========================================================
    # RESTORE
    # =========================================================

    def restore_selected(self):
        selected = self.selected_backup.get()

        if not selected:
            messagebox.showwarning(
                "Restore",
                "Please select a backup first.",
            )
            return

        if not messagebox.askyesno(
            "Confirm Restore",
            "Restoring this backup will replace the current "
            "database.\n\n"
            "A safety backup will be created automatically "
            "before restoration.\n\n"
            "Do you want to continue?",
        ):
            return

        try:
            backup_path = Path(selected)

            if not validate_backup(
                backup_path
            ):
                messagebox.showerror(
                    "Invalid Backup",
                    "The selected backup failed the SQLite "
                    "integrity check.",
                )
                return

            safety_backup = restore_backup(
                backup_path
            )

            self.refresh_backups()

            messagebox.showinfo(
                "Restore Successful",
                "Database restored successfully.\n\n"
                f"Safety backup:\n{safety_backup.name}",
            )

        except Exception as error:
            messagebox.showerror(
                "Restore Failed",
                "Unable to restore the selected backup.\n\n"
                f"{error}",
            )