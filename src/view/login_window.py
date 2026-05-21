import customtkinter as ctk
from tkinter import messagebox
from src.controller.app_controller import AppController

class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()

        self.title("AI Personal Finance - Login")
        self.geometry("400x500")
        self.on_login_success = on_login_success
        self.controller = AppController()

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Finance AI", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, pady=(40, 20))

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.entry_username.grid(row=1, column=0, pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", width=250, show="*")
        self.entry_password.grid(row=2, column=0, pady=10)

        btn_login = ctk.CTkButton(self, text="Login", width=250, command=self.handle_login)
        btn_login.grid(row=3, column=0, pady=(20, 10))

        btn_register = ctk.CTkButton(self, text="Register", width=250, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.handle_register)
        btn_register.grid(row=4, column=0, pady=10)

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please fill out all fields.")
            return

        try:
            user_id = self.controller.login(username, password)
            if user_id:
                self.destroy()
                self.on_login_success(user_id)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please fill out all fields.")
            return

        try:
            user_id = self.controller.register(username, password)
            messagebox.showinfo("Success", "Registration successful. You are now logged in.")
            self.destroy()
            self.on_login_success(user_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
