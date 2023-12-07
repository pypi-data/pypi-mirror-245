class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid credentials"):
        super().__init__(message)


class APIException(Exception):
    def __init__(self, error_info):
        super().__init__(error_info)
