from openai import OpenAI
import os


class QuickChat:
    @staticmethod
    def send(message):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{message}",
                }
            ],
            model="gpt-3.5-turbo",
        )

        return chat_completion.choices[0].message.content
