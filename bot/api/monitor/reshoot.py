import re

from bot.api.ai.ai import ChatGPT, generate
from bot.api.helper.text import is_symbol


def pattern_reshoot(text: str) -> bool:
    if re.search(
            r"\bп+[еиыі]+р+[еиыі]+([сз]+)н+?[еиыі]+м\w*|\bп+[еиыі]+р+[еиыі]+([сз]+)[їйъь]+?[еиыіёо]+?м+\w*|\bп+[еиыі]+р+[еиыі]+([сз]+)+н+[яії]\w*",
            text,
            re.IGNORECASE):
        return True
    return False


async def two_step_reshoot(text: str, question: str) -> bool:
    response = await generate(ChatGPT(
        f"""|{text}| Ответь <Да> или <Нет> на вопрос об тексте.
             {question}.
             Слова эти могут быть с ошибками. Если ответ являестся Да то поставь в самый конец ответа такой символ '!' если нет то такой символ '#'"""))
    print(response)
    return is_symbol(response)


async def reshoot(text: str, two_step: bool = True, question: str = "") -> bool:
    valid = pattern_reshoot(text)
    if valid:
        return valid
    if two_step:
        return await two_step_reshoot(text, question)
    return False
