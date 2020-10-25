import os
from jinja2 import Environment, FileSystemLoader, Template

# delete the ast
ast_out_file = "ast.py"
try:
    os.remove(ast_out_file)
except:
    pass

# define the ast properties
expressions = [
    ["Binary", ["left", "operator", "right"]],
    ["Grouping", ["expression"]],
    ["Literal", ["value"]],
    ["Unary", ["operator", "right"]]
]

# load the Jinja2 template
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
ast_template = env.get_template('ast_template.j2')

# render the template
ast_content = ast_template.render(expressions=expressions)

# write ast out to a file
with open(ast_out_file, 'a') as out:
    out.write(ast_content + '\n')