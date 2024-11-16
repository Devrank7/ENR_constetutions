import abc
import asyncio
from abc import ABC
from concurrent.futures import ThreadPoolExecutor

from g4f.client import Client

from bot.api.ai.models import GPTModels


class AI(ABC):
    @abc.abstractmethod
    async def generate(self):
        raise NotImplementedError


class ChatGPT(AI):
    MAX_ATTEMPTS = 10

    def __init__(self, prompt, model: GPTModels = GPTModels.GPT4O_MINI):
        self.prompt = prompt
        self.model = model

    async def generate(self):
        print("Begin")

        def get_response_sync():
            client = Client()
            response = client.chat.completions.create(
                model=self.model.value,
                messages=[{
                    "role": "user",
                    "content": self.prompt,
                }]
            )
            return response.choices[0].message.content

        max_attempts = self.MAX_ATTEMPTS
        attempt = 0
        loop = asyncio.get_running_loop()

        while attempt < max_attempts:
            try:
                responses = await asyncio.wait_for(
                    loop.run_in_executor(ThreadPoolExecutor(), get_response_sync),
                    timeout=8
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


async def generate(ai: AI):
    return await ai.generate()
