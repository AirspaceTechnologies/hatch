import sys
import json
import os
from openai import OpenAI
from lib.assistant_base import AssistantBase


def import_assistant(assistant_id):
    client = OpenAI()
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    assistant_name = my_assistant.name
    config_filename = f"{AssistantBase.camel_to_snake(assistant_name)}.json"
    config_path = os.path.join(os.path.dirname(__file__), "config", config_filename)
    with open(config_path, "w") as config_file:
        json.dump(my_assistant.to_dict(), config_file, indent=2)
    print(f"Assistant configuration saved to {config_path}")
    generate_assistant_class(assistant_name, my_assistant.to_dict())


def generate_assistant_class(assistant_name, assistant_config):
    class_name = assistant_name
    class_code = f"from lib.assistant_base import AssistantBase\n\n\nclass {class_name}(AssistantBase):\n    def __init__(self):\n        super().__init__()\n"

    for tool in assistant_config.get("tools", []):
        if tool["type"] == "function":
            function_name = tool["function"]["name"]
            params = tool["function"]["parameters"]["properties"].keys()
            params_str = ", ".join(params)
            class_code += f"\n    def {function_name}(self, params):\n"
            for param in params:
                class_code += f'        {param} = params.get("{param}")\n'

    class_filename = f"assistants/{AssistantBase.camel_to_snake(assistant_name)}.py"
    with open(class_filename, "w") as class_file:
        class_file.write(class_code)
    print(f"Assistant class saved to {class_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: import_assistant.py <assistant_id>")
        sys.exit(1)
    assistant_id = sys.argv[1]
    import_assistant(assistant_id)
