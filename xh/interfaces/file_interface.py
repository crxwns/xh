from collections import Counter
from pathlib import Path
from types import TracebackType
from typing import Self

from xh.interfaces.abstract import DBInterface


class FileInterface(DBInterface):
    def __init__(self, filepath: Path) -> None:
        self._fileobject = filepath.open("a+")

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: TracebackType | None
    ) -> None:
        self.close()

    def close(self) -> None:
        self._fileobject.close()

    def get_top_commands(self, number: int) -> list[tuple[int, str]]:
        commands: list[str] = []
        self._fileobject.seek(0)
        commands = [line.split(";")[0] for line in self._fileobject]
        counter = Counter(commands).most_common(number)
        return [(t[1], t[0]) for t in counter]

    def get_all_unique_commands(self) -> list[str]:
        unique: set[str] = set()
        self._fileobject.seek(0)
        for line in self._fileobject:
            unique.add(line.split(";")[0])
        return list(unique)

    def insert_command(self, command: str, timestamp: int) -> None:
        self._fileobject.write(f"{command};{timestamp}\n")
