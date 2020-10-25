class Expr():
	
	class Binary(Expr):
		def __init__(self, left, operator, right):
			
			this.left = left
			
			this.operator = operator
			
			this.right = right
			
	
	class Grouping(Expr):
		def __init__(self, expression):
			
			this.expression = expression
			
	
	class Literal(Expr):
		def __init__(self, value):
			
			this.value = value
			
	
	class Unary(Expr):
		def __init__(self, operator, right):
			
			this.operator = operator
			
			this.right = right
			
	
