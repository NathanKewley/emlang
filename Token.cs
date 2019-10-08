using System;

namespace emlang
{
	public class Token
	{
		TokenType type;
		string lexme;
		object literal;
		int line;

		public Token(TokenType type, string lexme, object literal, int line)
		{
			this.type = type;
			this.lexme = lexme;
			this.literal = literal;
			this.line = line;
		}

		public string toString()
		{
			return($"{type} {lexme} {literal}");
		}
	}
}
