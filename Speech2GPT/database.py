"""This module provides the database functionality of the Speech2GPT project."""
# Speech2GPT/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from Speech2GPT import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_speech2gpt.json"
)

class DBResponse(NamedTuple):
    """This class represents a response from the database"""
    s2gpt_list: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_s2gpt(self) -> DBResponse:
        """Read the Speech2GPT database"""
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_s2gpt(self, s2gpt_list: List[Dict[str, Any]]) -> DBResponse:
        """Write to the Speech2GPT database"""
        try:
            with self._db_path.open("w") as db:
                json.dump(s2gpt_list, db, indent=4)
            return DBResponse(s2gpt_list, SUCCESS)
        except OSError:
            return DBResponse(s2gpt_list, DB_WRITE_ERROR)

def get_database_path(config_file: Path) -> Path:
    """Get the database path from the config file"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Initialize the database"""
    try:
        db_path.write_text("[]") # Write an empty list to the database file
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR