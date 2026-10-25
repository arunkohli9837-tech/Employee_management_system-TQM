import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from services.employee_service import (
    get_all_employees,
    search_employees,
    create_employee,
    update_employee,
    deactivate_employee,
)


class EmployeeManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back
        self.selected_employee_id = None

        self.entries = {}

        self.grid_columnconfigure(0, weight=0, minsize=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_form_panel()
        self.create_records_panel()

        self.load_employees()

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    def create_header(self):
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(25, 15),
        )

        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Employee Management",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

    # ---------------------------------------------------------
    # LEFT FORM
    # ---------------------------------------------------------

    def create_form_panel(self):
        """Build a compact form embedded on the left side of the records table."""
        self.form_panel = ctk.CTkFrame(self, corner_radius=14, width=260)
        self.form_panel.grid(
            row=1, column=0, sticky="nsew", padx=(24, 10), pady=(0, 24)
        )
        self.form_panel.grid_propagate(False)
        self.form_panel.grid_columnconfigure(0, weight=1)
        self.form_panel.grid_rowconfigure(1, weight=1)
        self.form_panel.grid_rowconfigure(0, weight=0)
        self.form_panel.grid_remove()

        self.form_title = ctk.CTkLabel(
            self.form_panel,
            text="Add Employee",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.form_title.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 5))

        self.form_scroll = ctk.CTkScrollableFrame(
            self.form_panel, fg_color="transparent"
        )
        self.form_scroll.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 4))
        self.form_scroll.grid_columnconfigure(0, weight=1)
        self.create_form_fields()

        self.action_frame = ctk.CTkFrame(self.form_panel, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=(2, 8))
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=1)

        self.add_button = ctk.CTkButton(
            self.action_frame, text="Add Employee", height=36, command=self.add_employee
        )
        self.add_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.update_button = ctk.CTkButton(
            self.action_frame, text="Update Employee", height=36, state="disabled",
            command=self.update_selected_employee,
        )
        self.update_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(7, 0))
        self.clear_button = ctk.CTkButton(
            self.action_frame, text="Cancel / Hide", height=36,
            fg_color="#4b5563", hover_color="#374151", command=self.clear_form,
        )
        self.clear_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def open_add_form(self):
        self.selected_employee_id = None
        self.clear_form(hide_panel=False)
        self.form_title.configure(text="Add Employee")
        self.add_button.configure(state="normal")
        self.update_button.configure(state="disabled")
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.form_panel.grid()
        self.form_panel.lift()

    def open_update_form(self):
        if self.selected_employee_id is None:
            messagebox.showwarning("No Employee Selected", "Please select an employee before updating.")
            return
        self.form_title.configure(text="Update Employee")
        self.add_button.configure(state="disabled")
        self.update_button.configure(state="normal")
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.form_panel.grid()
        self.form_panel.lift()

    def create_form_fields(self):
        fields = [
            ("employee_code", "Employee Code"),
            ("full_name", "Full Name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("department", "Department"),
            ("designation", "Designation"),
            ("salary", "Salary"),
            ("joining_date", "Joining Date (DD-MM-YYYY)"),
        ]
        self.entries = {}
        for index, (key, label_text) in enumerate(fields):
            row, column = index, 0
            field = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
            field.grid(row=row, column=column, sticky="ew", padx=4, pady=2)
            field.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(field, text=label_text, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=0, column=0, sticky="ew", pady=(0, 2)
            )
            entry = ctk.CTkEntry(field, height=30, placeholder_text=f"Enter {label_text.lower()}")
            entry.grid(row=1, column=0, sticky="ew")
            self.entries[key] = entry

    # ---------------------------------------------------------
    # RIGHT RECORDS PANEL
    # ---------------------------------------------------------

    def create_records_panel(self):
        self.records_panel = ctk.CTkFrame(self)
        self.records_panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 24),
            pady=(0, 24),
        )

        self.records_panel.grid_columnconfigure(0, weight=1)
        self.records_panel.grid_rowconfigure(2, weight=1)

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

        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search by name, code or email",
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
            command=self.search_employee_records,
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
            command=self.load_employees,
        )
        self.refresh_button.grid(
            row=0,
            column=2,
        )

        self.add_toolbar_button = ctk.CTkButton(
            self.search_frame, text="+ Add Employee", width=125, height=38,
            command=self.open_add_form,
        )
        self.add_toolbar_button.grid(row=0, column=3, padx=(8, 0))

        self.update_toolbar_button = ctk.CTkButton(
            self.search_frame, text="Update Selected", width=135, height=38,
            state="disabled", command=self.open_update_form,
        )
        self.update_toolbar_button.grid(row=0, column=4, padx=(8, 0))

        self.records_title = ctk.CTkLabel(
            self.records_panel,
            text="Employee Records",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.records_title.grid(
            row=1,
            column=0,
            sticky="w",
            padx=25,
            pady=(5, 10),
        )

        # A Canvas owns both scroll directions. CTkScrollableFrame only provides
        # vertical scrolling and resizes its inner frame to the viewport, which
        # made the previous horizontal scrollbar appear without moving the table.
        self.table_viewport = ctk.CTkFrame(self.records_panel, fg_color="transparent")
        self.table_viewport.grid(
            row=2, column=0, sticky="nsew", padx=20, pady=(0, 10)
        )
        self.table_viewport.grid_rowconfigure(0, weight=1)
        self.table_viewport.grid_columnconfigure(0, weight=1)

        canvas_bg = self.records_panel._apply_appearance_mode(
            self.records_panel.cget("fg_color")
        )
        self.records_canvas = tk.Canvas(
            self.table_viewport, highlightthickness=0, borderwidth=0,
            background=canvas_bg,
        )
        self.records_canvas.grid(row=0, column=0, sticky="nsew")

        self.records_vscroll = ctk.CTkScrollbar(
            self.table_viewport, orientation="vertical",
            command=self.records_canvas.yview,
        )
        self.records_vscroll.grid(row=0, column=1, sticky="ns")
        self.records_hscroll = ctk.CTkScrollbar(
            self.table_viewport, orientation="horizontal",
            command=self.records_canvas.xview,
        )
        self.records_hscroll.grid(row=1, column=0, sticky="ew")
        self.records_canvas.configure(
            xscrollcommand=self.records_hscroll.set,
            yscrollcommand=self.records_vscroll.set,
        )

        # Keep the table wider than the viewport when required; headers and rows
        # share this one content frame and therefore scroll in exact alignment.
        # The embedded table frame must retain its full content width instead of
        # being resized to the visible Canvas viewport. The exact width is
        # recalculated from the column definitions in display_employees().
        self.employee_table_width = 1180
        self.records_scroll = ctk.CTkFrame(self.records_canvas, fg_color="transparent")
        self.records_scroll.configure(width=self.employee_table_width)
        self.records_scroll.grid_columnconfigure(
            0, weight=0, minsize=self.employee_table_width
        )
        self._records_window = self.records_canvas.create_window(
            (0, 0), window=self.records_scroll, anchor="nw",
            width=self.employee_table_width,
        )
        self.records_scroll.bind("<Configure>", self._update_employee_scroll_region)
        self.records_canvas.bind("<Configure>", self._update_employee_scroll_region)

    # ---------------------------------------------------------
    # EMPLOYEE RECORD DISPLAY
    # ---------------------------------------------------------

    def _update_employee_scroll_region(self, _event=None):
        # The Canvas window's bounding box can be narrower than the table's
        # requested content when child columns extend past the embedded frame.
        # Keep the window at the existing table width and include that full
        # width in the scroll region so xview scrolls the actual table content.
        table_width = max(
            self.employee_table_width,
            self.records_scroll.winfo_reqwidth(),
        )
        self.records_canvas.itemconfigure(self._records_window, width=table_width)

        bounds = self.records_canvas.bbox("all")
        content_height = bounds[3] if bounds else self.records_scroll.winfo_reqheight()
        self.records_canvas.configure(
            scrollregion=(0, 0, table_width, max(content_height, self.records_canvas.winfo_height()))
        )

    def display_employees(self, employees):
        for widget in self.records_scroll.winfo_children():
            widget.destroy()

        if not employees:
            empty_label = ctk.CTkLabel(
                self.records_scroll,
                text="No employee records found.",
                font=ctk.CTkFont(size=15),
            )
            empty_label.grid(
                row=0,
                column=0,
                padx=20,
                pady=30,
            )
            return

        header = ctk.CTkFrame(self.records_scroll)
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=(0, 5),
        )

        # Keep the same column widths in the header and every record row.
        # This prevents values from appearing far apart or wrapping awkwardly.
        columns = [
            ("Code", 0, 100),
            ("Name", 1, 170),
            ("Email", 2, 240),
            ("Department", 3, 150),
            ("Designation", 4, 210),
            ("Salary", 5, 120),
            ("Status / Action", 6, 170),
        ]
        self.employee_column_widths = [width for _, _, width in columns]

        # Keep the Canvas window at least as wide as all columns combined.
        # The same width is used by the header and every row so columns never
        # disappear or shift when the viewport is narrower than the table.
        self.employee_table_width = sum(self.employee_column_widths) + 20
        self.records_scroll.configure(width=self.employee_table_width)
        self.records_scroll.grid_columnconfigure(
            0, weight=0, minsize=self.employee_table_width
        )
        self.records_canvas.itemconfigure(
            self._records_window, width=self.employee_table_width
        )

        for text, column, width in columns:
            header.grid_columnconfigure(column, weight=0, minsize=width)

            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                width=width - 12,
            )
            label.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=6,
                pady=8,
            )

        for row_index, employee in enumerate(employees, start=1):
            self.create_employee_row(row_index, employee)
        self.records_scroll.update_idletasks()
        self.records_canvas.configure(scrollregion=self.records_canvas.bbox("all"))

    def create_employee_row(self, row_index, employee):
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

        for column, width in enumerate(self.employee_column_widths):
            row_frame.grid_columnconfigure(column, weight=0, minsize=width)

        values = [
            employee["employee_code"],
            employee["full_name"],
            employee["email"],
            employee["department"],
            employee["designation"],
            f"{employee['salary']:.2f}",
            employee["status"],
        ]

        for column, value in enumerate(values):
            if column == 6:
                is_active = employee["status"] == "Active"
                status_menu = ctk.CTkOptionMenu(
                    row_frame,
                    values=["Active", "Deactivate"] if is_active else ["Inactive"],
                    width=88, height=25,
                    fg_color="#2563a6" if is_active else "#b91c1c",
                    button_color="#1d4ed8" if is_active else "#991b1b",
                    button_hover_color="#1e40af" if is_active else "#7f1d1d",
                    command=lambda choice, emp=employee: self._employee_status_choice(emp, choice),
                )
                status_menu.set("Active" if is_active else "Inactive")
                status_menu.grid(row=0, column=column, sticky="w", padx=5, pady=5)
                continue
            label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                anchor="w",
                width=self.employee_column_widths[column] - 10,
                font=ctk.CTkFont(size=11),
            )
            label.grid(row=0, column=column, sticky="ew", padx=6, pady=8)
            label.bind("<Button-1>", lambda event, emp=employee: self.select_employee(emp))

        row_frame.bind(
            "<Button-1>",
            lambda event, emp=employee: self.select_employee(emp),
        )

    def _employee_status_choice(self, employee, choice):
        # OptionMenu changes its displayed value before the operation completes.
        # Reload from the database afterwards so cancel/failure never leaves a
        # misleading status selected in the row.
        if choice == "Deactivate":
            self.select_employee(employee)
            self.deactivate_selected_employee()
        elif choice == "Active":
            self.load_employees()

    def _deactivate_employee_row(self, employee):
        self._employee_status_choice(employee, "Deactivate")

    # ---------------------------------------------------------
    # LOAD / SEARCH
    # ---------------------------------------------------------

    def load_employees(self):
        try:
            employees = get_all_employees()
            self.selected_employee_id = None
            self.update_toolbar_button.configure(state="disabled")
            self.display_employees(employees)
        except Exception as error:
            messagebox.showerror(
                "Employee Records",
                f"Unable to load employee records:\n{error}",
            )

    def search_employee_records(self):
        search_text = self.search_entry.get().strip()

        if not search_text:
            self.load_employees()
            return

        try:
            employees = search_employees(search_text)
            self.selected_employee_id = None
            self.update_toolbar_button.configure(state="disabled")
            self.display_employees(employees)
        except Exception as error:
            messagebox.showerror(
                "Employee Search",
                f"Unable to search employees:\n{error}",
            )

    # ---------------------------------------------------------
    # SELECT EMPLOYEE
    # ---------------------------------------------------------

    def select_employee(self, employee):
        self.selected_employee_id = employee["id"]

        self.set_entry_value(
            "employee_code",
            employee["employee_code"],
        )
        self.set_entry_value(
            "full_name",
            employee["full_name"],
        )
        self.set_entry_value(
            "email",
            employee["email"],
        )
        self.set_entry_value(
            "phone",
            employee["phone"],
        )
        self.set_entry_value(
            "department",
            employee["department"],
        )
        self.set_entry_value(
            "designation",
            employee["designation"],
        )
        self.set_entry_value(
            "salary",
            employee["salary"],
        )
        self.set_entry_value(
            "joining_date",
            employee["joining_date"],
        )

        self.update_button.configure(state="normal")
        self.update_toolbar_button.configure(state="normal")
        # Selecting a record should dismiss the Add/Update form. The selected
        # employee's values remain in the entries so Update Selected can reopen it.
        self.form_panel.grid_remove()
        self.grid_columnconfigure(0, weight=0, minsize=0)

    def set_entry_value(self, key, value):
        entry = self.entries[key]
        entry.delete(0, "end")
        entry.insert(0, str(value))

    # ---------------------------------------------------------
    # UPDATE EMPLOYEE
    # ---------------------------------------------------------

    def update_selected_employee(self):
        if self.selected_employee_id is None:
            messagebox.showwarning(
                "No Employee Selected",
                "Please select an employee before updating.",
            )
            return

        employee_code = self.entries["employee_code"].get()
        full_name = self.entries["full_name"].get()
        email = self.entries["email"].get()
        phone = self.entries["phone"].get()
        department = self.entries["department"].get()
        designation = self.entries["designation"].get()
        salary = self.entries["salary"].get()
        joining_date = self.entries["joining_date"].get()

        try:
            updated = update_employee(
                employee_id=self.selected_employee_id,
                employee_code=employee_code,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                designation=designation,
                salary=salary,
                joining_date=joining_date,
                performed_by=self.user,
            )

            if not updated:
                messagebox.showwarning(
                    "Update Employee",
                    "Employee could not be updated.",
                )
                return

            messagebox.showinfo(
                "Success",
                "Employee updated successfully.",
            )

            self.clear_form()
            self.load_employees()

        except ValueError as error:
            messagebox.showwarning(
                "Validation Error",
                str(error),
            )

        except Exception as error:
            messagebox.showerror(
                "Employee Update",
                f"Unable to update employee:\n{error}",
            )

    # ---------------------------------------------------------
    # DEACTIVATE EMPLOYEE
    # ---------------------------------------------------------

    def deactivate_selected_employee(self):
        if self.selected_employee_id is None:
            messagebox.showwarning(
                "No Employee Selected",
                "Please select an employee before deactivating.",
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Deactivation",
            "Are you sure you want to deactivate this employee?",
        )

        if not confirmation:
            # The OptionMenu changes its label before this confirmation appears.
            # Re-render persisted values so Cancel restores the saved status.
            self.load_employees()
            return

        try:
            deactivated = deactivate_employee(
                self.selected_employee_id,
                performed_by=self.user,
            )

            if not deactivated:
                messagebox.showwarning(
                    "Deactivate Employee",
                    "Employee could not be deactivated.",
                )
                self.load_employees()
                return

            messagebox.showinfo(
                "Success",
                "Employee deactivated successfully.",
            )

            self.clear_form()
            self.load_employees()

        except Exception as error:
            messagebox.showerror(
                "Deactivate Employee",
                f"Unable to deactivate employee:\n{error}",
            )
            self.load_employees()

    # ---------------------------------------------------------
    # ADD EMPLOYEE
    # ---------------------------------------------------------

    def add_employee(self):
        employee_code = self.entries["employee_code"].get()
        full_name = self.entries["full_name"].get()
        email = self.entries["email"].get()
        phone = self.entries["phone"].get()
        department = self.entries["department"].get()
        designation = self.entries["designation"].get()
        salary = self.entries["salary"].get()
        joining_date = self.entries["joining_date"].get()

        try:
            create_employee(
                employee_code=employee_code,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                designation=designation,
                salary=salary,
                joining_date=joining_date,
                performed_by=self.user,
            )

            messagebox.showinfo(
                "Success",
                "Employee added successfully.",
            )

            self.clear_form()
            self.load_employees()

        except ValueError as error:
            messagebox.showwarning(
                "Validation Error",
                str(error),
            )

        except Exception as error:
            messagebox.showerror(
                "Employee Creation",
                f"Unable to add employee:\n{error}",
            )

    # ---------------------------------------------------------
    # CLEAR FORM
    # ---------------------------------------------------------

    def clear_form(self, hide_panel=True):
        self.selected_employee_id = None
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.update_button.configure(state="disabled")
        self.update_toolbar_button.configure(state="disabled")
        self.form_title.configure(text="Add Employee")
        self.add_button.configure(state="normal")
        if hide_panel and hasattr(self, "form_panel"):
            self.form_panel.grid_remove()
            self.grid_columnconfigure(0, weight=0, minsize=0)
