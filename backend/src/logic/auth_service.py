from logic.db.users_repository import UsersRepository
from logic.helpers.tokens_helper import TokensHelper
import bcrypt

from models.user import User


class NotAuthenticated(Exception):
    pass


class AuthService:

    def __init__(self, users_repository: UsersRepository, tokens_helper):
        self.users_repository = users_repository
        self.tokens_helper = tokens_helper

    def login(self, username, password) -> str:
        user = self.users_repository.get_by_username(username)
        if not bcrypt.checkpw(bytes(password, encoding='utf-8'), bytes(user.password_hash, encoding='utf-8')):
            raise NotAuthenticated("Incorrect password.")

        return self.tokens_helper.encode_auth_token(user.id)

    def get_user(self, user_id) -> User:
        return self.users_repository.get(user_id)

