import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
import logging

logger = logging.getLogger(__name__)


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Center the window
        self.center_window()

        self.user_controller = UserController()

        # Create a frame to hold the login form
        self.frame = tk.Frame(root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.username_label = tk.Label(self.frame, text="Username")
        self.username_label.grid(row=0, column=0, pady=10)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)

        self.password_label = tk.Label(self.frame, text="Password")
        self.password_label.grid(row=1, column=0, pady=10)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=20)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=2, column=1, pady=20)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        logger.debug(f"Attempting to login with username: {username}")
        user = self.user_controller.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login", "Invalid credentials")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        logger.debug(f"Attempting to sign up with username: {username}")
        self.user_controller.create_user(username, password)
        messagebox.showinfo("Sign Up", "User created successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()
