import pytest

from app.core import Settings
from app.exceptions import TokenInvalidError
from app.services.auth_service import AuthService

from tests.fakes import FakeUserService


def test_validate_token_payload_ok():
    user_id = AuthService._validate_token_payload(
        {"sub": "1", "type": "access", "jti": "abc"},
        "access",
        "invalid",
    )
    assert user_id == 1


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"sub": "1"},
        {"sub": "1", "type": "access"},
        {"sub": "1", "jti": "abc"},
        {"sub": "", "type": "access", "jti": "abc"},
        {"sub": "x", "type": "access", "jti": "abc"},
        {"sub": "1", "type": "refresh", "jti": "abc"},
        {"sub": "1", "type": "access", "jti": ""},
        {"sub": 1, "type": "access", "jti": "abc"},
    ],
)
def test_validate_token_payload_invalid(payload):
    with pytest.raises(TokenInvalidError):
        AuthService._validate_token_payload(payload, "access", "invalid")


def test_get_user_id_from_token(test_settings: Settings):
    service = AuthService(FakeUserService(), test_settings)
    token, _ = service.jwt_manager.create_token(
        {"sub": "777", "type": service.ACCESS_TOKEN_TYPE},
        test_settings.access_secret,
        5,
    )
    assert service.get_user_id_from_token(token) == 777
