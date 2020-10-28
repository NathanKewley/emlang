from lib.token import Token
from lib.error import Error

class Environment():
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if(name in self.values):
            return self.values[name]
        Error.throw_generic(f"Undefined Variabe: {name}.")