class UserException(Exception):
    def __init__(self, details: str) -> None:
        super().__init__(details)
