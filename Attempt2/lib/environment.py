from lib.token import Token
from lib.error import Error

class Environment():
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        if(not(name in self.values)):
            self.values[name] = value
        else:
            Error.throw_generic(self, f"Variable '{name}' already defined")

    def get(self, name):
        if(name in self.values):
            return self.values[name]
        if(not(self.enclosing == None)):
            return self.enclosing.get(name)
        Error.throw_generic(self, f"Undefined Variabe: {name}.")

    def assign(self, name, value):
        if(name in self.values):
            self.values[name] = value
            return None
        if(not(self.enclosing == None)):
            self.enclosing.assign(name, value)
            return None
        Error.throw_generic(self, f"Variable '{name}' not defined")