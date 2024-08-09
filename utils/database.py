import sqlite3
import logging
from config import local_config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_file=local_config.DATABASE_NAME):
        self.connection = None
        self.cursor = None
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        try:
            logger.debug("Attempting to initialize database connection.")
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            logger.info("Database connection and cursor initialized successfully.")
            self.create_tables()  # Create tables if they don't exist
        except sqlite3.Error as err:
            logger.error(f"Error initializing database: {err}")
            self.connection = None
            self.cursor = None

    def create_tables(self):
        try:
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {local_config.USER_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """)
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {local_config.WEATHER_DATA_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                wind_speed REAL NOT NULL,
                timestamp INTEGER NOT NULL
            )
            """)
            self.connection.commit()
        except sqlite3.Error as err:
            logger.error(f"Error creating tables: {err}")

    def get_cursor(self):
        if self.connection and self.cursor:
            return self.cursor
        else:
            logger.error("No cursor or connection available.")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
            logger.info("Cursor closed.")
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")
