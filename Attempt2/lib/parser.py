from lib.token import Token
from lib.token_types import TokenType
from lib.error import Error

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens