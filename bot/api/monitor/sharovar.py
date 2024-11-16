from abc import ABC, abstractmethod

from bot.api.ai.ai import ChatGPT, generate
from bot.api.monitor.reshoot import reshoot


class RulesOfENR(ABC):

    def __init__(self, text: str):
        self.text = text

    async def check(self) -> tuple[bool, str, int]:
        response = await generate(ChatGPT(prompt=self._question()))
        print(response)
        return response[-1] == '!', f"{self.name()}.{response}", self.cost_fine()

    @abstractmethod
    def cost_fine(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _question(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def name(self):
        raise NotImplementedError


class Sharovarshina(RulesOfENR):
    def _question(self) -> str:
        return f"""--START_TEXT--{self.text}--END_TEXT--
        Говорится ли в тексте ясно и открыто, что кто-то что-то забыл или забыл к чему-то подготовиться?
        Если ответ являестся Да то последний символ твоего ответа должен быть '!' если нет то такой символ '#'
        """

    def cost_fine(self) -> int:
        return 2

    def name(self):
        return "Статья 2. Явный признак шароварщины👁️ это же непрофесионализм и неподготовленость."


class FreeWordsOfENR(RulesOfENR):
    def _question(self) -> str:
        return f"""--START_TEXT--{self.text}--END_TEXT--
        Содержит ли текст жестокое оскорбление человеческого мнения?
        Если ответ являестся Да то самый последний символ твоего ответа должен быть '!' если нет то такой символ '#'
        """

    def cost_fine(self) -> int:
        return 3

    def name(self):
        return "Статья 3. Нарушение свободы слова!!! Неуважение человечиского мнения😡"


class ReshootsOfENR(RulesOfENR):

    def __init__(self, text: str, two_steps: bool = False):
        super().__init__(text)
        self.two_steps = two_steps

    async def check(self) -> tuple[bool, str, int]:
        return await reshoot(self.text, self.two_steps, self._question()), self.name(), self.cost_fine()

    def cost_fine(self) -> int:
        return 5

    def _question(self) -> str:
        return "В этом тексте есть словоа 'переснять, пересъомка' и подобные слова об съемках с префиксом 'пере'"

    def name(self):
        return "СТАТЬЯ 1. Явно видно намек на ПЕРЕСЪОМКИ📸."
