import customtkinter as ctk
from tkinter import messagebox

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
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.pack(
            side="left",
            padx=15,
            pady=15,
        )

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

    def refresh_backups(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        backups = list_backups()

        if not backups:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No backups available.",
            )
            empty_label.pack(
                padx=20,
                pady=20,
            )
            return

        for backup_path in backups:
            radio = ctk.CTkRadioButton(
                self.list_frame,
                text=backup_path.name,
                variable=self.selected_backup,
                value=str(backup_path),
            )
            radio.pack(
                anchor="w",
                padx=15,
                pady=8,
            )

    def create_backup_action(self):
        try:
            backup_path = create_backup()

            self.refresh_backups()

            messagebox.showinfo(
                "Backup Created",
                f"Backup created successfully.\n\n"
                f"{backup_path.name}",
            )

        except Exception as error:
            messagebox.showerror(
                "Backup Failed",
                f"Unable to create backup.\n\n{error}",
            )

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
            backup_path = selected

            if not validate_backup(
                __import__("pathlib").Path(backup_path)
            ):
                messagebox.showerror(
                    "Invalid Backup",
                    "The selected backup failed the SQLite "
                    "integrity check.",
                )
                return

            safety_backup = restore_backup(
                __import__("pathlib").Path(backup_path)
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
                f"Unable to restore the selected backup.\n\n"
                f"{error}",
            )