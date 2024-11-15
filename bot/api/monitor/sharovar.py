from abc import ABC, abstractmethod

from bot.api.ai.ai import ChatGPT, generate
from bot.api.monitor.reshoot import reshoot

prompt_sharovarshina = lambda text: f"""
                                --START_TEXT--{text}--END_TEXT--
                                Есть ли в этом тексте много непрофисионализма и не подготовленности человека к чему то.
                                Если ответ являестся Да то поставь в самый конец ответа такой символ '!' если нет то такой символ '#'
                                """


def sharovarshina(text: str) -> tuple[bool, str]:
    response = generate(ChatGPT(prompt=prompt_sharovarshina(text)))
    print(response)
    return response[-1] == "!", response


def city_bourgeois():
    pass


class RulesOfENR(ABC):

    def __init__(self, text: str):
        self.text = text

    def check(self) -> tuple[bool, str, int]:
        response = generate(ChatGPT(prompt=self._question()))
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
        Есть ли в этом тексте крайне много признаков не подготовленности и растеряности человека к какому то делу.
        Если ответ являестся Да то поставь в самый конец ответа такой символ '!' если нет то такой символ '#'
        """

    def cost_fine(self) -> int:
        return 3

    def name(self):
        return "Это же шароварщина"


class FreeWordsOfENR(RulesOfENR):
    def _question(self) -> str:
        return f"""--START_TEXT--{self.text}--END_TEXT--
        Есть ли в тексте признак серъезной диктатуры, неуважения или оскорбления человечиского мнения
        Если ответ являестся Да то поставь в самый конец ответа такой символ '!' если нет то такой символ '#'
        """

    def cost_fine(self) -> int:
        return 3

    def name(self):
        return "Никакой свободы слова"


class ReshootsOfENR(RulesOfENR):

    def __init__(self, text: str, two_steps: bool = False):
        super().__init__(text)
        self.two_steps = two_steps

    def check(self) -> tuple[bool, str, int]:
        return reshoot(self.text, self.two_steps), self.name(), self.cost_fine()

    def cost_fine(self) -> int:
        return 5

    def _question(self) -> str:
        return self.text

    def name(self):
        return "Обнаружены намеки на пересъемки"
