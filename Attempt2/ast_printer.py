from lib.error import Error
from lib.expr import Expr

class Ast_Printer():
    def print_ast(self, expr):
        return expr.accept(this)