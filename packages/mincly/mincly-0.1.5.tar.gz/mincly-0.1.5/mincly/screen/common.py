from abc import ABC as _Abstract
import typing as _t
from ..utils.result import Result as _Result

_T = _t.TypeVar("_T")


class Screen(_Abstract, _t.Generic[_T]):
    from abc import abstractmethod as abstract

    def __init__(self, screen_name: _t.Union[str, None] = None) -> None:
        self.name = screen_name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.name if self.name is not None else '<NoName>'}')"

    @abstract
    def process_input(self, user_input: str) -> _Result[_T]:
        raise NotImplementedError()

    @abstract
    def get_display_string(self) -> str:
        raise NotImplementedError()
