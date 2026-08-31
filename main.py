import customtkinter as ctk


class EmployeeManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Employee Management System")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.main_label = ctk.CTkLabel(
            self,
            text="Employee Management System",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        self.main_label.pack(expand=True)


def main():
    app = EmployeeManagementApp()
    app.mainloop()


if __name__ == "__main__":
    main()