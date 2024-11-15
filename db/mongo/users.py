from abc import abstractmethod, ABC

from db.mongo.connect import get_collections


class UsersMonitor(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class UserUpdateStatus(UsersMonitor):

    def __init__(self, user_id: int):
        self.user_id = user_id

    def run(self):
        collections = get_collections("users")
        collections.update_one(
            {"_id": 0},
            {"$inc": {f"users.{self.user_id}": 1}},
            upsert=True
        )


class GetUserActivity(UsersMonitor):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def run(self) -> int:
        collections = get_collections("users")
        res = collections.find_one({"_id": 0})  # Поиск документа с _id: 0
        if res and "users" in res:
            # Получаем значение активности пользователя по user_id или возвращаем 0, если его нет
            return res["users"].get(self.user_id, 0)
        return 0


class ResetAllUserActivity(UsersMonitor):
    def run(self):
        collections = get_collections("users")
        res = collections.find_one({"_id": 0})
        if res and "users" in res:
            collections.update_one(
                {"_id": 0},
                {"$set": {"users": {key: 0 for key in res["users"]}}}
            )
        else:
            collections.update_one(
                {"_id": 0},
                {"$set": {"users": {}}},
                upsert=True
            )


def update_user_activity(user_monitor: UsersMonitor):
    return user_monitor.run()
