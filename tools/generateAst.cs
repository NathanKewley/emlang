using System;

namespace emlang_tools
{
	public class GenerateAST
	{
		public static void main(String[] args)
		{
			if(args.Length != 1){
				Console.WriteLine("error in args");
			}	

			string outputDir = args[0];
		}	
	}
}
