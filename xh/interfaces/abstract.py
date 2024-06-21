from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Mapping, Self


class DBInterface(ABC):
    @abstractmethod
    def __init__(self, **kwargs: Mapping[str, Any]) -> None: ...

    @abstractmethod
    def __enter__(self) -> Self: ...

    @abstractmethod
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: TracebackType | None
    ) -> None: ...

    @abstractmethod
    def get_top_commands(self, number: int) -> list[tuple[int, str]]: ...

    @abstractmethod
    def get_all_unique_commands(self) -> list[str]: ...

    @abstractmethod
    def insert_command(self, command: str, timestamp: int) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
