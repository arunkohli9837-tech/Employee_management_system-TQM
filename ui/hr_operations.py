"""Payroll and performance-log screen for the Employee Management System."""
import customtkinter as ctk
from tkinter import messagebox

from services.hr_operations_service import (
    create_payroll_record,
    create_performance_log,
    get_payroll_records,
    get_performance_logs,
    list_active_employees,
)


class HROperationsFrame(ctk.CTkFrame):
    def __init__(self, master, user, on_back=None):
        super().__init__(master)
        self.user = user
        self.on_back = on_back
        self.employees = []
        self.employee_lookup = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(self, text="Payroll & Performance Logs", font=ctk.CTkFont(size=26, weight="bold")).grid(
            row=0, column=0, padx=24, pady=(22, 8), sticky="w"
        )
        ctk.CTkLabel(
            self,
            text="Basic monthly payroll record and employee performance review tracking.",
            text_color=("gray35", "gray70"),
        ).grid(row=1, column=0, padx=24, pady=(0, 12), sticky="w")
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=2, column=0, padx=24, pady=(0, 22), sticky="nsew")
        self.tabs.add("Payroll")
        self.tabs.add("Performance")
        self._build_payroll_tab()
        self._build_performance_tab()
        self.refresh_employees()
        self.refresh_records()

    def _employee_menu(self, parent, row):
        self.employee_menu = ctk.CTkOptionMenu(parent, values=["No active employees"])
        self.employee_menu.grid(row=row, column=1, padx=8, pady=6, sticky="ew")

    def _build_payroll_tab(self):
        tab = self.tabs.tab("Payroll")
        tab.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(tab, text="Employee").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.pay_employee = ctk.CTkOptionMenu(tab, values=["No active employees"])
        self.pay_employee.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkLabel(tab, text="Pay period (YYYY-MM)").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.pay_period = ctk.CTkEntry(tab, placeholder_text="2026-10")
        self.pay_period.grid(row=1, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkLabel(tab, text="Deductions").grid(row=2, column=0, padx=8, pady=6, sticky="w")
        self.pay_deductions = ctk.CTkEntry(tab, placeholder_text="0")
        self.pay_deductions.insert(0, "0")
        self.pay_deductions.grid(row=2, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkLabel(tab, text="Bonus").grid(row=3, column=0, padx=8, pady=6, sticky="w")
        self.pay_bonus = ctk.CTkEntry(tab, placeholder_text="0")
        self.pay_bonus.insert(0, "0")
        self.pay_bonus.grid(row=3, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkButton(tab, text="Create Payroll Record", command=self.save_payroll).grid(
            row=4, column=0, columnspan=2, padx=8, pady=10, sticky="ew"
        )
        ctk.CTkLabel(tab, text="Payroll Records", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=5, column=0, columnspan=2, padx=8, pady=(8, 2), sticky="w"
        )
        self.payroll_list = ctk.CTkScrollableFrame(tab, height=190)
        self.payroll_list.grid(row=6, column=0, columnspan=2, padx=8, pady=(2, 8), sticky="nsew")
        tab.grid_rowconfigure(6, weight=1)

    def _build_performance_tab(self):
        tab = self.tabs.tab("Performance")
        tab.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(tab, text="Employee").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.performance_employee = ctk.CTkOptionMenu(tab, values=["No active employees"])
        self.performance_employee.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkLabel(tab, text="Review date (DD-MM-YYYY)").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.review_date = ctk.CTkEntry(tab, placeholder_text="25-10-2026")
        self.review_date.grid(row=1, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkLabel(tab, text="Rating (1–5)").grid(row=2, column=0, padx=8, pady=6, sticky="w")
        self.performance_rating = ctk.CTkOptionMenu(tab, values=["1", "2", "3", "4", "5"])
        self.performance_rating.set("3")
        self.performance_rating.grid(row=2, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkLabel(tab, text="Review comments").grid(row=3, column=0, padx=8, pady=6, sticky="nw")
        self.performance_comments = ctk.CTkTextbox(tab, height=75)
        self.performance_comments.grid(row=3, column=1, padx=8, pady=6, sticky="ew")
        ctk.CTkButton(tab, text="Save Performance Log", command=self.save_performance).grid(
            row=4, column=0, columnspan=2, padx=8, pady=10, sticky="ew"
        )
        ctk.CTkLabel(tab, text="Performance Records", font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=5, column=0, columnspan=2, padx=8, pady=(8, 2), sticky="w"
        )
        self.performance_list = ctk.CTkScrollableFrame(tab, height=180)
        self.performance_list.grid(row=6, column=0, columnspan=2, padx=8, pady=(2, 8), sticky="nsew")
        tab.grid_rowconfigure(6, weight=1)

    def refresh_employees(self):
        try:
            self.employees = list_active_employees(self.user)
            self.employee_lookup = {
                f"{row[1]} — {row[2]}": row[0] for row in self.employees
            }
            values = list(self.employee_lookup) or ["No active employees"]
            self.pay_employee.configure(values=values)
            self.performance_employee.configure(values=values)
            self.pay_employee.set(values[0])
            self.performance_employee.set(values[0])
        except Exception as error:
            messagebox.showerror("Unable to load employees", str(error), parent=self)

    def _selected_employee_id(self, menu):
        selected = menu.get()
        if selected not in self.employee_lookup:
            raise ValueError("Please add/select an active employee first.")
        return self.employee_lookup[selected]

    def save_payroll(self):
        try:
            create_payroll_record(
                self._selected_employee_id(self.pay_employee),
                self.pay_period.get(), self.pay_deductions.get(), self.pay_bonus.get(), self.user,
            )
            messagebox.showinfo("Saved", "Payroll record saved successfully.", parent=self)
            self.refresh_records()
        except Exception as error:
            messagebox.showerror("Payroll not saved", str(error), parent=self)

    def save_performance(self):
        try:
            create_performance_log(
                self._selected_employee_id(self.performance_employee),
                self.review_date.get(), self.performance_rating.get(),
                self.performance_comments.get("1.0", "end").strip(), self.user,
            )
            messagebox.showinfo("Saved", "Performance log saved successfully.", parent=self)
            self.performance_comments.delete("1.0", "end")
            self.refresh_records()
        except Exception as error:
            messagebox.showerror("Performance log not saved", str(error), parent=self)

    def refresh_records(self):
        """Refresh payroll and performance records using aligned table rows."""
        try:
            payroll_rows = get_payroll_records(self.user)
            for widget in self.payroll_list.winfo_children():
                widget.destroy()
            payroll_columns = ["Code", "Employee", "Period", "Basic", "Deductions", "Bonus", "Net Salary"]
            for col, title in enumerate(payroll_columns):
                self.payroll_list.grid_columnconfigure(col, weight=1, minsize=72)
                ctk.CTkLabel(
                    self.payroll_list, text=title, anchor="w",
                    font=ctk.CTkFont(size=11, weight="bold"),
                ).grid(row=0, column=col, sticky="ew", padx=5, pady=(5, 8))
            if payroll_rows:
                for row_index, row in enumerate(payroll_rows, start=1):
                    values = [row[1], row[2], row[3], f"{row[4]:.2f}", f"{row[5]:.2f}", f"{row[6]:.2f}", f"{row[7]:.2f}"]
                    for col, value in enumerate(values):
                        ctk.CTkLabel(
                            self.payroll_list, text=str(value), anchor="w",
                            font=ctk.CTkFont(size=11),
                        ).grid(row=row_index, column=col, sticky="ew", padx=5, pady=5)
            else:
                ctk.CTkLabel(self.payroll_list, text="No payroll records yet.", anchor="w").grid(
                    row=1, column=0, columnspan=len(payroll_columns), sticky="ew", padx=5, pady=12
                )

            performance_rows = get_performance_logs(self.user)
            for widget in self.performance_list.winfo_children():
                widget.destroy()
            performance_columns = ["Code", "Employee", "Review Date", "Rating", "Comments"]
            for col, title in enumerate(performance_columns):
                self.performance_list.grid_columnconfigure(col, weight=1, minsize=80)
                ctk.CTkLabel(
                    self.performance_list, text=title, anchor="w",
                    font=ctk.CTkFont(size=11, weight="bold"),
                ).grid(row=0, column=col, sticky="ew", padx=5, pady=(5, 8))
            if performance_rows:
                for row_index, row in enumerate(performance_rows, start=1):
                    values = [row[1], row[2], row[3], f"{row[4]}/5", row[5]]
                    for col, value in enumerate(values):
                        ctk.CTkLabel(
                            self.performance_list, text=str(value), anchor="w",
                            justify="left", wraplength=260 if col == 4 else 150,
                            font=ctk.CTkFont(size=11),
                        ).grid(row=row_index, column=col, sticky="ew", padx=5, pady=5)
            else:
                ctk.CTkLabel(self.performance_list, text="No performance logs yet.", anchor="w").grid(
                    row=1, column=0, columnspan=len(performance_columns), sticky="ew", padx=5, pady=12
                )
        except Exception as error:
            messagebox.showerror("Unable to refresh records", str(error), parent=self)
