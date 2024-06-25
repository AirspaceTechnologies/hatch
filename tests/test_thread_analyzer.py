import unittest
from unittest.mock import patch, MagicMock
from lib.thread_analyzer import ThreadAnalyzer


class TestThreadAnalyzer(unittest.TestCase):
    @patch("lib.thread_analyzer.openai")
    def test_no_messages_or_runs(self, mock_openai):
        mock_openai.beta.threads.messages.list.return_value = []
        mock_openai.beta.threads.runs.list.return_value = []

        analyzer = ThreadAnalyzer(thread_id="test_thread")
        analyzer.analyze_thread()

        self.assertIn("test_thread", analyzer.analysis_results)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_messages"], 0)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_runs"], 0)

    @patch("lib.thread_analyzer.openai")
    @patch("lib.thread_analyzer.CostCalculator")
    def test_analyze_thread_with_mock_data(self, MockCostCalculator, mock_openai):
        mock_messages = [MagicMock()] * 5
        mock_runs = [MagicMock()] * 3
        mock_steps = [MagicMock()] * 4

        mock_openai.beta.threads.messages.list.return_value = mock_messages
        mock_openai.beta.threads.runs.list.return_value = mock_runs
        mock_openai.beta.threads.runs.steps.list.return_value = mock_steps

        mock_run = MagicMock()
        mock_run.id = "run_id"
        mock_run.model = "model"
        mock_run.status = "status"
        mock_run.usage = MagicMock()
        mock_run.usage.completion_tokens = 10
        mock_run.usage.prompt_tokens = 20
        mock_run.usage.total_tokens = 30
        mock_openai.beta.threads.runs.list.return_value = [mock_run]

        mock_assistant = MagicMock()
        mock_assistant.name = "assistant_name"
        mock_openai.beta.assistants.retrieve.return_value = mock_assistant

        mock_cost_calculator = MockCostCalculator.return_value
        mock_cost_calculator.calculate_cost.return_value = (0.1, 0.2, 0.3)

        analyzer = ThreadAnalyzer(thread_id="test_thread")
        analyzer.analyze_thread()

        self.assertIn("test_thread", analyzer.analysis_results)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_messages"], 5)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_runs"], 1)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_run_steps"], 4)

    @patch("lib.thread_analyzer.openai")
    def test_error_handling(self, mock_openai):
        mock_openai.beta.threads.messages.list.side_effect = Exception("API Error")

        analyzer = ThreadAnalyzer(thread_id="test_thread")
        with self.assertRaises(Exception) as context:
            analyzer.analyze_thread()

        self.assertTrue("API Error" in str(context.exception))

    @patch("lib.thread_analyzer.openai")
    def test_edge_case_token_usage(self, mock_openai):
        mock_messages = [MagicMock()] * 2
        mock_runs = [MagicMock()] * 1
        mock_steps = [MagicMock()] * 3

        mock_openai.beta.threads.messages.list.return_value = mock_messages
        mock_openai.beta.threads.runs.list.return_value = mock_runs
        mock_openai.beta.threads.runs.steps.list.return_value = mock_steps

        mock_run = MagicMock()
        mock_run.id = "run_id"
        mock_run.model = "model"
        mock_run.status = "status"
        mock_run.usage = MagicMock()
        mock_run.usage.completion_tokens = 0
        mock_run.usage.prompt_tokens = 0
        mock_run.usage.total_tokens = 0
        mock_openai.beta.threads.runs.list.return_value = [mock_run]

        analyzer = ThreadAnalyzer(thread_id="test_thread")
        analyzer.analyze_thread()

        self.assertIn("test_thread", analyzer.analysis_results)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_completion_tokens"], 0)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_prompt_tokens"], 0)
        self.assertEqual(analyzer.analysis_results["test_thread"]["total_token_usage"], 0)


if __name__ == "__main__":
    unittest.main()
