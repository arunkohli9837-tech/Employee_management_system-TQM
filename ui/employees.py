import customtkinter as ctk
from tkinter import messagebox

from services.employee_service import (
    get_all_employees,
    search_employees,
    create_employee,
    update_employee,
)


class EmployeeManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back
        self.selected_employee_id = None

        self.entries = {}

        self.grid_columnconfigure(0, weight=0, minsize=390)
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

        self.back_button = ctk.CTkButton(
            self.header,
            text="Back to Dashboard",
            width=150,
            command=self.on_back,
        )
        self.back_button.grid(
            row=0,
            column=1,
            padx=(10, 0),
        )

    # ---------------------------------------------------------
    # LEFT FORM
    # ---------------------------------------------------------

    def create_form_panel(self):
        self.form_panel = ctk.CTkFrame(self)
        self.form_panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(30, 12),
            pady=(0, 30),
        )

        self.form_panel.grid_columnconfigure(0, weight=1)
        self.form_panel.grid_rowconfigure(1, weight=1)

        self.form_title = ctk.CTkLabel(
            self.form_panel,
            text="Employee Details",
            font=ctk.CTkFont(size=21, weight="bold"),
        )
        self.form_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(25, 15),
        )

        self.form_scroll = ctk.CTkScrollableFrame(
            self.form_panel,
            fg_color="transparent",
        )
        self.form_scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10),
        )

        self.form_scroll.grid_columnconfigure(0, weight=1)

        self.create_form_fields()

        self.action_frame = ctk.CTkFrame(
            self.form_panel,
            fg_color="transparent",
        )
        self.action_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(5, 25),
        )

        self.action_frame.grid_columnconfigure(0, weight=1)

        self.add_button = ctk.CTkButton(
            self.action_frame,
            text="Add Employee",
            height=38,
            command=self.add_employee,
        )
        self.add_button.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 8),
        )

        self.update_button = ctk.CTkButton(
            self.action_frame,
            text="Update Employee",
            height=38,
            state="disabled",
            command=self.update_selected_employee,
        )
        self.update_button.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=4,
        )

        self.deactivate_button = ctk.CTkButton(
            self.action_frame,
            text="Deactivate Employee",
            height=38,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            state="disabled",
        )
        self.deactivate_button.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=4,
        )

        self.clear_button = ctk.CTkButton(
            self.action_frame,
            text="Clear Form",
            height=38,
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.clear_form,
        )
        self.clear_button.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(8, 0),
        )

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

        for row, (key, placeholder) in enumerate(fields):
            entry = ctk.CTkEntry(
                self.form_scroll,
                placeholder_text=placeholder,
                height=38,
            )
            entry.grid(
                row=row,
                column=0,
                sticky="ew",
                padx=15,
                pady=7,
            )

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
            padx=(12, 30),
            pady=(0, 30),
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

        self.records_scroll.grid_columnconfigure(0, weight=1)

    # ---------------------------------------------------------
    # EMPLOYEE RECORD DISPLAY
    # ---------------------------------------------------------

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

        columns = [
            ("Code", 0),
            ("Name", 1),
            ("Email", 2),
            ("Department", 3),
            ("Designation", 4),
            ("Salary", 5),
            ("Status", 6),
        ]

        for text, column in columns:
            header.grid_columnconfigure(column, weight=1)

            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
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

        for column in range(7):
            row_frame.grid_columnconfigure(column, weight=1)

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
                padx=6,
                pady=8,
            )

            label.bind(
                "<Button-1>",
                lambda event, emp=employee: self.select_employee(emp),
            )

        row_frame.bind(
            "<Button-1>",
            lambda event, emp=employee: self.select_employee(emp),
        )

    # ---------------------------------------------------------
    # LOAD / SEARCH
    # ---------------------------------------------------------

    def load_employees(self):
        try:
            employees = get_all_employees()
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

    def set_entry_value(self, key, value):
        entry = self.entries[key]
        entry.delete(0, "end")
        entry.insert(0, str(value))

    #---------------------------------------------------------
    #UPDATE EMPLOYEE
    #---------------------------------------------------------
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

    def clear_form(self):
        self.selected_employee_id = None

        for entry in self.entries.values():
            entry.delete(0, "end")

        self.update_button.configure(
            state="disabled"
        )

        self.form_title.configure(
            text="Employee Details"
        )