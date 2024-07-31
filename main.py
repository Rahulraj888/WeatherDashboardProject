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
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()



