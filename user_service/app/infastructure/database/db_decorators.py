from functools import wraps
from typing import (
    Any,
    Awaitable,
    Coroutine,
    Callable,
    Optional,
    TypeVar,
    ParamSpec,
    Concatenate,
    TYPE_CHECKING,
)
from sqlalchemy.exc import (
    SQLAlchemyError,
    OperationalError,
    DatabaseError,
)
from .db_infrastructure_exceptions import (
    DBOperationalError,
    DBDatabaseError,
    DBSQLAlchemyError,
)

if TYPE_CHECKING:
    from .db_helper import DataBaseHelper

P = ParamSpec("P")
R = TypeVar("R")


def db_exception_handler(
    func: Callable[Concatenate["DataBaseHelper", P], Awaitable[R]],
) -> Callable[Concatenate["DataBaseHelper", P], Coroutine[Any, Any, Optional[R]]]:
    @wraps(func)
    async def wrapper(
        self: "DataBaseHelper", *args: P.args, **kwargs: P.kwargs
    ) -> Optional[R]:
        try:
            return await func(self, *args, **kwargs)

        except OperationalError as e:
            raise DBOperationalError(
                model_name=self.__class__.__name__,
                details=str(e),
            ) from e

        except DatabaseError as e:
            raise DBDatabaseError(
                model_name=self.__class__.__name__,
                details=str(e),
            ) from e

        except SQLAlchemyError as e:
            raise DBSQLAlchemyError(
                model_name=self.__class__.__name__,
                details=str(e),
            ) from e

    return wrapper
