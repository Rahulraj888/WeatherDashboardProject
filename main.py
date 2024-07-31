import mysql.connector

myDb = mysql.connector.connect(
    user="root",
    password="Rahulraj@88",
    host='127.0.0.1',
    database='Test',
    auth_plugin='mysql_native_password'
)

print(myDb)
