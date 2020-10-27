from lib.token import Token
from lib.token_types import TokenType
from lib.expr import Expr, Binary, Literal, Grouping, Unary
from lib.error import Error

# This parser will use recursice descent to generate the abasract syntax tree.
class Parser():
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def parse(self):
        try:
            return self.expression()
        except:
            Error.throw_generic("there was an error")
            return None

    # expression     → equality
    def expression(self):
        return self.equality()

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
        # return ParseError()
        return None

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if(self.previous().token_type == TokenType.SEMICOLON):
                return
            if(self.peek().token_type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]):
                return
            self.advance()
