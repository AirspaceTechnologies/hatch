import pytest
import json
from unittest.mock import patch, MagicMock, PropertyMock
from lib.event_handler import EventHandler


@pytest.fixture
def event_handler():
    return EventHandler()


@patch("lib.event_handler.get_assistant_instance", autospec=True)
@patch("lib.event_handler.client.beta.threads.runs.submit_tool_outputs_stream", autospec=True)
def test_handle_requires_action(mock_submit_tool_outputs_stream, mock_get_assistant_instance, event_handler):
    mock_data = MagicMock()
    mock_data.assistant_id = "test_id"
    mock_data.required_action.submit_tool_outputs.tool_calls = []
    mock_run_id = "test_run_id"
    mock_assistant = MagicMock()
    mock_get_assistant_instance.return_value = mock_assistant
    mock_submit_tool_outputs_stream.return_value.__enter__.return_value = MagicMock()

    type(event_handler).current_run = PropertyMock(return_value=MagicMock(thread_id="test_thread_id", id="test_run_id"))
    event_handler._submit_tool_outputs = MagicMock()

    event_handler.handle_requires_action(mock_data, mock_run_id)
    event_handler._submit_tool_outputs.assert_called_once()


def test_handle_requires_action_missing_data(event_handler):
    """Test handling of missing required_action data"""
    mock_data = MagicMock()
    mock_data.assistant_id = "test_id"
    mock_data.required_action = None

    with pytest.raises(AttributeError):
        event_handler.handle_requires_action(mock_data, "mock_run_id")


@patch("lib.event_handler.get_assistant_instance")
def test_handle_tool_call_invalid_function(mock_get_assistant_instance, event_handler):
    """Test handling of invalid function name in tool call"""
    mock_assistant = MagicMock()
    mock_get_assistant_instance.return_value = mock_assistant
    
    mock_tool = MagicMock()
    mock_tool.function.name = "nonexistent_function"
    mock_tool.function.arguments = "{}"
    
    with pytest.raises(AttributeError):
        event_handler._handle_tool_call(mock_assistant, mock_tool)


def test_on_timeout(event_handler, capsys):
    """Test timeout handling"""
    event_handler.on_timeout()
    captured = capsys.readouterr()
    assert "Timeout: Request timed out" in captured.out


def test_on_run_failed(event_handler, capsys):
    """Test run failure handling"""
    mock_data = MagicMock()
    mock_data.last_error.code = "error_code"
    mock_data.last_error.message = "error_message"
    
    with pytest.raises(SystemExit):
        event_handler.handle_run_failed(mock_data)
    
    captured = capsys.readouterr()
    assert "Run failed: error_code" in captured.out
    assert "error_message" in captured.out


@patch("lib.event_handler.get_assistant_instance")
def test_on_event_exception_handling(mock_get_assistant_instance, event_handler, capsys):
    """Test exception handling in on_event"""
    mock_event = MagicMock()
    mock_event.event = "thread.run.requires_action"
    mock_event.data.id = "test_id"
    
    # Make get_assistant_instance raise an exception
    mock_get_assistant_instance.side_effect = Exception("Test exception")
    
    event_handler.on_event(mock_event)
    
    captured = capsys.readouterr()
    assert "Exception:" in captured.out
    assert "Test exception" in captured.out


def test_handle_tool_calls_malformed_json(event_handler):
    """Test handling of malformed JSON in tool call arguments"""
    mock_run_step = MagicMock()
    mock_run_step.assistant_id = "test_id"
    mock_run_step.step_details.tool_calls = [MagicMock()]
    mock_run_step.step_details.tool_calls[0].type = "function"
    mock_run_step.step_details.tool_calls[0].function.arguments = "invalid json"
    
    with pytest.raises(json.JSONDecodeError):
        event_handler.handle_tool_calls(mock_run_step)
