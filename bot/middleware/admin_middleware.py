from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

from bot.api.permision import my_permission_has


class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print('HERE')
        has = await my_permission_has(event, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
        if has:
            return await handler(event, data)
        return await event.answer(
            "Сделай меня админом 👽 если хочешь чтобы я мог разбанивать или баннить людей на некоторое время."
            "И самое главное!!! Это банниить людей за нарушение конституции.😈 ")
