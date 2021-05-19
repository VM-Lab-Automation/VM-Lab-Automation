import pytest
from mock import MagicMock

from logic.auth_service import AuthService, NotAuthenticated
from models.user import User


def test_login_should_raise_exception():
    user_repository = MagicMock()
    tokens_helper = MagicMock()

    user = User("id", "user1", "$2y$12$XSjsdOLKBCIKHQ78j8D5L.DGCI0j5BXFYsZRgidZFDUxyi.r/Bn4", "email")
    user_repository.get_by_username.return_value = user

    auth_service = AuthService(user_repository, tokens_helper)
    with pytest.raises(NotAuthenticated):
        auth_service.login("user1", "password")
