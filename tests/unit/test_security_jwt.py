import pytest

from app.core.security import JWTManager
from app.exceptions import TokenExpiredError, TokenInvalidError


def test_create_and_decode_token_roundtrip():
    secret = "a" * 32
    token, jti = JWTManager.create_token(
        {"sub": "1", "type": "access"},
        secret,
        10,
    )

    payload = JWTManager.decode_token(token, secret)

    assert payload["sub"] == "1"
    assert payload["type"] == "access"
    assert payload["jti"] == jti


def test_decode_expired_token_raises():
    secret = "a" * 32
    token, _ = JWTManager.create_token(
        {"sub": "1", "type": "access"},
        secret,
        -1,
    )

    with pytest.raises(TokenExpiredError):
        JWTManager.decode_token(token, secret)


def test_decode_invalid_token_raises():
    secret = "a" * 32

    with pytest.raises(TokenInvalidError):
        JWTManager.decode_token("not.a.jwt", secret)
