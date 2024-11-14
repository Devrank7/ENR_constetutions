class NotReplyException(Exception):
    def __init__(self, message: str = "Not reply", *args):
        super().__init__(*args)
        self.message = message
