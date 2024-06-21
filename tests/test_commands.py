# ruff: noqa: S101, PT004

import time
from pathlib import Path
from typing import Generator

import pytest

from xh.commands import get_all_unique_commands, get_top_commands, insert_command
from xh.interfaces.file_interface import FileInterface

filedb = Path(Path(__file__).parent, "filedb")


@pytest.fixture(autouse=True)
def pre_post_execution() -> Generator[None, None, None]:
    filedb.unlink(missing_ok=True)

    yield

    filedb.unlink()


def test_file_interface() -> None:
    filedb.unlink(missing_ok=True)
    with FileInterface(filedb) as fi:
        timestamp = int(time.time_ns() / 1_000_000)
        command = "cd"

        insert_command(database=fi, command=command, timestamp=timestamp)

        commands = fi.get_all_unique_commands()

        assert commands[0] == command


def test_unique() -> None:
    filedb.unlink(missing_ok=True)
    length = 3

    with FileInterface(filedb) as fi:
        insert_command(fi, "cd", 100)
        insert_command(fi, "ls", 100)
        insert_command(fi, "cat", 100)

        unique = get_all_unique_commands(fi)

        assert len(unique) == length
        assert "cd" in unique
        assert "ls" in unique
        assert "cat" in unique


def test_count() -> None:
    filedb.unlink(missing_ok=True)
    with FileInterface(filedb) as fi:
        count = 6
        for i in range(count):
            insert_command(fi, "cd", 100)

        top = get_top_commands(fi, 1)
        assert top == "1.\t6\tcd"
