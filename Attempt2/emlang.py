from lib.lexer import Lexer
from lib.error import Error
from lib.parser import Parser
from lib.interpreter import Interpreter
from ast_printer import Ast_Printer
import sys

# This is the main entry point to the program, this is essentailly a shell that calls our to the requited parts. 

class Emlang():
    hadError = False

    # This is the main source execution point
    def run(self, source):
        # Create the lexer and generate tokens
        lexer = Lexer(source)
        tokens = lexer.lex()

        # create the parser and parse the tokens
        parser = Parser(tokens)
        expression = parser.parse()

        # if(hadError):
        #     return
        print(Ast_Printer().print_ast(expression)); 
        
        # create the interpreter and interpret the expression
        interpreter = Interpreter()
        interpreter.interprert(expression)

    # Read and execute a file
    def runFile(self, sourceFile):
        file = open(sourceFile,mode='r')
        source = file.read()
        file.close()
        self.run(source)

        # Exit with an error code if there was a problem
        if (self.had_error): 
            sys.exit(65)

    # if we want an interactive session
    def runPrompt(self):
        # to implement
        print("interactive prompt not implemented")
        return None

    # Entry point of the program that determins what to do based on cli parameters
    def __init__(self, args):
        self.had_error = False

        if(len(args) > 1):
            print("Usage: python3 emlang.py <script>")

        if(len(args) == 1):
            self.runFile(args[0])
        
        if(len(args) == 0):
            self.runPrompt()

if __name__ == '__main__':
    result = Emlang(sys.argv[1:])
