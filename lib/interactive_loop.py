from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from lib.utilities import human_message, usage_message


class InteractiveLoop:
    def __init__(self, initial_message, agent):
        self.initial_message = initial_message
        self.session = PromptSession(history=InMemoryHistory())
        self.agent = agent
        self.thread = None

    def start_loop(self):
        """
        Starts the interactive loop that processes user input using the provided agent.
        The loop continues until the user types 'exit' or an interrupt signal is received.
        """
        self.process_initial_message(self.initial_message)
        while True:
            try:
                message = self.session.prompt("\nHuman --> ")
                if message.strip().lower() == "exit":
                    usage_message()
                    break
                self.process_message(message)
            except KeyboardInterrupt:
                self.handle_keyboard_interrupt()
                break
            except EOFError:
                self.handle_eof_error()
                break
            except Exception as e:
                self.handle_general_exception(e)
                break

    def process_initial_message(self, message):
        human_message(message)
        response = self.agent.message(message)
        self.thread = response.thread

    def process_message(self, message):
        print("")
        human_message(message)
        self.agent.message(message, thread=self.thread)

    def handle_keyboard_interrupt(self):
        """Handle Ctrl+C gracefully"""
        usage_message()

    def handle_eof_error(self):
        """Handle Ctrl+D gracefully"""
        usage_message()

    def handle_general_exception(self, e):
        print(f"\nError: {e}")
        usage_message()
