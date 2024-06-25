import json
import os
import re
import importlib
from rich import print
from rich.panel import Panel
import threading

message_lock = threading.Lock()


def build_assistant_map(config_dir="config"):
    assistant_map = {}
    for file_name in os.listdir(config_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(config_dir, file_name), "r") as f:
                config = json.load(f)
                assistant_map[config["id"]] = config["name"]
    return assistant_map


def camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def get_assistant_instance(assistant_id, assistant_map):
    assistant_classname = assistant_map.get(assistant_id)
    if not assistant_classname:
        raise ValueError(f"Assistant ID {assistant_id} not found in the assistant map.")
    module_filename = camel_to_snake(assistant_classname)
    module_path = f"assistants.{module_filename}"
    module = importlib.import_module(module_path)
    assistant_class = getattr(module, assistant_classname)
    return assistant_class()


def human_message(message, agent="Human"):
    if message.strip() == "":
        return

    print(
        Panel.fit(
            message,
            title_align="left",
            subtitle_align="right",
            title=f"[bold]{agent}",
            style="bright_white on dark_blue",
        )
    )


def system_message(message, agent="System"):
    if message.strip() == "":
        return

    print(Panel.fit(message, title_align="left", subtitle_align="right", title=f"[bold]{agent}", style="grey70"))


def assistant_message(message, elapsed_time, title="Assistant"):
    if message.strip() == "":
        return
    print(
        Panel.fit(
            message,
            title_align="left",
            subtitle_align="right",
            title=f"[bold]{title}",
            style="orange3 on grey15",
        )
    )


def function_call_message(message, elapsed_time, title):
    if message.strip() == "":
        message = "no arguments provided"

    print(
        Panel.fit(
            f"[bright_white]{message}",
            title_align="left",
            subtitle_align="right",
            title=f"[bold]{title}",
            style="bright_magenta",
        )
    )


def print_message(message_func, message, elapsed_time, title="Assistant"):
    with message_lock:
        if message_func == "assistant":
            assistant_message(message, elapsed_time, title)
        elif message_func == "function_call":
            function_call_message(message, elapsed_time, title)


def usage_message():
    from lib.session import Session

    session = Session()
    cost = round(session.cost(), 5)
    tokens = session.tokens()
    threads = len(session.get_thread_ids())
    system_message(f"threads: {threads}\ntokens: {tokens}\ncost: ${cost}", "Usage")
