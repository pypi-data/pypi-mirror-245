import typing as _t
from .common import Screen as _Screen
from ..utils.result import Err as _Err, Ok as _Ok, Result as _Result

_T = _t.TypeVar("_T")


class OptionScreen(_Screen[_T]):
    def __init__(
        self,
        numbered_options: _t.Tuple[_t.Tuple[str, _T]],
        keyword_options: _t.Dict[str, _t.Tuple[str, _T]],
        header: str = "Pick an option:",
        name: _t.Union[str, None] = None,
    ) -> None:
        super().__init__(name)
        self.numbered_options = numbered_options
        self.keyword_options = keyword_options
        self.header = header

    def process_input(self, user_input: str) -> _Result[_T]:
        if len(user_input) < 1:
            return _Err("Empty input")

        if user_input.isdecimal():
            nth_option = int(user_input) - 1
            if nth_option < 0 or nth_option >= len(self.numbered_options):
                return _Err(f"Invalid numbered option '{user_input}'")
            _, option = self.numbered_options[nth_option]
            return _Ok(option)

        _, option = self.keyword_options.get(user_input, ("", None))
        if option is None:
            return _Err(f"Invalid keyword option '{user_input}'")

        return _Ok(option)

    def get_display_string(self) -> str:
        display_string = f"{self.header}\n"

        for nth, (option_description, _) in enumerate(self.numbered_options, start=1):
            display_string += f" {nth} - {option_description}\n"

        if len(self.numbered_options) > 0:
            display_string += "\n"

        for key, (option_description, _) in self.keyword_options.items():
            display_string += f" {key} - {option_description}\n"

        if len(self.keyword_options) > 0:
            display_string += "\n"

        return display_string
