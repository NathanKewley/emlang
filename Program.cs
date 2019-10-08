using System;
using System.Collections.Generic;

namespace emlang
{
    class Program
    {
		private static bool hadError = false;

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
			
			if(hadError)
			{
				Environment.Exit(65);
			}
		}

		static void runPrompt()
		{
			for(;;)
			{
				Console.Write("> ");
				string code = Console.ReadLine();
				run(code);
				hadError = false;
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

		static void error(int line, string message)
		{
			report(line, "", message);
		}

		private static void report(int line, string at, string message)
		{
			Console.WriteLine($"Error [{line}] pos {at} - {message}");
			hadError = true;	
		}
    }
}
