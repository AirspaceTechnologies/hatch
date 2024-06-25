import os
import openai
from lib.cost_calculator import CostCalculator


class ThreadAnalyzer:
    def __init__(self, thread_id):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.cost_calculator = CostCalculator()
        self.analysis_results = {}
        self.thread_id = thread_id

    def get_messages(self):
        messages = list(openai.beta.threads.messages.list(thread_id=self.thread_id))
        return messages

    def get_runs(self):
        runs = list(openai.beta.threads.runs.list(thread_id=self.thread_id))
        return runs

    def get_assistant_name(self, assistant_id):
        assistant = openai.beta.assistants.retrieve(assistant_id)
        return assistant.name

    def get_run_steps(self, run_id):
        steps = list(openai.beta.threads.runs.steps.list(thread_id=self.thread_id, run_id=run_id))
        return steps

    def analyze_thread(self):
        messages = self.get_messages()
        message_count = len(messages)

        runs = self.get_runs()
        run_count = len(runs)

        total_completion_tokens = 0
        total_prompt_tokens = 0
        total_token_usage = 0
        total_run_steps = 0
        total_input_cost = 0.0
        total_output_cost = 0.0
        total_thread_cost = 0.0

        thread_analysis = {
            "thread_id": self.thread_id,
            "total_messages": message_count,
            "total_runs": run_count,
            "runs": [],
        }

        for index, run in enumerate(runs):
            steps = self.get_run_steps(run.id)
            step_count = len(steps)

            completion_tokens = run.usage.completion_tokens if run.usage else 0
            prompt_tokens = run.usage.prompt_tokens if run.usage else 0
            token_usage = run.usage.total_tokens if run.usage else 0

            input_cost, output_cost, total_run_cost = self.cost_calculator.calculate_cost(
                run.model, completion_tokens, prompt_tokens
            )

            run_analysis = {
                "model": run.model,
                "status": run.status,
                "completion_tokens": completion_tokens,
                "prompt_tokens": prompt_tokens,
                "total_tokens": token_usage,
                "step_count": step_count,
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_run_cost": total_run_cost,
                "assistant_name": self.get_assistant_name(run.assistant_id),
            }

            thread_analysis["runs"].append(run_analysis)

            total_completion_tokens += completion_tokens
            total_prompt_tokens += prompt_tokens
            total_token_usage += token_usage
            total_run_steps += step_count
            total_input_cost += input_cost
            total_output_cost += output_cost
            total_thread_cost += total_run_cost

        thread_analysis.update(
            {
                "total_run_steps": total_run_steps,
                "total_prompt_tokens": total_prompt_tokens,
                "total_completion_tokens": total_completion_tokens,
                "total_token_usage": total_token_usage,
                "total_input_cost": total_input_cost,
                "total_output_cost": total_output_cost,
                "total_thread_cost": total_thread_cost,
            }
        )

        self.analysis_results[self.thread_id] = thread_analysis
