from assistants.hello_world_agent import HelloWorldAgent
from lib.interactive_loop import InteractiveLoop

if __name__ == "__main__":
    initial_message = "How long since the last time I rebooted?"
    agent = HelloWorldAgent()
    loop = InteractiveLoop(initial_message, agent)
    loop.start_loop()
