# hatch : a framework for ai agents

<p align="center">
  <img src="lib/docs/hatch.jpg" width=250>
</p>

## Description
The purpose of this project is to facilitate interaction with different AI agents. These agents can perform various tasks, automate workflows, and aid in the development process.

## Full control
There are zero built in system prompts.

## Installation
Step-by-step instructions on how to install and set up the project.
1. Clone the repository:
```sh
$ git clone https://github.com/michaelirey/hatch.git
```
2. Navigate to the project directory:
```sh
$ cd hatch
```
3. Install the required packages:
```sh
$ pip install -r requirements.txt
```
4. Make sure openai api key is set
```sh
$ export OPENAI_API_KEY=...
```

## Usage
Instructions and examples on how to use the project.
```sh
$ python app.py
```

## AI Function Calling
The project allows you to interact with various AI agents. For example, in `app.py`, a `HelloWorldAgent` is used to look up domain information:
See: https://platform.openai.com/docs/assistants/tools/function-calling

## Thread Summary
The `thread_summary.py` script provides a summary of a specific thread. To use it, run the following command:

```sh
$ python thread_summary.py <thread_id>
```

This script uses the `ThreadAnalyzer` and `ReportPrinter` classes to analyze and print the thread summary.

## Importing Assistants
You can import new assistants using the `import_assistant.py` script. This script retrieves the assistant configuration from OpenAI and generates the corresponding Python class.

To import an assistant, run:
```sh
$ python import_assistant.py <assistant_id>
```

This will save the assistant configuration and generate a new Python class in the `assistants` directory.

## Tests
Instructions on how to run tests.
```sh
$ pytest
```

## License
Information about the project's license.
MIT License
