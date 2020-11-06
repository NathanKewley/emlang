from lib.token import Token
from lib.token_types import TokenType
from lib.error import Error

class Lexer():
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        # A dictionary of reserved identifiers
        self.reserved_words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "function": TokenType.FUNCTION,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "YEET": TokenType.YEET,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def lex(self):
        # scan tokens until the end of the source file is reached
        while(not self.is_at_end()):
            self.start = self.current
            self.scan_token()

        # Add an EOF token and return the list of tokens
        # token = Token(TokenType.EOF, "", None, self.line)
        # self.tokens.append(token)
        self.add_token(TokenType.EOF)
        print(f"{len(self.tokens)}: tokens")
        return(self.tokens)

    # scans a single token and returns it
    def scan_token(self):
        char = self.advance()
        
        # Python does not implement switch statement, might look at a better way of implementing this later
        # This is the list of single character tokens, so they can be added directly to the token list without 
        # any additional thought. 
        if(char == '('): self.add_token(TokenType.LEFT_PAREN)
        elif(char == ')'): self.add_token(TokenType.RIGHT_PAREN)
        elif(char == '{'): self.add_token(TokenType.LEFT_BRACE)
        elif(char == '}'): self.add_token(TokenType.RIGHT_BRACE)
        elif(char == ','): self.add_token(TokenType.COMMA)
        elif(char == '.'): self.add_token(TokenType.DOT)
        elif(char == '-'): self.add_token(TokenType.MINUS)
        elif(char == '+'): self.add_token(TokenType.PLUS)
        elif(char == ';'): self.add_token(TokenType.SEMICOLON)
        elif(char == '*'): self.add_token(TokenType.STAR)

        # Here we have optional one or 2 character tokens, these will call out to a special funciton to peek
        # at the next character and resolve the token appropriatly
        # x = 10 if a > b else 11 [https://stackoverflow.com/questions/14461905/python-if-else-short-hand]
        elif(char == '!'): self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif(char == '='): self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif(char == '<'): self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif(char == '>'): self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

        # Now to handle the '/' operator. This one is a bit special since comments are denoted by '//'
        elif(char == '/'): 
            # if a comment
            if(self.match('/')):
                print(f"Comment Detected [//]")
                # advance until we hit and end of line (end of comment)
                while (self.peek() != '\n' and not(self.is_at_end())): 
                    self.advance()

            # if not a comment
            else:
                self.add_token(TokenType.SLASH)

        # we will handle other multi character tokens and literals here
        elif(char == '"'): self.string()
        elif(self.is_digit(char)): self.number()

        # Now we need to identiy identifiers (lel). These will either start with an alphanumrical character or an underscore
        elif(self.is_alpha_num(char)): self.identifier()

        # We have a few special character that we dont care about like spaces
        # and new lines (other than incrementing the line number)
        elif(char == ' ' or char == '\r' or char == '\t'): pass
        elif(char == '\n'): 
            self.line = self.line + 1
            print(f"[{self.line}] new line detected")

        # A catch all at the end for any unsupported characters, we want to throw an error for these
        else:
            Error.throw(self, line = self.line, where = char, message = "Unexpected Character")
        
    # move to the next character in the source 
    def advance(self):
        self.current = self.current + 1
        return(self.source[self.current-1])

    # add a token onto the list
    def add_token(self, token_type):
        print(f"adding token {token_type}")
        token = Token(token_type, self.source[self.start:self.current], None, self.line)
        self.tokens.append(token)

    # add a token onto the list that contains a value
    def add_token_with_value(self, token_type, value):
        print(f"adding token {token_type} with value {value}")
        token = Token(token_type, self.source[self.start:self.current], value, self.line)
        self.tokens.append(token)        

    # check the next token for a match to find multiple character tokens
    def match(self, expected):
        # check not at end of file
        if(self.is_at_end()):
            return False

        # if next character matches return true, else false
        if(self.source[self.current] == expected):
            self.current = self.current + 1
            return True
        return False

    # check if we are at the end of the source file
    def is_at_end(self):
        if(len(self.source) > self.current):
            return False
        return True

    # look at what the next character is and return that
    def peek(self):
        if(self.is_at_end()):
            return('\0')
        return self.source[self.current]
    
    def peek_next(self):
        if(self.current + 1 > len(self.source)):
            return('\0')
        return self.source[self.current+1]        

    def is_digit(self, char):
        if(char >= '0' and char <= '9'):
            return True
        return False

    def is_alpha(self, char):
        if(char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or (char == '_'):
            return True
        return False

    def is_alpha_num(self, char):
        if(self.is_alpha(char)) or (self.is_digit(char)):
            return True
        return False

    def number(self):
        # check the next digit is a number
        while(self.is_digit(self.peek())): self.advance()

        # see if there is a decimal point in the value. We only want to continue if there is another digit directly after the '.'
        # this is because a number cannot end with a .
        if(self.peek() == '.' and self.is_digit(self.peek_next())):
            self.advance()

            # get the rest of the number
            while(self.is_digit(self.peek())): self.advance()
        
        self.add_token_with_value(TokenType.NUMBER, float(self.source[self.start : self.current]))

    # this is for string literal values, we will pull them out here
    def string(self):
        # go through the string until we find the closing "
        while(not(self.peek() == '"')) and (not(self.is_at_end())):
            if(self.peek() == '\n'): 
                self.line = self.line + 1
            self.advance()
        
        # if we hit the end of the file before the closing " we need to error
        if(self.is_at_end()):
            Error.throw(self, line = self.line, where = '"', message = "Unterminated String")

        # advance once for the closing "
        self.advance()

        # strip the quoted from the string and add the token
        self.add_token_with_value(TokenType.STRING, self.source[self.start+1 : self.current-1])      

    # we need to determine if the identifier is reserved or user defined and treat it as such
    def identifier(self):
        while(self.is_alpha_num(self.peek())):
            self.advance()
        
        # Check if reserved word
        token_text = self.source[self.start : self.current]
        if(token_text in self.reserved_words.keys()):
            self.add_token(self.reserved_words[token_text])    

        # else it is user defined
        else:
            self.add_token(TokenType.IDENTIFIER)