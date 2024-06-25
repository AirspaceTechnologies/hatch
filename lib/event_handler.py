from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads.runs import RunStep, FunctionToolCall
from openai.types.beta.threads.message import Message
from rich.console import Console
import json
import os
from pprint import pprint

from .utilities import build_assistant_map, get_assistant_instance, print_message
from .session import Session
from rich.text import Text

assistant_map = build_assistant_map()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
console = Console()


class EventHandler(AssistantEventHandler):
    def __init__(self):
        """Initialize the EventHandler."""
        super().__init__()
        self.completion_tokens = 0
        self.prompt_tokens = 0
        self.text = Text()
        self.session = Session()
        self.panel = None

    @override
    def on_event(self, event):
        """Handle various events."""
        try:
            if event.event == "thread.run.requires_action":
                run_id = event.data.id
                self.handle_requires_action(event.data, run_id)

            elif event.event == "thread.run.failed":
                self.handle_run_failed(event.data)
        except Exception as e:
            self.on_exception(e)

    def handle_run_failed(self, data):
        """Handle run failure event."""
        print(f"Run failed: {data.last_error.code}\n{data.last_error.message}")
        os._exit(1)

    def on_run_step_done(self, run_step: RunStep) -> None:
        """Callback fired when a run step is completed."""
        try:
            if run_step.step_details.type == "tool_calls":
                self.handle_tool_calls(run_step)
        except Exception as e:
            self.on_exception(e)

    def handle_tool_calls(self, run_step: RunStep):
        """Handle tool calls in a run step."""
        assistant_id = run_step.assistant_id
        assistant = get_assistant_instance(assistant_id, assistant_map).__class__.__name__

        for tool_call in run_step.step_details.tool_calls:
            if isinstance(tool_call, FunctionToolCall) and tool_call.type == "function":
                function_name = tool_call.function.name
                function_arguments = tool_call.function.arguments

                function_arguments_dict = json.loads(function_arguments)
                formatted_args = "\n".join([f"{k}: {v}" for k, v in function_arguments_dict.items()])

                title = f"{assistant} -> {function_name}()"
                print_message("function_call", formatted_args, 0, title)

    def on_exception(self, exception: Exception) -> None:
        """Fired whenever an exception happens during streaming."""
        print("Exception:")
        pprint(exception)

    def on_timeout(self) -> None:
        """Fires if the request times out."""
        print("Timeout: Request timed out")

    def on_message_created(self, message: Message) -> None:
        """Callback fired when a message is created."""

    def on_message_done(self, message: Message) -> None:
        """Callback fired when a message is completed."""

        assistant_id = message.assistant_id
        assistant = get_assistant_instance(assistant_id, assistant_map).__class__.__name__
        ai_message = message.content[0].text.value

        print_message("assistant", ai_message, 0, assistant)

        self.session.store_message(message.thread_id, message)

    def handle_requires_action(self, data, run_id):
        """Handle required actions."""
        assistant_id = data.assistant_id
        assistant = get_assistant_instance(assistant_id, assistant_map)
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            tool_outputs.append(self._handle_tool_call(assistant, tool))

        self._submit_tool_outputs(tool_outputs, run_id, assistant.__class__.__name__)

    def _handle_tool_call(self, assistant, tool):
        """Handle individual tool calls."""
        function_name = tool.function.name
        function_args = json.loads(tool.function.arguments)
        method_to_call = getattr(assistant, function_name)
        tool_output = method_to_call(params=function_args)

        if not isinstance(tool_output, str):
            tool_output = json.dumps(tool_output)

        return {"tool_call_id": tool.id, "output": tool_output}

    def _submit_tool_outputs(self, tool_outputs, run_id, assistant_classname):
        """Submit the tool outputs."""
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(),
        ) as stream:
            for text in stream.text_deltas:
                """Noop to keep the stream open"""
