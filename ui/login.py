import customtkinter as ctk

from services.auth_service import authenticate_user


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)

        self.on_login_success = on_login_success

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Employee Management System",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.title_label.grid(
            row=0,
            column=0,
            padx=30,
            pady=(40, 10),
        )

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Login to continue",
            font=ctk.CTkFont(size=16),
        )
        self.subtitle_label.grid(
            row=1,
            column=0,
            padx=30,
            pady=(0, 25),
        )

        self.username_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Username",
        )
        self.username_entry.grid(
            row=2,
            column=0,
            padx=30,
            pady=10,
        )

        self.password_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Password",
            show="*",
        )
        self.password_entry.grid(
            row=3,
            column=0,
            padx=30,
            pady=10,
        )

        self.message_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red",
        )
        self.message_label.grid(
            row=4,
            column=0,
            padx=30,
            pady=(5, 5),
        )

        self.login_button = ctk.CTkButton(
            self,
            width=300,
            text="Login",
            command=self.handle_login,
        )
        self.login_button.grid(
            row=5,
            column=0,
            padx=30,
            pady=(10, 30),
        )

        self.password_entry.bind("<Return>", lambda event: self.handle_login())
        self.username_entry.focus_set()

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        self.message_label.configure(text="")

        if not username or not password:
            self.message_label.configure(
                text="Username and password are required."
            )
            return

        user = authenticate_user(username, password)

        if user is None:
            self.message_label.configure(
                text="Invalid username or password."
            )
            return

        self.on_login_success(user)