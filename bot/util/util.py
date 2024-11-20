import json


def to_json(myjson) -> dict:
    if isinstance(myjson, dict):
        return myjson
    if isinstance(myjson, str):
        return json.loads(myjson)
