# Register Exceptions


class RegisterError(Exception):
    """
    Base register exception
    """

    pass


class UserAlreadyExists(RegisterError):
    """
    User already exists
    """

    pass


# Authenticate Exceptions


class AuthError(Exception):
    """
    Base authenticate exception
    """

    pass


class TokenExpiredError(AuthError):
    """
    Token expired
    """

    pass


class TokenInvalidError(AuthError):
    """
    Token is invalid
    """

    pass