from lib.token import Token
import sys

class Error():
    def __init__(self):
        pass

    def throw_generic(self, message):
        sys.tracebacklimit = 0
        raise Exception(message)

    def throw_token_error(self, token, message):
        raise Exception(f"[line {token.line}] at [{token.lexeme}] ERROR: {message}")

    def throw(self, line, where, message):
        raise Exception(f"[Line {line}] ERROR {where}: {message}")

    def throw_runtime_error(self, operator, message):
        sys.tracebacklimit = 0
        raise Exception(f"[RUNTUME ERROR] [Line {operator.line}] {operator.token_type}, {message}")
