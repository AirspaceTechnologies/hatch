import os
import pytest
from unittest.mock import patch, MagicMock
from lib.assistant_base import AssistantBase, AssistantResponse


@pytest.fixture
@patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
@patch("lib.assistant_base.OpenAI")
@patch.object(AssistantBase, "load_config", return_value={"id": "test_id"})
def assistant_fixture(mock_load_config, MockOpenAI):
    mock_client = MagicMock()
    MockOpenAI.return_value = mock_client
    assistant = AssistantBase()
    return assistant, mock_client


@patch("lib.assistant_base.os.path.exists")
@patch("builtins.open")
@patch("json.load")
def test_load_config(mock_json_load, mock_open, mock_path_exists, assistant_fixture):
    assistant, _ = assistant_fixture
    mock_path_exists.return_value = True
    mock_json_load.return_value = {"id": "test_id"}

    config = assistant.load_config()
    assert config == {"id": "test_id"}
    mock_open.assert_called_once()
    mock_json_load.assert_called_once()


def test_camel_to_snake(assistant_fixture):
    assistant, _ = assistant_fixture
    assert assistant.camel_to_snake("CamelCaseName") == "camel_case_name"


@patch("lib.assistant_base.EventHandler")
@patch.object(AssistantBase, "load_config", return_value={"id": "test_id"})
def test_message(mock_load_config, MockEventHandler, assistant_fixture):
    assistant, mock_client = assistant_fixture
    mock_thread = MagicMock()
    mock_client.beta.threads.create.return_value = mock_thread
    mock_stream = MagicMock()
    mock_thread.id = "test_thread_id"
    MockEventHandler.return_value = mock_stream
    mock_stream.__enter__.return_value.text_deltas = iter(["Hello, World!"])

    # Mock the session to return a specific message
    mock_message = MagicMock()
    mock_message.thread_id = "test_thread_id"
    assistant.session.get_last_message = MagicMock(return_value=mock_message)

    result = assistant.message("Hello World")

    mock_client.beta.threads.create.assert_called_once()
    mock_client.beta.threads.messages.create.assert_called_once_with(
        thread_id="test_thread_id", role="user", content="Hello World"
    )

    assert list(mock_stream.__enter__.return_value.text_deltas) == ["Hello, World!"]
    assert result.message == mock_message
    assert result.thread.id == mock_message.thread_id


def test_assistant_response():
    mock_message = MagicMock()
    mock_thread = MagicMock()
    response = AssistantResponse(mock_message, mock_thread)

    assert response.message == mock_message
    assert response.thread == mock_thread
