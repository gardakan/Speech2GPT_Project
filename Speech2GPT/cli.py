"""This module provides the command line interface for the Speech2GPT project."""
# Speech2GPT/cli.py

from pathlib import Path
# from Speech2GPT import __version__, __app_name__
import typer
from typing import List, Optional

from Speech2GPT import ERRORS, __app_name__, __version__, config, database, Speech2GPT

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="Database path?",
        help="Path to the database file.",
    ),
) -> None:
    """Initialize the Speech2GPT database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f"Creating the config file failed with {ERRORS[app_init_error]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f"Creating the database failed with {ERRORS[db_init_error]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Speech2GPT initialized successfully.  Database path: {db_path}",
            fg=typer.colors.GREEN
        )
        

def get_s2gpt() -> Speech2GPT.Speech2GPT:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "Speech2GPT init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return Speech2GPT.Speech2GPT(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "Speech2GPT init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
@app.command()
def add(
    prompt: List[str] = typer.Argument(...),
    response: List[str] = typer.Argument(...),
) -> None:
    """Add a new Speech2GPT instance with a PROMPT."""
    speech2gpt = Speech2GPT()
    s2gpt, error = speech2gpt.add(prompt, response)
    if error:
        typer.secho(
            f'Adding Speech2GPT instance failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""S2GPT: "{s2gpt['Prompt']}" was added """
            f"""with response: {response}""",
            fg=typer.colors.GREEN,
        )

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show the version and exit.",
    )
) -> None:
    return