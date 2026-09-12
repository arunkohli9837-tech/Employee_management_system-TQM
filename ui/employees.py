import customtkinter as ctk
from tkinter import messagebox

from services.employee_service import (
    get_all_employees,
    search_employees,
    create_employee,
)


class EmployeeManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_form()
        self.create_list_area()

        self.load_employees()

    def create_header(self):
        header = ctk.CTkFrame(self)
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=20,
        )

        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Employee Management",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w",
        )

        back_button = ctk.CTkButton(
            header,
            text="Back to Dashboard",
            command=self.on_back,
        )
        back_button.grid(
            row=0,
            column=1,
            padx=15,
            pady=10,
        )

    def create_form(self):
        form = ctk.CTkFrame(self)
        form.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=10,
        )

        for column in range(4):
            form.grid_columnconfigure(column, weight=1)

        self.employee_code_entry = self.create_field(
            form, "Employee Code", 0, 0
        )

        self.name_entry = self.create_field(
            form, "Full Name", 0, 1
        )

        self.email_entry = self.create_field(
            form, "Email", 0, 2
        )

        self.phone_entry = self.create_field(
            form, "Phone", 0, 3
        )

        self.department_entry = self.create_field(
            form, "Department", 2, 0
        )

        self.designation_entry = self.create_field(
            form, "Designation", 2, 1
        )

        self.salary_entry = self.create_field(
            form, "Salary", 2, 2
        )

        self.joining_date_entry = self.create_field(
            form, "Joining Date", 2, 3
        )

        self.add_button = ctk.CTkButton(
            form,
            text="Add Employee",
            command=self.add_employee,
        )
        self.add_button.grid(
            row=4,
            column=0,
            padx=10,
            pady=15,
        )

        self.update_button = ctk.CTkButton(
            form,
            text="Update Employee",
            state="disabled",
        )
        self.update_button.grid(
            row=4,
            column=1,
            padx=10,
            pady=15,
        )

        self.deactivate_button = ctk.CTkButton(
            form,
            text="Deactivate",
            state="disabled",
        )
        self.deactivate_button.grid(
            row=4,
            column=2,
            padx=10,
            pady=15,
        )

        self.clear_button = ctk.CTkButton(
            form,
            text="Clear",
            command=self.clear_form,
        )
        self.clear_button.grid(
            row=4,
            column=3,
            padx=10,
            pady=15,
        )

        self.status_label = ctk.CTkLabel(
            form,
            text="",
        )
        self.status_label.grid(
            row=5,
            column=0,
            columnspan=4,
            padx=10,
            pady=(0, 10),
        )

    def create_field(self, parent, label_text, row, column):
        label = ctk.CTkLabel(
            parent,
            text=label_text,
        )
        label.grid(
            row=row,
            column=column,
            padx=10,
            pady=(10, 2),
            sticky="w",
        )

        entry = ctk.CTkEntry(parent)
        entry.grid(
            row=row + 1,
            column=column,
            padx=10,
            pady=(2, 10),
            sticky="ew",
        )

        return entry

    def create_list_area(self):
        self.list_area = ctk.CTkScrollableFrame(self)
        self.list_area.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10,
        )

        self.list_area.grid_columnconfigure(0, weight=1)

        self.records_title = ctk.CTkLabel(
            self.list_area,
            text="Employee Records",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.records_title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(10, 15),
            sticky="w",
        )

        search_area = ctk.CTkFrame(self.list_area)
        search_area.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=5,
        )

        search_area.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_area,
            placeholder_text="Search by employee code, name or email",
        )
        self.search_entry.grid(
            row=0,
            column=0,
            padx=(0, 10),
            pady=5,
            sticky="ew",
        )

        self.search_button = ctk.CTkButton(
            search_area,
            text="Search",
            width=100,
            command=self.search_employee_records,
        )
        self.search_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        self.clear_search_button = ctk.CTkButton(
            search_area,
            text="Clear",
            width=100,
            command=self.clear_search,
        )
        self.clear_search_button.grid(
            row=0,
            column=2,
            padx=(5, 0),
            pady=5,
        )

        self.records_container = ctk.CTkFrame(
            self.list_area,
            fg_color="transparent",
        )
        self.records_container.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=5,
        )

        self.records_container.grid_columnconfigure(0, weight=1)

    def clear_records(self):
        for widget in self.records_container.winfo_children():
            widget.destroy()

    def display_employees(self, employees):
        self.clear_records()

        if not employees:
            empty_label = ctk.CTkLabel(
                self.records_container,
                text="No employee records found.",
                font=ctk.CTkFont(size=15),
            )
            empty_label.grid(
                row=0,
                column=0,
                padx=20,
                pady=20,
            )
            return

        for index, employee in enumerate(employees):
            employee_frame = ctk.CTkFrame(
                self.records_container
            )
            employee_frame.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=5,
                pady=5,
            )

            employee_frame.grid_columnconfigure(0, weight=1)

            title = ctk.CTkLabel(
                employee_frame,
                text=(
                    f"{employee['employee_code']} - "
                    f"{employee['full_name']}"
                ),
                font=ctk.CTkFont(size=16, weight="bold"),
            )
            title.grid(
                row=0,
                column=0,
                padx=15,
                pady=(10, 5),
                sticky="w",
            )

            details = ctk.CTkLabel(
                employee_frame,
                text=(
                    f"Email: {employee['email']}\n"
                    f"Phone: {employee['phone']}\n"
                    f"Department: {employee['department']}\n"
                    f"Designation: {employee['designation']}\n"
                    f"Salary: {employee['salary']}\n"
                    f"Joining Date: {employee['joining_date']}\n"
                    f"Status: {employee['status']}"
                ),
                anchor="w",
                justify="left",
            )
            details.grid(
                row=1,
                column=0,
                padx=15,
                pady=(5, 10),
                sticky="w",
            )

    def load_employees(self):
        employees = get_all_employees()
        self.display_employees(employees)

    def search_employee_records(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.load_employees()
            return

        employees = search_employees(search_term)
        self.display_employees(employees)

    def clear_search(self):
        self.search_entry.delete(0, "end")
        self.load_employees()

    def add_employee(self):
        employee_code = self.employee_code_entry.get()
        full_name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        department = self.department_entry.get()
        designation = self.designation_entry.get()
        salary = self.salary_entry.get()
        joining_date = self.joining_date_entry.get()

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

        except ValueError as error:
            self.status_label.configure(
                text=str(error)
            )
            return

        except Exception as error:
            self.status_label.configure(
                text=f"Unable to add employee: {error}"
            )
            return

        self.status_label.configure(
            text="Employee added successfully."
        )

        self.clear_form()
        self.load_employees()

    def clear_form(self):
        entries = [
            self.employee_code_entry,
            self.name_entry,
            self.email_entry,
            self.phone_entry,
            self.department_entry,
            self.designation_entry,
            self.salary_entry,
            self.joining_date_entry,
        ]

        for entry in entries:
            entry.delete(0, "end")