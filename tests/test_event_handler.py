import pytest
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
