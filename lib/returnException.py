from lib.stmt import Return

class ReturnException(Exception):
    def __init__(self, value):
        self.value = Return("return", value)
        super().__init__(self.value)
