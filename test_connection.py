import mysql.connector
import logging
from utils.database import Database

logging.basicConfig(level=logging.DEBUG)


def test_connection():
    try:
        connection = mysql.connector.connect(
            user="root",
            password="Rahulraj@88",
            host='127.0.0.1',
            database='weatherdashboard',
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            logging.info(f"Connected to database: {db}")
            cursor.close()
        else:
            logging.error("Failed to connect to database.")
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
    finally:
        if connection:
            connection.close()


logging.basicConfig(level=logging.DEBUG)


def test_db():
    db = Database()
    cursor = db.get_cursor()
    if cursor:
        try:
            cursor.execute("SELECT DATABASE()")
            result = cursor.fetchone()
            print("Connected to database:", result)
        except Exception as e:
            print(f"Failed to execute query: {e}")
    else:
        print("Failed to get cursor.")
    db.close()


if __name__ == "__main__":
    test_db()
