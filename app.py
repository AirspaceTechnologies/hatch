from assistants.hello_world_agent import HelloWorldAgent
from lib.utilities import human_message, usage_message

# Define the message to send to the clock agent
message = "How long since the last time I rebooted?"

# Print the message being sent to the clock agent
human_message(message)

# Create an instance of the ClockAgent
clock_agent = HelloWorldAgent()

# Send the message to the clock agent and get the response
response = clock_agent.message(message)

# Print the usage information, including threads, tokens, and cost
usage_message()
