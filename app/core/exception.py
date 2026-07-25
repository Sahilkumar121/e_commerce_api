class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EmailAlreadyExistsException(AppException):

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"Email {email} already exists")

class UnauthorizedException(AppException):
    def __init__(self) -> None:
        super().__init__("Invalid email and Password")

class CredentialException(AppException):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"No User with {user_id} found !")
