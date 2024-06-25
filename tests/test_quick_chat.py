import pytest
from unittest.mock import patch, MagicMock
from lib.quick_chat import QuickChat


@pytest.fixture
def mock_openai_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Hello, how can I assist you?"))]
    return mock_response


def test_quick_chat_initialization():
    chat_instance = QuickChat()
    assert isinstance(chat_instance, QuickChat)


@patch("lib.quick_chat.OpenAI")
def test_quick_chat_send(mock_openai, mock_openai_response):
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value = mock_openai_response

    chat_instance = QuickChat()
    response = chat_instance.send("Hello")
    assert response == "Hello, how can I assist you?"
