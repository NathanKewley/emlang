from lib.error import Error
from lib.emlCallable import EmlCallable
from lib.environment import Environment
from lib.returnException import ReturnException

class EmlFunction(EmlCallable):
    def __init__(self, declaration, environment):
        self.declaration = declaration
        self.environment = environment

    def call(self, interpreter, arguments):
        self.environment = Environment(self.environment)
        for i in range(0, len(self.declaration.params)):
            self.environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, self.environment)
        except ReturnException as e:
            return e.value.value

    def arity(self):
        return len(self.declaration.params)

    def to_string(self):
        return f"<fun {self.declaration.name.lexeme} >"
