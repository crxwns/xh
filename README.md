# About

Small Python tool to grab all executed commands, add them to a SQLite Database (Default DB file $HOME/.xhdb) and read all commands.

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
