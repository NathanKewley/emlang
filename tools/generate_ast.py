import os
from jinja2 import Environment, FileSystemLoader

# define the ast properties
expressions = [
    ["Binary", ["Expr left", "Token operator", "Expr right"]],
    ["Grouping", ["Expr expression"]],
    ["Literal", ["Object value"]],
    ["Unary", ["Token operator", "Expr right"]]
]

# load the Jinja2 template
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
ast_template = env.get_template('ast_template.j2')

# render the template
ast_content = ast_template.render(expressions=expressions)

print(ast_content)