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
        Error.throw_generic(self, f"Undefined Variabe: {name}.")

    def assign(self, name, value):
        if(name in self.values):
            self.values[name] = value
            return None
        Error.throw_generic(self, f"Variable '{name}' not defined")