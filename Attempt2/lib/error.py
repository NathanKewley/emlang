from lib.token import Token

class Error():
    def throw_generic(self, message):
        print(message)

    def throw_token_error(self, token, message):
        print(f"[line {token.line}] at [{token.lexeme}] ERROR: {message}")

    def throw(self, line, where, message):
        print(f"[Line {line}] ERROR {where}: {message}")
