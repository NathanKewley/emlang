using System;
using System.Collections.Generic;

namespace emlang
{
    class Program
    {
        static void Main(string[] args)
        {
			if(args.Length > 1)
			{
	            Console.WriteLine("Usage: emlang <script>");
			}
			
			else if(args.Length == 1) 
			{
				runFile(args[0]);
			}
			
			else 
			{
				runPrompt();
			}
        }

		static void runFile(string path)
		{
			Console.WriteLine($"Running file {path}");
			string code = System.IO.File.ReadAllText(path);
			run(code);
		}

		static void runPrompt()
		{
			for(;;)
			{
				Console.Write("> ");
				string code = Console.ReadLine();
				run(code);
			}
		}

		static void run(string code)
		{
			Lexer lexer = new Lexer(code);
			List<Token> tokens = lexer.lex();

			foreach(Token token in tokens)
			{
				Console.WriteLine(token);
			}
		}
    }
}
