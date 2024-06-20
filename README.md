# About

Small Python tool to grab all executed commands, add them to a SQLite Database (Default DB file $HOME/.xhdb) and read all commands.

# TODO

- [ ] Input sanitization
  - [ ] Remove leading and trailing whitespaces and newlines during insertion
- [ ] Add the possibility to ignore commands like `cd` and `ls`
  - [ ] Maybe with configfile or by passing in a list of ignored commands?
- [ ] Rethink DB Schema
  - [ ] Split Command to multiple columns <command> <arguments> <fullcommand>
- [ ] Run `xh` in the Background to not block the execution of commands in Powershell
- [ ] Prebuilt the package and look for a good way of distributing
- [ ] Evaluate Click to replace argparse
- [ ] Evaluate Rich for a TUI
  - [ ] Create a Heatmap of commands used per day
- [ ] Evaluate the usage of an ORM + Migrations
- [ ] Try integration with bash
- [ ] Build a prototype in rust and compare performance
  - [ ] If everything is just IO bound theres no need to switch lanuages i guess

# Installation

## Build

Build with Poetry

```
$ poetry build
```

## Install

Using Python installation:

```
$ pip install .\dist\xh-0.1.0-py3-none-any.whl
```

Using pipx

```
$ pipx install .\dist\xh-0.1.0-py3-none-any.whl
```

## Powershell Profile

Edit your Powershell Profile (`code $PROFILE`)

Overwrite `Enter` to get current input buffer and write in the `xh` database.

```powershell
Set-PSReadlineKeyHandler -Key Enter -ScriptBlock {
    $line = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$null)

    try {
        xh -c $line
    } catch {}

    [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
}
```

Use `xh` and `fzf` to get an interactive search through your history.

```powershell
Set-PSReadlineKeyHandler -Key Ctrl+r -ScriptBlock {
    $result = $null
    try {
        $result = xh --unique | fzf
    }
    catch {
        # catch custom exception
    }
    if (-not [string]::IsNullOrEmpty($result)) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert($result)
    }
}
```

# Usage

```
usage: xh [-h] [-c COMMAND] [-t TIMESTAMP] [-db DATABASE] [-m MIGRATE] [-u]

options:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        The command to insert into the xh database.
  -t TIMESTAMP, --timestamp TIMESTAMP
                        The timestamp of the command in Unix milliseconds. If not provided the current time will be used.
  -db DATABASE, --database DATABASE
                        Filepath to the SQLite Database. Default `$HOME/.xhdb`.
  -m MIGRATE, --migrate MIGRATE
                        Migrate all commands from a history file to xh. E.g. xh -m (Get-PSReadlineOption).HistorySavePath
  -u, --unique          Retrieve all unique commands from the database as a newline seperated list.
```
