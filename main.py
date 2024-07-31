# import mysql.connector
#
# myDb = mysql.connector.connect(
#     user="root",
#     password="Rahulraj@88",
#     host='127.0.0.1',
#     database='Test',
#     auth_plugin='mysql_native_password'
# )
#
# print(myDb)

import tkinter as tk
from views.login_view import LoginView
from views.main_view import MainView

API_KEY = '969353204ed3454e013d97eccc693b9d'  # Replace with your actual API key


def load_main_view(root):
    root.destroy()
    root = tk.Tk()
    app = MainView(root, API_KEY)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()
