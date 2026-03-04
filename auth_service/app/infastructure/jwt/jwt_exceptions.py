class JWTException(Exception):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail)
        self.detail = detail


class JWTExpiredError(JWTException):
    pass


class JWTInvalidError(JWTException):
    pass
