from dishka import Provider, Scope, provide  # type: ignore[misc]
from .password_hasher import PasswordHasher


class PasswordHasherProvider(Provider):
    @provide(scope=Scope.APP)
    def password_hasher(
        self,
    ) -> PasswordHasher:
        return PasswordHasher()
