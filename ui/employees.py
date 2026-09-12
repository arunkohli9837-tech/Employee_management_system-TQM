import customtkinter as ctk

from services.employee_service import get_all_employees, search_employees


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

        form.grid_columnconfigure(0, weight=1)

        search_label = ctk.CTkLabel(
            form,
            text="Search Employees",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        search_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5),
            sticky="w",
        )

        search_area = ctk.CTkFrame(form)
        search_area.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 10),
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

        self.add_button = ctk.CTkButton(
            form,
            text="Add Employee",
            state="disabled",
        )
        self.add_button.grid(
            row=2,
            column=0,
            padx=10,
            pady=(5, 10),
            sticky="w",
        )

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

        self.records_container = ctk.CTkFrame(
            self.list_area,
            fg_color="transparent",
        )
        self.records_container.grid(
            row=1,
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

            employee_frame.grid_columnconfigure(1, weight=1)

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
                    f"Email: {employee['email']}    "
                    f"Phone: {employee['phone']}    "
                    f"Department: {employee['department']}    "
                    f"Designation: {employee['designation']}    "
                    f"Salary: {employee['salary']}    "
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