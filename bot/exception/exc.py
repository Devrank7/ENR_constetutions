class NotReplyException(Exception):
    def __init__(self, message: str = "Not reply", *args):
        super().__init__(*args)
        self.message = message


class ENRConstitutionsException(Exception):
    def __init__(self, message: str, cost: int, *args):
        super().__init__(*args)
        self.message = message
        self.cost = cost
