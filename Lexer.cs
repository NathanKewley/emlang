using System;
using System.Collections.Generic;

namespace emlang
{
	public class Lexer
	{
		string code;

		public Lexer(string inCode)
		{
			code = inCode;
		}

		public List<Token> lex()
		{
			List<Token> tokens = new List<Token>();
			return(tokens);
		}
	}
}
