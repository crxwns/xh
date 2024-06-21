import sqlite3
from pathlib import Path
from types import TracebackType
from typing import Self

from xh.interfaces.abstract import DBInterface


class SQLiteInterface(DBInterface):
    """Implements SQLite Interface."""

    def __init__(self, db_file_path: Path) -> None:
        """Initalize SQLite Database."""
        self._connection: sqlite3.Connection = sqlite3.connect(db_file_path)
        self._cursor: sqlite3.Cursor = self._connection.cursor()
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS commands(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                timestamp_ms INTEGER
            )""",
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: TracebackType | None
    ) -> None:
        self.close()

    def close(self) -> None:
        self._connection.commit()
        self._connection.close()

    def get_top_commands(self, number: int) -> list[tuple[int, str]]:
        """Get the top X commands by number of calls."""
        self._cursor.execute(
            """
            SELECT count(command),
                TRIM(command, '\n')
            FROM commands
            GROUP by command
            ORDER by count(command) DESC
            LIMIT ?
            """,
            (number,),
        )
        return self._cursor.fetchall()

    def get_all_unique_commands(self) -> list[str]:
        """Gets all unique commands."""
        self._cursor.execute("SELECT DISTINCT(TRIM(LTRIM(command))) FROM commands")
        commands: list[tuple[str]] = self._cursor.fetchall()
        return [command[0] for command in commands if command]

    def insert_command(self, command: str, timestamp: int) -> None:
        """Insert a command into the Database."""
        self._cursor.execute(
            """
            INSERT INTO commands (command, timestamp_ms)
            VALUES (?, ?)
            """,
            (command, timestamp),
        )
