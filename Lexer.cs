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
				
				// function callouts
				case '/': slash(); break;
				case '"': stringLiteral(); break;

				// dual character lexmes
				case '!': addToken(match('=') ? TokenType.BANG_EQUAL : TokenType.BANG); break;
				case '=': addToken(match('=') ? TokenType.EQUAL_EQUAL : TokenType.EQUAL); break;
				case '<': addToken(match('=') ? TokenType.LESS_EQUAL : TokenType.LESS); break;
				case '>': addToken(match('=') ? TokenType.GREATER_EQUAL : TokenType.GREATER); break;

				// special character lexmes
				case '\n': line = line + 1; break;
				case ' ': break;
				case '\r': break;
				case '\t': break;

				// throw error on enexpected tokens
				default: defaultCase(c); break;
			}	
		}

		private void defaultCase(char c){
			if(isDigit(c))
			{
				numberLiteral();
			}
			else if(isAlpha(c))
			{
				identifier();
			}
			else
			{
				Program.error(line, $"Unexpected token: {c}");
			}
		}

		private void slash()
		{
			if(match('/'))
			{
				Console.WriteLine("comment detected");
				while(peek() != '\n' && !isAtEnd()){advance();}
			}
			else
			{
				addToken(TokenType.SLASH);
			}	
		}

		private void stringLiteral()
		{
			// track length of a string so we can Substring it later
			int stringLength = 0;

			while(peek() != '"' && !isAtEnd())
			{
				if(peek() == '\n'){line = line + 1;}
				stringLength = stringLength + 1;
				advance();
			}

			if(isAtEnd())
			{
				Program.error(line, "non-terminating string");
			}

			//this is for the closing '"'
			advance();

			// trim the quotes form the value
			string literal = source.Substring(start+1, stringLength);
			addToken(TokenType.STRING, literal);
			Console.WriteLine($"String Found: {literal}");
		}

		private void numberLiteral()
		{
			int numberLength = 1;

			while(isDigit(peek()))
			{
				advance();
				numberLength++;
			}

			if(peek() == '.' && isDigit(peekNext()))
			{
				advance();
				numberLength++;

				while(isDigit(peek()))
				{
					advance();
					numberLength++;
				}
			}	

			double number = Double.Parse(source.Substring(start, numberLength));
			addToken(TokenType.NUMBER, number);
			Console.WriteLine($"number detected: {number}");
		}

		public void identifier(){
			while(isAlphaNumeric(peek())){ advance(); }
			
			addToken(TokenType.IDENTIFIER);
		}

		private bool match(char expected)
		{
			if(isAtEnd()){return(false);}
			if(source[current] != expected){return(false);}

			current = current + 1;
			return(true);
		}

		private bool isDigit(char c)
		{
			if(c >= '0' && c <= '9'){
				return(true);
			}
			else
			{
				return(false);
			}
		}

		private bool isAlpha(char c)
		{
			return
			(
				(c >= 'a' && c <= 'z') ||
				(c >= 'A' && c <= 'Z') ||
				(c == '_')
			);
			
		}

		private bool isAlphaNumeric(char c)
		{
			return(isAlpha(c) || isDigit(c));
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
		
		private char peekNext()
		{
			if((current + 1) >= source.Length){return('\0');}
			return(source[current + 1]);
		}
	}
}
