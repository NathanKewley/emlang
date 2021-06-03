import os
from jinja2 import Environment, FileSystemLoader, Template

expr_out_file = "../lib/expr.py"
stmt_out_file = "../lib/stmt.py"

try:
    os.remove(expr_out_file)
    os.remove(stmt_out_file)
except:
    pass

# define the expressions
expressions = [
    ["Binary", ["left", "operator", "right"]],
    ["Grouping", ["expression"]],
    ["Literal", ["value"]],
    ["Unary", ["operator", "right"]],
    ["Variable", ["name"]],
    ["Assign", ["name", "value"]],
    ["Logical", ["left", "operator", "right"]],
    ["Call", ["callee", "paren", "arguments"]]
]

# define the statements
statements = [
    ["Expression", ["expression"]],
    ["Print", ["expression"]],
    ["Var", ["name", "expression"]],
    ["Yeet", ["expression"]],
    ["Block", ["statements"]],
    ["If", ["condition", "then_branch", "else_branch"]],
    ["While", ["condition", "body"]],
    ["Function", ["name", "params", "body"]],
    ["Return", ["keyword" ,"value"]]
]

# load the Jinja2 templates
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
expr_template = env.get_template('expr_template.j2')
stmt_template = env.get_template('stmt_template.j2')

# render expr template
expr_content = expr_template.render(expressions=expressions)
with open(expr_out_file, 'a') as out:
    out.write(expr_content + '\n')

# render stmt template
stmt_content = stmt_template.render(expressions=statements)
with open(stmt_out_file, 'a') as out:
    out.write(stmt_content + '\n')