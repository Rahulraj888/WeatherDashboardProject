import mysql.connector
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.init_db()

    def init_db(self):
        try:
            logger.debug("Attempting to initialize database connection.")
            self.connection = mysql.connector.connect(
                user="root",
                password="Rahulraj@88",
                host='127.0.0.1',
                database='weatherdashboard',
                auth_plugin='mysql_native_password'
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                logger.info("Database connection and cursor initialized successfully.")
            else:
                logger.error("Database connection is not active.")
                self.connection = None
                self.cursor = None
        except mysql.connector.Error as err:
            logger.error(f"Error initializing database: {err}")
            self.connection = None
            self.cursor = None

    def get_cursor(self):
        if self.connection and self.cursor:
            if self.connection.is_connected():
                logger.debug(f"Cursor state: {self.cursor is not None}")
                return self.cursor
            else:
                logger.error("Database connection is not active.")
                return None
        else:
            logger.error("No cursor or connection available.")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
            logger.info("Cursor closed.")
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed.")
