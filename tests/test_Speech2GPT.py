# tests/test_Speech2GPT.py
import json

import pytest
from typer.testing import CliRunner

from Speech2GPT import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__, 
    __version__,
    cli,
    Speech2GPT
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} version {__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    """Create a mock JSON file."""
    s2data = [{"Prompt": "What is the capital of Assyria?", "Response": "Probably Nineveh"}]
    db_file = tmp_path / "mock.json"
    with db_file.open("w") as db:
        json.dump(s2data, db, indent=4)
    return db_file

test_data1 = {
    "prompt": ["Please", "give", "me", "a", "sentence", "to", "complete."],
    "response": ["The", "completed", "sentence"],
    "s2gpt": {
        "Prompt": "Please give me a sentence to complete.", 
        "Response": "The completed sentence."
        },
}

test_data2 = {
    "prompt": ["Another", "sentence", "for", "me", "to", "complete"],
    "response": ["The", "completed", "response", "to", "the", "sentence"],
    "s2gpt": {
        "Prompt": "Another sentence for me to complete.", 
        "Response": "The completed response to the sentence."
        },
}

@pytest.mark.parametrize(
    "prompt, response, expected",
    [
        pytest.param(
            test_data1["prompt"],
            test_data1["response"],
            (test_data1["s2gpt"], SUCCESS),
        ),
        pytest.param(
            test_data2["prompt"],
            test_data2["response"],
            (test_data2["s2gpt"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, prompt, response, expected):
    speech2GPT = Speech2GPT.Speech2GPT(mock_json_file)
    assert speech2GPT.add(prompt, response) == expected
    read = speech2GPT._db_handler.read_s2gpt()
    assert len(read.s2gpt_list) == 2