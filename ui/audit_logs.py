import customtkinter as ctk

from services.audit_service import (
    get_all_audit_logs,
    search_audit_logs,
)


class AuditLogsFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back
        self.current_logs = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_controls()
        self.create_log_table()

        self.load_logs()

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
            sticky="ew",
            padx=30,
            pady=(25, 10),
        )

        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Audit Logs",
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
            anchor="w",
        )
        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Trace system activities, successful operations and failures.",
            font=ctk.CTkFont(size=14),
            text_color=("gray45", "gray65"),
            anchor="w",
        )
        self.subtitle_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 0),
        )

    # =========================================================
    # CONTROLS
    # =========================================================

    def create_controls(self):
        self.controls = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=("white", "#181818"),
        )
        self.controls.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=30,
            pady=10,
        )

        self.controls.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.controls,
            placeholder_text="Search username, action, target or description",
            height=40,
        )
        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(15, 10),
            pady=15,
        )

        self.status_menu = ctk.CTkOptionMenu(
            self.controls,
            values=[
                "All",
                "Success",
                "Failed",
            ],
            width=145,
            height=40,
            command=self.filter_by_status,
        )
        self.status_menu.grid(
            row=0,
            column=1,
            padx=5,
            pady=15,
        )

        self.search_button = ctk.CTkButton(
            self.controls,
            text="Search",
            width=100,
            height=40,
            command=self.search_logs,
        )
        self.search_button.grid(
            row=0,
            column=2,
            padx=5,
            pady=15,
        )

        self.refresh_button = ctk.CTkButton(
            self.controls,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_logs,
        )
        self.refresh_button.grid(
            row=0,
            column=3,
            padx=(5, 15),
            pady=15,
        )

    # =========================================================
    # LOG TABLE
    # =========================================================

    def create_log_table(self):
        self.table_frame = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=("white", "#181818"),
        )
        self.table_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(5, 10),
        )

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(
            self.table_frame,
            wrap="none",
            font=ctk.CTkFont(size=13),
        )
        self.log_textbox.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10,
        )

        self.log_textbox.configure(
            state="disabled"
        )

        self.bottom_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.bottom_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 20),
        )

        self.status_label = ctk.CTkLabel(
            self.bottom_frame,
            text="",
            font=ctk.CTkFont(size=13),
        )
        self.status_label.pack(
            side="left",
        )

        self.back_button = ctk.CTkButton(
            self.bottom_frame,
            text="Back to Dashboard",
            width=160,
            command=self.on_back,
        )
        self.back_button.pack(
            side="right",
        )

    # =========================================================
    # DATA
    # =========================================================

    def load_logs(self):
        try:
            self.current_logs = get_all_audit_logs()
            self.apply_status_filter(self.current_logs)

        except Exception as error:
            self.current_logs = []
            self.display_logs([])

            self.status_label.configure(
                text=f"Unable to load audit logs: {error}"
            )

    def search_logs(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.load_logs()
            return

        try:
            self.current_logs = search_audit_logs(
                search_term
            )

            self.apply_status_filter(
                self.current_logs
            )

        except Exception as error:
            self.current_logs = []
            self.display_logs([])

            self.status_label.configure(
                text=f"Unable to search audit logs: {error}"
            )

    def filter_by_status(self, selected_status):
        self.apply_status_filter(
            self.current_logs
        )

    def apply_status_filter(self, logs):
        selected_status = self.status_menu.get()

        if selected_status == "All":
            filtered_logs = logs

        else:
            filtered_logs = [
                log
                for log in logs
                if str(
                    log.get("status", "")
                ).lower()
                == selected_status.lower()
            ]

        self.display_logs(
            filtered_logs
        )

    # =========================================================
    # DISPLAY
    # =========================================================

    def display_logs(self, logs):
        self.log_textbox.configure(
            state="normal"
        )

        self.log_textbox.delete(
            "1.0",
            "end",
        )

        if not logs:
            self.log_textbox.insert(
                "end",
                "No audit log records found.\n",
            )

            self.status_label.configure(
                text="No records found."
            )

            self.log_textbox.configure(
                state="disabled"
            )

            return

        header = (
            f"{'ID':<6}"
            f"{'Username':<18}"
            f"{'Action':<25}"
            f"{'Target':<20}"
            f"{'Status':<12}"
            f"{'Date / Time':<22}"
            f"Description\n"
        )

        separator = "-" * 150 + "\n"

        self.log_textbox.insert(
            "end",
            header,
        )

        self.log_textbox.insert(
            "end",
            separator,
        )

        for log in logs:
            target_type = str(
                log.get("target_type", "")
            )

            target_id = log.get(
                "target_id",
                "",
            )

            if target_type:
                target = f"{target_type} #{target_id}"
            else:
                target = str(target_id)

            line = (
                f"{str(log.get('id', '')):<6}"
                f"{str(log.get('username', ''))[:17]:<18}"
                f"{str(log.get('action', ''))[:24]:<25}"
                f"{target[:19]:<20}"
                f"{str(log.get('status', '')):<12}"
                f"{str(log.get('created_at', '')):<22}"
                f"{str(log.get('description', ''))}\n"
            )

            self.log_textbox.insert(
                "end",
                line,
            )

        self.status_label.configure(
            text=f"{len(logs)} audit log record(s) displayed."
        )

        self.log_textbox.configure(
            state="disabled"
        )