from bot.api.ai.ai import ChatGPT, generate
from bot.api.helper.text import extract_text_from_angle_brackets


def sharovarshina(text: str):
    response = generate(ChatGPT(prompt=
                                f"""
                                --START_TEXT--{text}--END_TEXT--
                                Есть ли в этом тексте нотки непрофисионализма и не подготовленности.
                                Ответ предоставить внутри угловых скобок <>
                                """))
    text = extract_text_from_angle_brackets(response)
    return text.lower() in ["да", "yes", "true", "так", "да.", "yes.", "true.", "так."]
