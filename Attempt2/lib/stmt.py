class Stmt():
	def visitor(self, visitor):
		def visit_expression_stmt(self, expr):
			pass
		def visit_print_stmt(self, expr):
			pass
		def visit_var_stmt(self, expr):
			pass
		def visit_yeet_stmt(self, expr):
			pass
		def visit_block_stmt(self, expr):
			pass
		def visit_if_stmt(self, expr):
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

class Var(Stmt):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        
    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

class Yeet(Stmt):
    def __init__(self, expression):
        self.expression = expression
        
    def accept(self, visitor):
        return visitor.visit_yeet_stmt(self)

class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements
        
    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        
    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

