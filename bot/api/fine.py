from aiogram.types import Message

from bot.api.permision import AnswerBan
from bot.util.math import clamp
from db.mongo.users import update_user_activity, GetUserActivity, UserUpdateStatus


class Fine:
    def __init__(self, message: Message):
        self.message = message

    async def issue(self, reason: str, strength: int = 5, need_to_ban: bool = True):
        activity = update_user_activity(GetUserActivity(user_id=str(self.message.from_user.id)))
        time_mute = strength ** clamp(activity + 1, 1, 5)
        print(time_mute)
        if need_to_ban:
            answer_ban = AnswerBan(message=self.message, minutes=time_mute)
            await answer_ban.restrict()
            await self.message.reply(reason)
        else:
            await self.message.reply(
                f"К сожелению не смогу забаннить на {time_mute} минут 🥺 из того что меня так настроили /set_lock"
                f" но то что я могу сделать это вычитать мораль. {reason}")
        update_user_activity(UserUpdateStatus(self.message.from_user.id))
