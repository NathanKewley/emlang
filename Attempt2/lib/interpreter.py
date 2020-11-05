from lib.token import Token
from lib.token_types import TokenType
from lib.expr import Expr, Binary, Literal, Grouping, Unary, Variable, Assign, Logical
from lib.stmt import Stmt, Expression, Print, Var, Yeet, Block, If
from lib.error import Error
from lib.environment import Environment
import numbers

# The interpreter takes an expression and evaluates it
class Interpreter(Expr, Stmt):
    def __init__(self):
        self.environment = Environment()

    def interprert(self, statements):
        # try:
        for statement in statements:
            # print(statement.expression)
            # print(statement)
            self.execute(statement)
        # except:
        #     Error.throw_generic(self, "Unknown runtime error... shit")

    def execute(self, statement):
        statement.accept(self)

    # evaluate blocks { }
    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # visit if statement
    def visit_if_stmt(self, stmt):
        if(self.is_truthful(self.evaluate(stmt.condition))):
            self.execute(stmt.then_branch)
        elif(not(stmt.else_branch == None)):
            self.execute(stmt.else_branch)
        return None

    # visit block statement
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    # evaluate expression statement
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    # evaluate print statement
    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(value)
        return None

    # evaluate var statement
    def visit_var_stmt(self, stmt):
        value = None
        if(not(stmt.expression) == None):
            value = self.evaluate(stmt.expression)
        self.environment.define(stmt.name, value)
        return None

    # variable assignment statement
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name.lexeme, value)
        return value

    # evaluate yeet statement
    def visit_yeet_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(value.upper())
        return None

    # evaluate logic expression
    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if(expr.operator.token_type == TokenType.OR):
            if(self.is_truthful(left)): 
                return left
        else:
            if(not(self.is_truthful(left))):
                return left
        return self.evaluate(expr.right)

    # evaluate variable expression
    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name.lexeme)

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
            if((isinstance(left, numbers.Real)) and (isinstance(right, numbers.Real))):
                return(left + right)
            if(isinstance(left, str)) and (isinstance(right, str)):
                return(left + right)
            Error.throw_runtime_error(self, expr.operator, "operands must be either 2 number or 2 strings")
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
        if(isinstance(value, bool)):
            return value
        return True

    def is_equal(self, left, right):
        # if types are different they are false
        if(not(type(left) == type(right))):
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