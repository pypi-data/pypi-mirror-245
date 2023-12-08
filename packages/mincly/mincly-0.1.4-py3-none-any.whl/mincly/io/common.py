from abc import ABC as _Abstract, abstractmethod as _abstract


class Reader(_Abstract):
    @_abstract
    def read(self) -> str:
        """Collect input from user or any source."""
        raise NotImplementedError()


class SupportsWrite(_Abstract):
    @_abstract
    def write(self, message: str):
        """Sends message to output (e.g. by printing)."""
        raise NotImplementedError()


class Writer(SupportsWrite):
    @_abstract
    def clear(self):
        """Clears output (e.g. by removing printed content)"""
        raise NotImplementedError()


class Io(Reader, Writer):
    pass


class HybridIo(Io):
    def __init__(self, input: Reader, output: Writer) -> None:
        self.__in = input
        self.__out = output

    def write(self, message: str):
        return self.__out.write(message)

    def clear(self):
        return self.__out.clear()

    def read(self) -> str:
        return self.__in.read()
