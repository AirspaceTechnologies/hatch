import unittest
from unittest.mock import MagicMock, patch
from lib.interactive_loop import InteractiveLoop


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


if __name__ == "__main__":
    unittest.main()
