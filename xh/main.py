"""XtendedHistory."""

import argparse
import sqlite3
import sys
import time
from pathlib import Path


def main() -> None:
    """Main entrypoint for CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", help="The command to store", required=False)
    parser.add_argument(
        "-t",
        "--timestamp",
        help="The timestamp of the command in Unix milliseconds",
        required=False,
        default=int(time.time_ns() / 1_000_000),
    )
    parser.add_argument(
        "-db",
        "--database",
        help="Filepath to the SQLite Database to store commands",
        required=False,
        default=str(Path(Path.home(), ".xhdb").absolute()),
    )
    parser.add_argument("--migrate", required=False)
    parser.add_argument("--unique", required=False, action="store_true")
    args = parser.parse_args()

    db_folder = Path(args.database).parent
    if not db_folder.exists():
        raise AssertionError(f"Path doesn't exist: {db_folder}")

    cursor, connection = initialize_db(database=args.database)

    if args.command:
        insert_command(cursor=cursor, command=args.command, timestamp=args.timestamp)

    if args.migrate:
        history_file = Path(args.migrate)
        if not history_file.exists():
            raise AssertionError(f"File doesn't exist: {history_file}")

        with history_file.open() as history:
            for line in history:
                insert_command(cursor=cursor, command=line, timestamp=args.timestamp)

    if args.unique:
        commands = get_all_unique_commands(cursor=cursor)
        sys.stdout.write("\n".join(commands))

    connection.commit()
    connection.close()


def insert_command(cursor: sqlite3.Cursor, command: str, timestamp: int) -> None:
    """Insert command into Database."""
    if not isinstance(command, str):
        raise TypeError("Command needs to be a string.")
    if not isinstance(timestamp, int):
        raise TypeError("Timestamp needs to be an integer.")

    stripped_command = command.lstrip().rstrip()

    cursor.execute(
        "INSERT INTO commands (command, timestamp_ms) VALUES (?, ?)",
        (stripped_command, timestamp),
    )


def initialize_db(database: str) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """Initialize Database and returns connection and cursor."""
    connection: sqlite3.Connection = sqlite3.connect(database)
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS commands(id INTEGER PRIMARY KEY AUTOINCREMENT, command TEXT, timestamp_ms INTEGER)",
    )
    return cursor, connection


def get_all_unique_commands(cursor: sqlite3.Cursor) -> list[str]:
    """Collect all unique Commands from Database."""
    commands: list[tuple[str]] = cursor.execute("SELECT DISTINCT(TRIM(LTRIM(command))) FROM commands").fetchall()
    return [command[0].strip().lstrip() for command in commands if command]


if __name__ == "__main__":
    main()