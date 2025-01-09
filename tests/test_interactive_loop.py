import unittest
from unittest.mock import MagicMock, patch
from lib.interactive_loop import InteractiveLoop
from lib.event_handler import EventHandler


class TestInteractiveLoop(unittest.TestCase):
    def setUp(self):
        self.initial_message = "Hello, world!"
        self.mock_agent = MagicMock()
        self.loop = InteractiveLoop(self.initial_message, self.mock_agent)

    def test_initialization(self):
        self.assertEqual(self.loop.initial_message, self.initial_message)
        self.assertEqual(self.loop.agent, self.mock_agent)
        self.assertIsNone(self.loop.thread)

    def test_process_initial_message(self):
        self.loop.process_initial_message(self.initial_message)
        self.mock_agent.message.assert_called_with(self.initial_message)
        self.assertIsNotNone(self.loop.thread)

    def test_process_message(self):
        message = "How are you?"
        self.loop.thread = MagicMock()  # Mock the thread
        self.loop.process_message(message)
        self.mock_agent.message.assert_called_with(message, thread=self.loop.thread)

    @patch("lib.interactive_loop.usage_message", side_effect=SystemExit)
    def test_handle_keyboard_interrupt(self, mock_usage_message):
        with self.assertRaises(SystemExit):
            self.loop.handle_keyboard_interrupt()

    @patch("lib.interactive_loop.usage_message", side_effect=SystemExit)
    def test_handle_eof_error(self, mock_usage_message):
        with self.assertRaises(SystemExit):
            self.loop.handle_eof_error()

    @patch("lib.interactive_loop.usage_message", side_effect=SystemExit)
    def test_handle_general_exception(self, mock_usage_message):
        with self.assertRaises(SystemExit):
            self.loop.handle_general_exception(Exception("Test exception"))


    @patch("lib.event_handler.get_assistant_instance")
    @patch("lib.event_handler.client.beta.threads.runs.submit_tool_outputs_stream", autospec=True)
    def test_interactive_loop_with_event_handler(self, mock_submit_tool_outputs_stream, mock_get_assistant_instance):
        """Integration test for InteractiveLoop with EventHandler"""
        # Set up EventHandler with mocked components
        event_handler = EventHandler()
        mock_assistant = MagicMock()
        mock_get_assistant_instance.return_value = mock_assistant
        mock_submit_tool_outputs_stream.return_value.__enter__.return_value = MagicMock()
        
        # Create a mock agent that will use our EventHandler
        mock_agent = MagicMock()
        mock_agent.message.side_effect = lambda msg, thread=None: MagicMock(
            thread=MagicMock(id="test_thread_id"),
            message=MagicMock(content=[MagicMock(text=MagicMock(value="Response"))])
        )
        
        # Create InteractiveLoop with our agent
        loop = InteractiveLoop("Initial message", mock_agent)
        
        # Process initial message
        loop.process_initial_message("Initial message")
        self.assertIsNotNone(loop.thread)
        mock_agent.message.assert_called_with("Initial message")
        
        # Process a message that would trigger EventHandler
        loop.process_message("Test message")
        mock_agent.message.assert_called_with("Test message", thread=loop.thread)
        
        # Verify the interaction completed successfully
        self.assertEqual(mock_agent.message.call_count, 2)


if __name__ == "__main__":
    unittest.main()
