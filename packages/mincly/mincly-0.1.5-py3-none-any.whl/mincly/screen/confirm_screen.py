import re as _re
import typing as _t
from .common import Screen as _Screen
from ..utils.result import Err as _Err, Ok as _Ok, Result as _Result


class ConfirmScreen(_Screen[bool]):
    def __init__(
        self,
        message: str,
        true_regex: str = r"^[Yy]|[Yy][Ee][Ss]$",
        default_no_input: _t.Union[bool, None] = None,
        screen_name: _t.Union[str, None] = None,
    ) -> None:
        super().__init__(screen_name)
        self.message = message
        self.true_regex = _re.compile(true_regex)
        self.default = default_no_input

    def get_display_string(self) -> str:
        return self.message

    def process_input(self, user_input: str) -> _Result[bool]:
        if self.true_regex.match(user_input):
            return _Ok(True)
        elif len(user_input) < 1:
            return _Err("Empty input") if self.default is None else _Ok(self.default)
        else:
            return _Ok(False)
