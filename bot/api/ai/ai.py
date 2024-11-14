import abc
from abc import ABC

from g4f.client import Client

from bot.api.ai.models import GPTModels

client = Client()


class AI(ABC):
    @abc.abstractmethod
    def generate(self):
        raise NotImplementedError


class ChatGPT(AI):
    def __init__(self, prompt, model: GPTModels = GPTModels.GPT4O_MINI):
        self.prompt = prompt
        self.model = model

    def generate(self):
        print("API_KEY: ", client.api_key)
        response = client.chat.completions.create(
            model=self.model.value,
            messages=[{
                "role": "user",
                "content": self.prompt,
            }]
        )
        return response.choices[0].message.content


def generate(ai: AI):
    return ai.generate()
