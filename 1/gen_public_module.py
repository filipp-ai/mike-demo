import ast
import textwrap
"""
prepare tree_services.py for public repository
could be extended for cleaning up any other modules
- Get ../dataheroes/services/tree_services.py
- clean up decorators
- clean up class and function bodies
- clean up certain class and methods
- save in current dir as tree_services.py
"""


class MethodRemover(ast.NodeTransformer):
    def visit_ClassDef(self, node):
        # keep only these classes
        if node.name in ['CoresetTreeService', 'CoresetTreeServiceLG']:
            node.body = [ast.Pass()] + [b for b in node.body
                                        # remove everything but methods
                                        if b.__class__.__name__ == 'FunctionDef'
                                            # delete few methods
                                            and 'tensor' not in b.name
                                            and b.name != 'explain'
                                            and b.name != 'optimized_for'
                                            and b.name != 'chunk_size'
                                            and b.name != 'max_memory_gb'
                                            and not b.name.startswith('_')
                                        ]
        else:
            return None


class MethodTextRemover(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        docstring = ast.get_docstring(node)
        if docstring:
            docstring = '\n' + textwrap.indent(docstring, '        ')
            docstring_node = ast.Expr(value=ast.Str(s=docstring))
            node.body = [docstring_node, ast.Pass()]
        else:
            node.body = [ast.Pass()]


with open("../dataheroes/services/tree_services.py") as f:
    source = f.read()

tree = ast.parse(source)
MethodRemover().visit(tree)
MethodTextRemover().visit(tree)
# fix missing location information in the generated AST
ast.fix_missing_locations(tree)
code = compile(tree, "<string>", "exec")
output_file = "tree_services.py"

# write the modified source code to a new file
with open(output_file, "w") as f:
    lines = ast.unparse(tree).split('\n')
    for line in lines:
        # remove import and decorators
        if 'import ' not in line and ' @' not in line:
            f.write(line + '\n')
