import re

from aiogram.types import Message

from bot.api.ai.ai import ChatGPT, generate
from bot.api.helper.recognize import recognize_type


def extract_text_from_angle_brackets(text: str) -> str:
    match = re.search(r'<(.*?)>', text)
    if match:
        return match.group(1)
    return "No"


def pattern_reshoot(text: str) -> bool:
    if re.search(
            r"\bп+[еиыі]+р+[еиыі]+([сз]+)н+?[еиыі]+м\w*|\bп+[еиыі]+р+[еиыі]+([сз]+)[йъь]?[еиыіёо]+м\w*|\bп+[еиыі]+р+[еиыі]+([сз]+)+н+я\w*",
            text,
            re.IGNORECASE):
        return True
    return False


def two_step_reshoot(text: str) -> bool:
    response = generate(ChatGPT(
        f"""|{text}| Ответь <Да> или <Нет> на вопрос об тексте.
             В этом тексте что то идется про пересъемки?. Ответ да или нет внутри <>"""))
    print(response)
    text = extract_text_from_angle_brackets(response)
    return text.lower() in ["да", "yes", "true", "так"]


def reshoot_text(text: str, two_step: bool = True) -> bool:
    valid = pattern_reshoot(text)
    if valid:
        return valid
    if two_step:
        return two_step_reshoot(text)
    return False


async def reshoot(message: Message):
    recognize_typ = recognize_type.get(message.content_type)
    text_reshoot = message.text
    if recognize_typ:
        voice_recognize = recognize_typ(message)
        text = await voice_recognize.recognize()
        print(text)
        text_reshoot = text
    return reshoot_text(text_reshoot)


