using System;
using System.Collections.Generic;

namespace emlang
{
	public class Lexer
	{
		List<Token> tokens = new List<Token>();
		string source;
		int start = 0;
	    int current = 0; 
		int line = 1;

		public Lexer(string code)
		{
			this.source = code;
		}

		private bool isAtEnd()
		{
			return(current >= source.Length);
		}

		public List<Token> lex()
		{
			while(!isAtEnd())
			{
				start = current;
				scanToken();
			}

			tokens.Add(new Token(TokenType.EOF, "", null, line));
			return(tokens);
		}

		private void scanToken()
		{
			char c = advance();

			switch(c)
			{
				case '(': addToken(TokenType.LEFT_PAREN); break;
			}	
		}

		private char advance()
		{
			current = current + 1;
			return(source[current-1]);
		}

		private void addToken(TokenType type)
		{
			addToken(type, null);
		}

		private void addToken(TokenType type, Object literal)
		{
			Console.WriteLine($"added token {type}");
		}
	}
}
