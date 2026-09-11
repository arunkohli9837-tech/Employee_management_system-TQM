import customtkinter as ctk


class EmployeeManagementFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back):
        super().__init__(master)

        self.user = user
        self.on_back = on_back

        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_form()
        self.create_list_area()

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
            state="disabled",
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
        self.list_area = ctk.CTkFrame(self)
        self.list_area.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10,
        )

        label = ctk.CTkLabel(
            self.list_area,
            text="Employee Records",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        label.pack(
            padx=20,
            pady=(20, 10),
        )

        self.empty_label = ctk.CTkLabel(
            self.list_area,
            text="Employee records will appear here.",
        )
        self.empty_label.pack(
            padx=20,
            pady=20,
        )

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