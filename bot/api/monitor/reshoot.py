import re

from bot.api.ai.ai import ChatGPT, generate
from bot.api.helper.text import extract_text_from_angle_brackets


def pattern_reshoot(text: str) -> bool:
    if re.search(
            r"\bп+[еиыі]+р+[еиыі]+([сз]+)н+?[еиыі]+м\w*|\bп+[еиыі]+р+[еиыі]+([сз]+)[їйъь]+?[еиыіёо]+?м+\w*|\bп+[еиыі]+р+[еиыі]+([сз]+)+н+[яії]\w*",
            text,
            re.IGNORECASE):
        return True
    return False


def two_step_reshoot(text: str) -> bool:
    response = generate(ChatGPT(
        f"""|{text}| Ответь <Да> или <Нет> на вопрос об тексте.
             В этом тексте есть словоа 'переснять, пересъомка' и подобные слова об съемках с префиксом 'пере'.
             Слова эти могут быть с ошибками. Если ответ являестся Да то поставь в самый конец ответа такой символ '!' если нет то такой символ '#'"""))
    print(response)
    text = response[-1]
    return text == '!'


def reshoot(text: str, two_step: bool = True) -> bool:
    valid = pattern_reshoot(text)
    if valid:
        return valid
    if two_step:
        return two_step_reshoot(text)
    return False


