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
				case ')': addToken(TokenType.RIGHT_PAREN); break;
				case '{': addToken(TokenType.LEFT_BRACE); break;
				case '}': addToken(TokenType.RIGHT_BRACE); break;
				case ',': addToken(TokenType.COMMA); break;
				case '.': addToken(TokenType.PERIOD); break;
				case ';': addToken(TokenType.SEMICOLON); break;
				case '+': addToken(TokenType.PLUS); break;
				case '-': addToken(TokenType.MINUS); break;
				case '*': addToken(TokenType.STAR); break;

				default: Program.error(current, $"Unexpected token: {c}"); break;
			}	
		}

		private bool match(char expected)
		{
			if(isAtEnd()){return(false);}
			if(source[current] != expected){return(false);}

			current = current + 1;
			return(true);
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
			string text = source.Substring(start, (current-start));
			tokens.Add(new Token(type, text, literal, line));
			Console.WriteLine($"added token {type}");
		}
	}
}
