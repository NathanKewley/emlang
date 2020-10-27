from lib.token import Token
from lib.token_types import TokenType
from lib.expr import Expr, Binary, Literal, Grouping, Unary
from lib.error import Error
import numbers

# The interpreter takes an expression and evaluates it
class Interpreter(Expr):
    def __init__(self):
        pass

    def interprert(self, expression):
        try:
            value = self.evaluate(expression)
            print(value)
            # print(self.stringify(value))
        except:
            Error.throw_generic("Unknown runtime error... shit")

    # evaluate Literal expressions
    def visit_literal_expr(self, expr):
        return(expr.value)

    # evaluate Grouping expressions
    def visit_grouping_expr(self, expr):
        return(self.evaluate(expr.expression))

    # evaluate Unary expressions
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if(expr.operator.token_type == TokenType.MINUS ):
            return(-(right))
        if(expr.operator.token_type == TokenType.BANG):
            return(not (self.is_truthful(right)))
        return(None)

    # evaluate Binary expressions
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if(expr.operator.token_type == TokenType.MINUS):
            self.check_number_operand(expr.operator, right)
            return(left - right)
        if(expr.operator.token_type == TokenType.SLASH):
            self.check_number_operands(expr.operator, left, right)
            return(left / right)
        if(expr.operator.token_type == TokenType.STAR):
            self.check_number_operands(expr.operator, left, right)
            return(left * right)
        if(expr.operator.token_type == TokenType.PLUS):
            # we need the distinciton between string and number values here as we dont want to add nunbers and strings
            print(f"PLUS FOUND: Left type: {left}  | right type: {right}")
            if((isinstance(left, numbers.Real)) and (isinstance(right, numbers.Real))):
                return(left + right)
            if(left.type() == str) and (right.type() == str):
                return(left + right)
            Error.throw_runtime_error(expr.operator, "operands must be either 2 number or 2 strings")
        if(expr.operator.token_type == TokenType.GREATER):
            self.check_number_operands(expr.operator, left, right)
            return(left > right)
        if(expr.operator.token_type == TokenType.GREATER_EQUAL):
            self.check_number_operands(expr.operator, left, right)
            return(left >= right)
        if(expr.operator.token_type == TokenType.LESS):
            self.check_number_operands(expr.operator, left, right)
            return(left < right)
        if(expr.operator.token_type == TokenType.LESS_EQUAL):
            self.check_number_operands(expr.operator, left, right)
            return(left <= right)                                    
        if(expr.operator.token_type == TokenType.BANG_EQUAL):
            return(not(self.is_equal(left, right)))
        if(expr.operator.token_type == TokenType.EQUAL_EQUAL):
            return(self.is_equal(left, right))
        return None

    def evaluate(self, expr):
        return(expr.accept(self))

    # determines if an expression is true for a boolean operation. For this instance everything is true except for `None` and `False`
    def is_truthful(self, value):
        if(value == None):
            return False
        if(value.type() is bool):
            return value
        return True

    def is_equal(self, left, right):
        # if types are different they are false
        if(not(left.type() == right.type())):
            return False
        return(left == right)

    def check_number_operand(self, operator, operand):
        if(isinstance(operand, numbers.Real)):
            return True
        Error.throw_runtime_error(operator, "operand must be a number")
        return None

    def check_number_operands(self, operator, left, right):
        if(not(isinstance(left, numbers.Real))):
            Error.throw_runtime_error(operator, "left operand must be a number")
        # if(not((right.type() is int) or (right.type() is float))):
        if(not(isinstance(right, numbers.Real))):
            Error.throw_runtime_error(operator, "right operand must be a number")
        return True

    # POSSIBLY NEED TO REVISIT AND IMPLEMENT
    # private String stringify(Object object) { (https://craftinginterpreters.com/evaluating-expressions.html#hooking-up-the-interpreter)
    #     if (object == null) return "nil";

    #     if (object instanceof Double) {
    #     String text = object.toString();
    #     if (text.endsWith(".0")) {
    #         text = text.substring(0, text.length() - 2);
    #     }
    #     return text;
    #     }

    #     return object.toString();
    # }