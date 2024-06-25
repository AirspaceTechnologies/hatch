import json
from unittest.mock import patch, mock_open, MagicMock
from lib.utilities import (
    build_assistant_map,
    camel_to_snake,
    get_assistant_instance,
    human_message,
    system_message,
    function_call_message,
    assistant_message,
)
from io import StringIO
import sys


def test_build_assistant_map():
    mock_json_data = {"id": "test_id", "name": "TestName"}

    with patch("os.listdir", return_value=["config.json"]), patch(
        "builtins.open", mock_open(read_data=json.dumps(mock_json_data))
    ), patch("json.load", return_value=mock_json_data):
        assistant_map = build_assistant_map()
        assert assistant_map == {"test_id": "TestName"}


def test_camel_to_snake():
    assert camel_to_snake("CamelCaseName") == "camel_case_name"


def test_get_assistant_instance():
    mock_assistant_class = MagicMock()
    mock_assistant_map = {"test_id": "TestAssistant"}

    with patch("lib.utilities.camel_to_snake", return_value="test_assistant"), patch(
        "importlib.import_module", return_value=MagicMock(TestAssistant=mock_assistant_class)
    ):
        instance = get_assistant_instance("test_id", mock_assistant_map)
        assert instance == mock_assistant_class.return_value


def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    func(*args, **kwargs)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return output


def test_human_message():
    output = capture_output(human_message, "Hello", "TestAgent")
    assert "TestAgent" in output
    assert "Hello" in output


def test_system_message():
    output = capture_output(system_message, "System Message", "System")
    assert "System" in output
    assert "System Message" in output


def test_function_call_message():
    output = capture_output(function_call_message, "Function Message", 0, "FunctionTitle")
    assert "FunctionTitle" in output
    assert "Function Message" in output


def test_assistant_message():
    output = capture_output(assistant_message, "Assistant Message", 3, "Assistant")
    assert "Assistant" in output
    assert "Assistant Message" in output
