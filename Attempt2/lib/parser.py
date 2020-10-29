from lib.token import Token
from lib.token_types import TokenType
from lib.expr import Expr, Binary, Literal, Grouping, Unary, Variable, Assign
from lib.stmt import Stmt, Expression, Print, Var, Yeet
from lib.error import Error

# This parser will use recursice descent to generate the abasract syntax tree.
class Parser():
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def parse(self):
        statements = []
        while(not (self.is_at_end())):
            print(f"adding statement {self.peek().token_type}")
            statements.append(self.declaration())
        return(statements)

    # declaration    → varDecl | statement ;
    def declaration(self):
        try:
            if(self.match([TokenType.VAR])):
                return self.var_declaration()  
            return self.statement()
        except:
            self.synchronize()
            return None

    # statement      → exprStmt | printStmt ;
    def statement(self):
        if(self.match([TokenType.PRINT])):
            return self.print_statement()
        if(self.match([TokenType.YEET])):
            return self.yeet_statement()               
        return self.expression_statement()

    # varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected Variable Name")
        expression = None
        if(self.match([TokenType.EQUAL])):
            expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' to terminate statement.")
        return Var(name.lexeme, expression)
        
    # exprStmt       → expression ";" ;
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' to terminate statement.")
        return Expression(expr)

    # printStmt      → "print" expression ";" ;
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' to terminate statement.")
        return Print(value)

    # yeetStmt       → "YEET" expression ";" ;     
    def yeet_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' to terminate statement.")
        return Yeet(value)

    # eexpression     → assignment ;
    def expression(self):
        return self.assignment()

    # assignment     → IDENTIFIER "=" assignment | equality ;
    def assignment(self):
        expr = self.equality()
        if(self.match([TokenType.EQUAL])):
            equals = self.previous()
            value = self.assignment()
            if(isinstance(expr, Variable)):
                name = expr.name
                return Assign(name, value)            
            Error.throw_token_error(self.peek(), "Invalid assignment target for variable")
        return expr     

    # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self):
        expr = self.comparison()

        while(self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    def comparison(self):
        expr = self.term()

        while(self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    # term           → factor ( ( "-" | "+" ) factor )* ;
    def term(self):
        expr = self.factor()

        while(self.match([TokenType.MINUS, TokenType.PLUS])):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    # factor         → unary ( ( "/" | "*" ) unary )* ;
    def factor(self):
        expr = self.unary()

        while(self.match([TokenType.SLASH, TokenType.STAR])):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    # unary          → ( "!" | "-" ) unary | primary ;
    def unary(self):
        if(self.match([TokenType.BANG, TokenType.MINUS])):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    # primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
    def primary(self):
        if(self.match([TokenType.FALSE])):
            return Literal(False)
        if(self.match([TokenType.TRUE])):
            return Literal(True)
        if(self.match([TokenType.NIL])):
            return Literal(None)
        if(self.match([TokenType.STRING, TokenType.NUMBER])):
            return Literal(self.previous().literal)
        if(self.match([TokenType.LEFT_PAREN])):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Except ')' after expression.")
            return Grouping(expr)
        if(self.match([TokenType.IDENTIFIER])):
            return Variable(self.previous())
        Error.throw_token_error(self.peek(), "Expect Expression")

    def match(self, token_types):
        for token_type in token_types:
            if(self.check(token_type)):
                self.advance()
                return True
        return False

    def check(self, token_type):
        if (self.is_at_end()):
            return False
        return self.peek().token_type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current = self.current + 1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, token_type, error):
        if(self.check(token_type)):
            return self.advance()
        token = self.peek()
        Error.throw_token_error(token, error)
        return None

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if(self.previous().token_type == TokenType.SEMICOLON):
                return
            if(self.peek().token_type in [TokenType.CLASS, TokenType.FUNCTION, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN, TokenType.YEET]):
                return
            self.advance()
