import abc
import asyncio
from abc import ABC
from concurrent.futures import ThreadPoolExecutor

from g4f.client import Client

from bot.api.ai.models import GPTModels, AIModels, FluxModels


class AI(ABC):
    @abc.abstractmethod
    async def generate(self):
        raise NotImplementedError


class ChatGPT(AI):

    def __init__(self, prompt, model: AIModels = GPTModels.GPT4O):
        self.prompt = prompt
        self.model = model

    def get_max_attempts(self):
        return 8

    def get_response_sync(self):
        client = Client()
        response = client.chat.completions.create(
            model=self.model.value,
            messages=[{
                "role": "user",
                "content": self.prompt,
            }]
        )
        return response.choices[0].message.content

    async def generate(self):
        print("Begin")
        attempt = 0
        loop = asyncio.get_running_loop()

        while attempt < 10:
            try:
                responses = await asyncio.wait_for(
                    loop.run_in_executor(ThreadPoolExecutor(), self.get_response_sync),
                    timeout=self.get_max_attempts()
                )
                print(responses)
                if responses == 'Request ended with status code 404':
                    raise Exception("404")
                return responses
            except asyncio.TimeoutError:
                print(f"Attempt {attempt + 1} timed out. Retrying...")
            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")

            attempt += 1

        raise TimeoutError("Failed to get a response within the allowed attempts.")


class FluxGPT(ChatGPT):

    def __init__(self, prompt, models: FluxModels = FluxModels.FLUX):
        super().__init__(prompt, models)

    def get_response_sync(self):
        client = Client()
        response = client.images.generate(
            model=self.model.value,
            prompt=self.prompt,
        )
        url = response.data[0].url
        print(url)
        return url

    def get_max_attempts(self):
        return 60


async def generate(ai: AI):
    return await ai.generate()
