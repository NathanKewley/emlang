from lib.emlCallable import EmlCallable
from datetime import datetime

# clock() function
class EmlClock(EmlCallable):
    def arity(self):
        return 0
    def call(self, interpreter, arguments):
        return datetime.now()
    def toString(self):
        return "[Native emlang Function]"

class EmlListLength(EmlCallable):
    def arity(self):
        return 1
    def call(self, interpreter, arguments):
        return len(arguments[0])
    def toString(self):
        return "[Native emlang Function]"

class EmlListItem(EmlCallable):
    def arity(self):
        return 2
    def call(self, interpreter, arguments):
        try:
            return float(arguments[0][int(arguments[1])])
        except:
            return arguments[0][int(arguments[1])]
    def toString(self):
        return "[Native emlang Function]"

class EmlLoadFileToList(EmlCallable):
    def arity(self):
        return 1
    def call(self, interpreter, arguments):
        input = []
        with open(arguments[0]) as f:
            input = f.read().splitlines()
        return input        
    def toString(self):
        return "[Native emlang Function]"
