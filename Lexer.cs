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
				// single character lexmes
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

				// dual character lexmes
				case '!': addToken(match('=') ? TokenType.BANG_EQUAL : TokenType.BANG); break;
				case '=': addToken(match('=') ? TokenType.EQUAL_EQUAL : TokenType.EQUAL); break;
				case '<': addToken(match('=') ? TokenType.LESS_EQUAL : TokenType.LESS); break;
				case '>': addToken(match('=') ? TokenType.GREATER_EQUAL : TokenType.GREATER); break;

				// / & comments
				case '/': 
					if(match('/'))
					{
						Console.WriteLine("comment detected");
						while(peek() != '\n' && !isAtEnd()){advance();}
					}
					else{
						addToken(TokenType.SLASH);
					}	
					break;

				// special character lexmes
				case '\n': line = line + 1; break;
				case ' ': break;
				case '\r': break;
				case '\t': break;

				// throw error on enexpected tokens
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

		private char peek()
		{
			if(isAtEnd()){return '\0';}
			return(source[current]);
		}
	}
}
