from abc import ABC, abstractmethod

from db.mongo.connect import get_collections


class BotSettings(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class UpdateBotConstActivity(BotSettings):
    def __init__(self, activity: bool):
        self.activity = activity

    def run(self) -> None:
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            collections.insert_one({"_id": 0, "activity": self.activity, "distribute_chat_ids": [], "lock": False,
                                    "changes_users_ids": []})
        else:
            collections.update_one({"_id": 0}, {"$set": {"activity": self.activity}})


class GetBotConstActivity(BotSettings):

    def run(self) -> bool:
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            collections.insert_one({"_id": 0, "activity": True, "distribute_chat_ids": [], "lock": False,
                                    "changes_users_ids": []})
            return True
        return res["activity"]


class UpdateBotChatsDistributes(BotSettings):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def run(self):
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            collections.insert_one({"_id": 0, "activity": True, "distribute_chat_ids": [self.chat_id], "lock": False,
                                    "changes_users_ids": []})
        else:
            collections.update_one(
                {"_id": 0},  # Условие поиска записи (например, _id: 0)
                {"$addToSet": {"distribute_chat_ids": self.chat_id}}  # Добавление chat_id в массив, если его нет
            )


class RemoveBotChatsDistributes(BotSettings):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def run(self):
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            print("Запись не найдена")
        else:
            collections.update_one(
                {"_id": 0},
                {"$pull": {"distribute_chat_ids": self.chat_id}}
            )
            print(f"chat_id {self.chat_id} был удален из distribute_chat_ids")


class GetBotChatsDistributes(BotSettings):

    def run(self) -> list[int]:
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            return []
        return res.get("distribute_chat_ids", [])


class UpdateBotLock(BotSettings):
    def __init__(self, status: bool):
        self.status = status

    def run(self) -> None:
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            collections.insert_one({"_id": 0, "activity": True, "distribute_chat_ids": [], "lock": self.status,
                                    "changes_users_ids": []})
        else:
            collections.update_one({"_id": 0}, {"$set": {"lock": self.status}})


class GetBotLock(BotSettings):

    def run(self) -> bool:
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            collections.insert_one({"_id": 0, "activity": True, "distribute_chat_ids": [], "lock": False,
                                    "changes_users_ids": []})
            return False
        return res.get("lock")


class ChangesUsers(BotSettings):

    def run(self):
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            return []
        return res.get("changes_users_ids", [])


class AddChangesUsers(BotSettings):

    def __init__(self, user_id: int):
        self.user_id = user_id

    def run(self):
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            collections.insert_one({"_id": 0, "activity": True, "distribute_chat_ids": [], "lock": False,
                                    "changes_users_ids": [self.user_id]})
        else:
            collections.update_one(
                {"_id": 0},
                {"$addToSet": {"changes_users_ids": self.user_id}}
            )


class RemoveChangesUsers(BotSettings):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def run(self):
        collections = get_collections()
        res = collections.find_one({"_id": 0})
        if res is None:
            print("Запись не найдена")
        else:
            collections.update_one(
                {"_id": 0},
                {"$pull": {"changes_users_ids": self.user_id}}
            )
            print(f"user_id {self.user_id} был удален из distribute_chat_ids")


def update_bot_settings(bot_settings: BotSettings):
    return bot_settings.run()
