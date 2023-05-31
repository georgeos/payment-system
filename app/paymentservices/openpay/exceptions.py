class OpenpayException(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Openpay [{self.message}]"
