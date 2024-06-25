import os
import re
import json
from openai import OpenAI
from .event_handler import EventHandler
from .utilities import system_message
from .session import Session


class AssistantResponse:
    def __init__(self, message, thread):
        self.message = message
        self.thread = thread


class AssistantBase:
    def __init__(self):
        """Initialize AssistantBase with API key and configuration."""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.config = self.load_config()
        self.assistant_id = self.config.get("id", "")
        self.session = Session()  # Initialize the session

    def load_config(self):
        """Load the configuration for the assistant."""
        class_name = self.__class__.__name__
        config_filename = f"{self.camel_to_snake(class_name)}.json"
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", config_filename)

        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                return json.load(config_file)
        else:
            return {}

    @staticmethod
    def camel_to_snake(name):
        """Convert CamelCase to snake_case."""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
        return snake_case

    def message(self, user_message, thread=None, tool_choice="auto", continue_interaction=False):
        """Send a message to the assistant and get a response."""
        run_message = "Starting run with existing thread"
        if thread is None:
            thread = self.client.beta.threads.create()
            run_message = "Starting run with new thread"
            self.session.add_thread_id(thread.id)

        system_message(f"thread_id: {thread.id}\nassistant_id: {self.assistant_id}", run_message)

        self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)

        with self.client.beta.threads.runs.stream(
            thread_id=thread.id,
            tool_choice=tool_choice,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

        # Retrieve the last message from the session
        last_message = self.session.get_last_message(thread.id, default=user_message)
        return AssistantResponse(last_message, thread)

    def save_state(self, key, value):
        """Save a state value in the session."""
        self.session.set(key, value)

    def get_state(self, key, default=None):
        """Get a state value from the session."""
        return self.session.get(key, default)
