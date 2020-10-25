from lib.error import Error
from lib.expr import Expr, Binary, Literal
from lib.token import Token
from lib.token_types import TokenType

class Ast_Printer(Expr):
    def print_ast(self, expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr):
        exprs = [expr.left, expr.right]
        return self.parenthesize(expr.operator.lexeme, exprs)

    def visitGroupingExpr(self, expr):
        exprs = [expr.expression]
        return self.parenthesize("group", exprs)

    def visitLiteralExpr(self, expr):
        if (expr == None): 
            return "Null"
        return expr.value

    def visitUnaryExpr(self, expr):
        exprs = [expr.right]
        return self.parenthesize(expr.operator.lexeme, exprs)

    def parenthesize(self, name, exprs):
        string_build = f"({name}"
        for expr in exprs:
            string_build = string_build + f" {expr.accept(self)}"
        string_build = string_build + ")"
        return string_build

# Will change this later to be some test cases, think this sort of thing will be a good base to go off
if __name__ == '__main__':
    # create a multi layered expression to test with
    minus = Token(TokenType.MINUS, "-", None, 1)
    literal_0 = Literal(123)
    literal_1 = Literal(22)
    expression_0 = Binary(literal_0, minus, literal_1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    expression_1 = Binary(expression_0, plus, literal_1)
    
    # print the expression
    expression_printer = Ast_Printer()
    print(expression_printer.print_ast(expression_1))