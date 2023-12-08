import typing as _t

_T = _t.TypeVar("_T")
_R = _t.TypeVar("_R")


class Result(_t.Generic[_T]):
    """Util class to wrap around fallible values instead of raising Exceptions.
    Do not instantiate direcly, instead, use `Err` and `Ok` util functions from
    this package"""

    def __init__(self, value: _t.Union[_T, Exception], is_ok: bool):
        self._value = value
        self._is_ok = is_ok

    @staticmethod
    def from_func(
        func: _t.Callable[[None], _R], catch_system_errors: bool = False
    ) -> "Result[_R]":
        catch_target = BaseException if catch_system_errors else Exception
        try:
            return Ok(func())
        except catch_target as e:
            return Err(e)

    def is_ok(self) -> bool:
        """Returns `True` if this `Result` is of the `Ok` type"""
        return self._is_ok

    def is_err(self) -> bool:
        """Returns `True` if this `Result` is of the `Err` type"""
        return not self._is_ok

    def unwrap(self) -> _T:
        """Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, then raises the wrapped exception, instead."""
        if self._is_ok:
            return self._value
        else:
            raise self._value

    def try_unwrap(self) -> _t.Union[_T, None]:
        """Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, returns `None`."""
        if self._is_ok:
            return self._value
        else:
            return None

    def unwrap_err(self) -> BaseException:
        """Returns the wrapped exception if this `Result` is `Err`, else, if
        this `Result` is `Ok`, then raises a `TypeError`."""
        if not self._is_ok:
            return self._value
        else:
            raise TypeError("Can't unwrap error type in instance of Ok result.")


def Err(error: _t.Union[BaseException, str]) -> Result[_T]:
    """Instantiate Error Result which wraps around exception. If `error` is
    a string, will instantiate an `Exception` with `error` as error message."""
    if isinstance(error, str):
        return Result(Exception(error), False)
    return Result(error, False)


def Ok(value: _T) -> Result[_T]:
    """Instantiate Ok Result which wraps around a `value` (use `None` if
    value is irrelevant)"""
    return Result(value, True)
