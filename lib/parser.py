from lib.token import Token
from lib.token_types import TokenType
from lib.expr import Expr, Binary, Literal, EMList, Grouping, Unary, Variable, Assign, Logical, Call
from lib.stmt import Stmt, Expression, Print, Var, Yeet, Block, If, While, Function, Return
from lib.error import Error

# This parser will use recursice descent to generate the abasract syntax tree.
class Parser():
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def parse(self):
        statements = []
        while(not (self.is_at_end())):
            # print(f"adding statement {self.peek().token_type}")
            decl = self.declaration()
            # print(decl)
            statements.append(decl)
        return(statements)

    # declaration    → varDecl | statement ;
    def declaration(self):
        # try:
        if(self.match([TokenType.VAR])):
            return self.var_declaration()  
        if(self.match([TokenType.FUN])):
            return self.function_declaration("Function")              
        return self.statement()
        # except:
        #     self.synchronize()
        #     return None

    # statement      → exprStmt | printStmt ;
    def statement(self):
        if(self.match([TokenType.PRINT])):
            return self.print_statement()
        if(self.match([TokenType.YEET])):
            return self.yeet_statement() 
        if(self.match([TokenType.LEFT_BRACE])):
            return Block(self.block())  
        if(self.match([TokenType.IF])):
            return self.if_statement()       
        if(self.match([TokenType.WHILE])):
            return self.while_statement()   
        if(self.match([TokenType.FOR])):
            return self.for_statement()       
        if(self.match([TokenType.RETURN])):
            return self.return_statement()                                                                           
        return self.expression_statement()

    # funcDecl       → "fun" function
    def function_declaration(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f"Expecting a name for you {kind}??")
        parameters = []
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'function identifier'")
        if(not(self.check(TokenType.RIGHT_PAREN))):
            parameters.append(self.consume(TokenType.IDENTIFIER, "expect parameter name"))
            while(self.match([TokenType.COMMA])):
                parameters.append(self.consume(TokenType.IDENTIFIER, "expect parameter name"))
                if(len(parameters) > 255):
                    Error.throw_token_error(self.peek(), "Funciton cant have more than 255 parameters")                
        self.consume(TokenType.RIGHT_PAREN, "Expect closing ')' for function declaration")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' for function body")
        body = self.block()
        return Function(name, parameters, body)

    # return Stmt    → "return" expression? ";"
    def return_statement(self):
        keyword = self.previous()
        value = None
        if(not(self.check(TokenType.SEMICOLON))):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return statement")
        return Return(keyword, value)

    # varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
    def var_declaration(self):
        # print("adding var")
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

    # whileStmt     → "while" "(" expression ")" statement
    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while' statement")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect closing ')' for 'while' statement")
        body = self.statement()
        return While(condition, body)

    # forStmt        → "for" "(" (varDecl | exprStmt | ";" ) expression? ";" expression? ")" statement
    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for' statement")
        initializer = None
        increment = None
        condition = None

        if(self.match([TokenType.SEMICOLON])):
            initializer = None
        elif(self.match([TokenType.VAR])):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        if(not(self.check(TokenType.SEMICOLON))):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after 'for' condition")

        if(not(self.check(TokenType.RIGHT_PAREN))):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect closing ')' for 'for' statement")

        body = self.statement()
        if(not(increment == None)):
            body = Block([body, Expression(increment)])
        if(condition == None):
            condition = Literal(True)
        body = While(condition, body)
        if(not(initializer == None)):
            body = Block([initializer, body])
        return body

    # ifStmt         → "if" "(" expression ")" statement ( "else" statement )? 
    def if_statement(self):
        # print("adding 'if' statement")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if' statement")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect closing ')' for 'if' statement")
        then_branch = self.statement()
        else_branch = None
        if(self.match([TokenType.ELSE])):
            else_branch = self.statement()
        return If(condition, then_branch, else_branch)

    # block          → "{" declaration* "}" ;
    def block(self):
        statements = []
        # print(f"building block statement")
        while(not(self.check(TokenType.RIGHT_BRACE)) and (not(self.is_at_end()))):
            # print("appending statement")
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect closing '}'")
        # print(f"statements for block {statements}")
        return statements

    # eexpression     → assignment ;
    def expression(self):
        return self.assignment()

    # assignment     → IDENTIFIER "=" assignment | equality ;
    def assignment(self):
        expr = self.logic_or()
        if(self.match([TokenType.EQUAL])):
            equals = self.previous()
            value = self.assignment()
            if(isinstance(expr, Variable)):
                name = expr.name
                return Assign(name, value)            
            Error.throw_token_error(self.peek(), "Invalid assignment target for variable")
        return expr     

    # logic_or       → logic_and ( "or" logic_and )* ;
    def logic_or(self):
        # print("in logic or")
        expr = self.logic_and()
        while(self.match([TokenType.OR])):
            operator = self.previous()
            right = self.logic_and()
            expr = Logical(expr, operator, right)
        return expr

    # logic_and      → equality ( "and" equality )* ;
    def logic_and(self):
        # print("in logic and")
        expr = self.equality()
        while(self.match([TokenType.AND])):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self):
        # print("in equality")
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
        return self.call()

    # call           → primary ( "(" arguments? ")" )*
    def call(self):
        expr = self.primary()
        while(True):
            if(self.match([TokenType.LEFT_PAREN])):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, callee):
        arguments = []
        if(not(self.check(TokenType.RIGHT_PAREN))):
            arguments.append(self.expression())
            while(self.match([TokenType.COMMA])):
                arguments.append(self.expression())
                if(len(arguments) > 255):
                    Error.throw_generic(self, "Cant have more than 255 arguments for a function")
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect closing ')' for function call argument list")
        print(f"creating function call with {len(arguments)} arguments")
        return Call(callee, paren, arguments)
            

    # primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | list ;
    def primary(self):
        if(self.match([TokenType.FALSE])):
            return Literal(False)
        if(self.match([TokenType.TRUE])):
            return Literal(True)
        if(self.match([TokenType.NIL])):
            return Literal(None)
        if(self.match([TokenType.STRING, TokenType.NUMBER])):
            return Literal(self.previous().literal)
        if(self.match([TokenType.EMLIST])):
            return EMList(self.previous().literal)            
        if(self.match([TokenType.LEFT_PAREN])):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)         
        if(self.match([TokenType.IDENTIFIER])):
            return Variable(self.previous())
        Error.throw_token_error(self, self.peek(), "Expect Expression")

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
        Error.throw_token_error(self, token, error)
        return None

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if(self.previous().token_type == TokenType.SEMICOLON):
                return
            if(self.peek().token_type in [TokenType.CLASS, TokenType.FUNCTION, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN, TokenType.YEET]):
                return
            self.advance()
