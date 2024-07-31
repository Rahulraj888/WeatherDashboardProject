import logging
from utils.database import Database

logger = logging.getLogger(__name__)


class UserController:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()

    def authenticate_user(self, username, password):
        if self.cursor:
            try:
                logger.debug("Attempting to authenticate user.")
                self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                user = self.cursor.fetchone()
                logger.info("User authentication successful." if user else "User authentication failed.")
                return user
            except Exception as e:
                logger.error(f"Error during authentication: {e}")
        return None

    def create_user(self, username, password):
        if self.cursor:
            try:
                logger.debug("Attempting to create user.")
                self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                self.db.connection.commit()
                logger.info("User created successfully.")
            except Exception as e:
                logger.error(f"Error during user creation: {e}")
                self.db.connection.rollback()
        else:
            logger.error("No cursor available for user creation.")
