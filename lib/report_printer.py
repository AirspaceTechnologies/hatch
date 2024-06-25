class ReportPrinter:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def print_run_details(self, run_analysis, run_index):
        print(f"\nRun {run_index + 1}:")
        print(f"    model: {run_analysis['model']}")
        print(f"    assistant: {run_analysis['assistant_name']}")
        print(f"    run steps: {run_analysis['step_count']}")
        print(f"    token in: {run_analysis['prompt_tokens']}")
        print(f"    token out: {run_analysis['completion_tokens']}")
        print(f"    token total: {run_analysis['total_tokens']}")
        print(f"    cost in: ${run_analysis['input_cost']:.6f}")
        print(f"    cost out: ${run_analysis['output_cost']:.6f}")
        print(f"    total run cost: ${run_analysis['total_run_cost']:.6f}")

    def print_thread_analysis(self, thread_id):
        analysis = self.analyzer.analysis_results.get(thread_id)
        if not analysis:
            print(f"No analysis found for thread: {thread_id}")
            return

        print(f"thread: {thread_id}")
        print(f"    total messages: {analysis['total_messages']}")
        print(f"    total runs: {analysis['total_runs']}")

        for index, run_analysis in enumerate(analysis["runs"]):
            self.print_run_details(run_analysis, index)

        print(f"\ntotal run steps: {analysis['total_run_steps']}")
        print(f"total tokens in: {analysis['total_prompt_tokens']}")
        print(f"total tokens out: {analysis['total_completion_tokens']}")
        print(f"total tokens: {analysis['total_token_usage']}")
        print(f"\ntotal cost: ${analysis['total_thread_cost']:.6f}")
