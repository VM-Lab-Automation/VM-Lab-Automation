from logic.db.db_connection import DbConnection
from models.user import User
from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime


meta = MetaData()
users = Table(
   'users', meta,
   Column('id', Integer, primary_key=True),
   Column('username', String),
   Column('password_hash', String),
   Column('email', String)
)


class UserNotFoundException(Exception):
    pass


class UsersRepository:

    def __init__(self, config: dict):
        self.config = config

    def get(self, id: int) -> User:
        with DbConnection(self.config) as con:
            result = con.execute(users.select().where(users.c.id == id))
            user_row = result.fetchone()
            if user_row is None:
                raise UserNotFoundException()
            return User(*user_row)

    def get_by_username(self, username: str) -> User:
        with DbConnection(self.config) as con:
            result = con.execute(users.select().where(users.c.username == username).limit(1))
            user_row = result.fetchone()
            if user_row is None:
                raise UserNotFoundException()
            return User(*user_row)

