from xh.interfaces.abstract import DBInterface


def sanitize_command(command: str) -> str:
    return command.strip().lstrip()


def insert_command_into_database(database: DBInterface, command: str, timestamp: int) -> None:
    """Insert command into Database."""
    if not isinstance(command, str):
        raise TypeError("Command needs to be a string.")
    if not isinstance(timestamp, int):
        raise TypeError("Timestamp needs to be an integer.")

    database.insert_command(command=command, timestamp=timestamp)


def get_unique_commands(database: DBInterface) -> list[str]:
    """Collect all unique Commands from Database."""
    commands: list[str] = database.get_all_unique_commands()
    return commands


def get_top_number_commands(database: DBInterface, number: int) -> str:
    """Retrieve top ten commands from Database."""
    commands = database.get_top_commands(number=number)
    return "\n".join([f"{idx + 1}.\t{count}\t{command}" for idx, (count, command) in enumerate(commands)])
