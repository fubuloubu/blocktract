import sys
import json
import ast


def debug(label, text):
    if not isinstance(label, str):
        label = label.__class__.__name__
    if not isinstance(text, str):
        text = json.dumps(text, indent=2)
    print(label +':', file=sys.stderr)
    print(text, file=sys.stderr)


def ast2objtree(node, node_type=ast.AST):
    obj = {}
    for field in node._fields:
        inner_node = getattr(node, field)
        if inner_node is not None:
            if isinstance(inner_node, list) and len(inner_node) > 0:
                obj[field] = [ast2objtree(n) for n in inner_node]
            elif isinstance(inner_node, node_type):
                obj[field] = ast2objtree(inner_node)
            else:
                obj[field] = str(inner_node)
    # json obj of class = dict of fields
    if obj is not {}:
        return { node.__class__.__name__ : obj }
