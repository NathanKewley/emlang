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