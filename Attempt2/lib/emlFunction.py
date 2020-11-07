from lib.error import Error
from lib.emlCallable import EmlCallable
from lib.environment import Environment

class EmlFunction(EmlCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        self.environment = Environment(interpreter.globals)
        for i in range(0, len(self.declaration.params)):
            self.environment.define(self.declaration.params[i].lexeme, arguments[i])
        interpreter.execute_block(self.declaration.body, self.environment)

    def arity(self):
        return len(self.declaration.params)

    def to_string(self):
        return f"<fun {self.declaration.name.lexeme} >"