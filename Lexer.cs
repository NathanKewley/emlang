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

		private bool isAtEnd(){
			return(current >= source.Length);
		}

		public List<Token> lex()
		{
			while(!isAtEnd()){
				start = current;
				scanToken();
			}

			tokens.Add(new Token(TokenType.EOF, "", null, line));
			return(tokens);
		}
	}
}
