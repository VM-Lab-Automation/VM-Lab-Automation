from logic.db.db_connection import DbConnection
from models.user import User


class UserNotFoundException(Exception):
    pass


class UsersRepository:

    def __init__(self, config: dict):
        self.config = config

    def get(self, id: int) -> User:
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM users WHERE id='%s' LIMIT 1" % id)
            user_row = rows.fetchone()
            if user_row is None:
                raise UserNotFoundException()
            return User(*user_row)

    def get_by_username(self, username: str) -> User:
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM users WHERE username='%s' LIMIT 1" % username)
            user_row = rows.fetchone()
            if user_row is None:
                raise UserNotFoundException()
            return User(*user_row)

