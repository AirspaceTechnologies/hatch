import os
import openai


class CostCalculator:
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def calculate_cost(self, model, completion_tokens, prompt_tokens):
        model_costs = {
            "gpt-3.5-turbo": {"input": 0.50 / 1_000_000, "output": 1.50 / 1_000_000},
            "gpt-4o": {"input": 5.00 / 1_000_000, "output": 15.00 / 1_000_000},
            "gpt-4-turbo": {"input": 10.00 / 1_000_000, "output": 30.00 / 1_000_000},
            "gpt-4": {"input": 30.00 / 1_000_000, "output": 60.00 / 1_000_000},
        }

        if model in model_costs:
            input_cost = model_costs[model]["input"] * prompt_tokens
            output_cost = model_costs[model]["output"] * completion_tokens
            total_cost = input_cost + output_cost
        else:
            input_cost = output_cost = total_cost = 0.0

        return input_cost, output_cost, total_cost
