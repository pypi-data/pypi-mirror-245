from mincly.io.common import (
    Io as _Io,
    Writer as _Writer,
    Reader as _Reader,
    HybridIo as _HybridIo,
)
from mincly.io.standard import (
    StandardTerminalReader as _StandardTerminalReader,
    StandardTerminalWriter as _StandardTerminalWriter,
    StandardTerminalIo as _StandardTerminalIo,
)


class Menu:
    def __init__(
        self,
        input_output: _Io = None,
        input: _Reader = None,
        output: _Writer = None,
    ) -> None:
        self.__io: _Io
        if input_output is not None:
            self.__io = input_output
        elif input is not None or output is not None:
            input_or_standard = (
                input if input is not None else _StandardTerminalReader()
            )
            output_or_standard = (
                output if output is not None else _StandardTerminalWriter()
            )
            self.__io = _HybridIo(input_or_standard, output_or_standard)
        else:
            self.__io = _StandardTerminalIo()
