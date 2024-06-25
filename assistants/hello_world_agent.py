from lib.assistant_base import AssistantBase
import subprocess
import json


class HelloWorldAgent(AssistantBase):
    def __init__(self):
        super().__init__()

    def whoami(self, params):
        process = subprocess.Popen("whoami", stdout=subprocess.PIPE, shell=True)
        stdout, _ = process.communicate()

        return json.dumps({"result": stdout.decode().strip()})

    def uptime(self, params):
        process = subprocess.Popen("uptime", stdout=subprocess.PIPE, shell=True)
        stdout, _ = process.communicate()

        return json.dumps({"result": stdout.decode().strip()})
