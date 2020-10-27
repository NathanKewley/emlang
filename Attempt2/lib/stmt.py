class Stmt():
	def visitor(self, visitor):
		def visit_expression_stmt(self, expr):
			pass
		def visit_print_stmt(self, expr):
			pass
		def visit_yeet_stmt(self, expr):
			pass
		
class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression
        
    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression
        
    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class Yeet(Stmt):
    def __init__(self, expression):
        self.expression = expression
        
    def accept(self, visitor):
        return visitor.visit_yeet_stmt(self)
