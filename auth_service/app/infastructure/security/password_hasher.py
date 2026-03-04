import bcrypt


class PasswordHasher:
    def __init__(self) -> None:
        pass

    def get(
        self,
        password: str,
    ) -> str:
        return bcrypt.hashpw(
            password=bytes(password, encoding="utf-8"),
            salt=bcrypt.gensalt(),
        ).decode()

    def check(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return bcrypt.checkpw(
            password=bytes(password, encoding="utf-8"),
            hashed_password=bytes(password_hash, encoding="utf-8"),
        )
