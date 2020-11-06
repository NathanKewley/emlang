from lib.lexer import Lexer

class TestLexer:
    def get_file_contents(self, test_file):
        file = open(test_file, mode='r')
        source = file.read()
        file.close()
        return source

    def test_token_generation(self):
        source = self.get_file_contents("tests/eml/test_lexer.eml")
        lexer = Lexer(source)
        tokens = lexer.lex()
        assert len(tokens) == 62
