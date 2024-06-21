"""XtendedHistory."""

import argparse
import sys
import time
from pathlib import Path

from xh.commands import get_all_unique_commands, get_top_commands, insert_command, sanitize_command
from xh.interfaces.sqlite_interface import SQLiteInterface


def main() -> None:
    """Main entrypoint for CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--command",
        help="Add a command to the database of xh. If no timestamp is provided, the current time will be used.",
        required=False,
    )
    parser.add_argument(
        "-t",
        "--timestamp",
        help="The timestamp of the command in Unix milliseconds. If not provided the current time will be used.",
        required=False,
        default=int(time.time_ns() / 1_000_000),
    )
    parser.add_argument(
        "-db",
        "--database",
        help="Filepath to the SQLite Database. Default `$HOME/.xhdb`.",
        required=False,
        default=str(Path(Path.home(), ".xhdb").absolute()),
    )
    parser.add_argument(
        "-m",
        "--migrate",
        help="Migrate all commands from a history file to xh. E.g. xh -m (Get-PSReadlineOption).HistorySavePath",
        required=False,
    )
    parser.add_argument(
        "-u",
        "--unique",
        help="Retrieve all unique commands from the database as a newline seperated list.",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-top",
        "--topten",
        help="Get a list of the top X commands used.",
        required=False,
        nargs="?",
        type=int,
        const=10,
    )

    args = parser.parse_args()

    db_folder = Path(args.database).parent
    if not db_folder.exists():
        raise AssertionError(f"Path doesn't exist: {db_folder}")

    with SQLiteInterface(db_file_path=Path(args.database)) as database:
        if args.command:
            command = sanitize_command(args.command)
            insert_command(database=database, command=command, timestamp=args.timestamp)

        if args.unique:
            commands = get_all_unique_commands(database=database)
            sys.stdout.write("\n".join(commands))

        if args.topten:
            if not isinstance(args.topten, int):
                raise TypeError("Topten needs to be an Integer.")
            commands = get_top_commands(database=database, number=args.topten)
            sys.stdout.write(commands)

        if args.migrate:
            history_file = Path(args.migrate)
            if not history_file.exists():
                raise AssertionError(f"File doesn't exist: {history_file}")

            with history_file.open() as history:
                for line in history:
                    sanitize_command(line)
                    database.insert_command(command=line, timestamp=args.timestamp)
