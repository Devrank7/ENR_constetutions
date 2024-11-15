from bot.api.fine import Fine
from bot.api.monitor.sharovar import Sharovarshina, FreeWordsOfENR, ReshootsOfENR
from bot.exception.exc import ENRConstitutionsException
from db.mongo.bot_settings import update_bot_settings, GetBotLock


def build_issue(reason: str):
    return "Нарушенние конституции ЕНР. {}".format(reason)


issues = [
    ReshootsOfENR,
    Sharovarshina,
    FreeWordsOfENR,
]


async def issue_fine_for_user_if_has(fine: Fine, text: str):
    lock = update_bot_settings(GetBotLock())
    try:
        for issue in issues:
            is_fine, reason, cost = issue(text).check()
            if is_fine:
                raise ENRConstitutionsException(build_issue(reason), cost)
    except ENRConstitutionsException as e:
        await fine.issue(e.message, e.cost, not lock)
