import sys
import json
import ast

# 0: functional debug, 5: compiler_stages
LEVEL=1

def debug(label, text, level=0):
    if level < LEVEL:
        return
    if not isinstance(label, str):
        label = 'class ' + label.__class__.__name__
    if not isinstance(text, str):
        text = json.dumps(text, indent=2)
    print(label +':', file=sys.stderr)
    print('  '+text.replace('\n','\n  '), file=sys.stderr)
    print('', file=sys.stderr)


def ast2objtree(node, node_type):
    obj = {}
    for field in node._fields:
        inner_node = getattr(node, field)
        if inner_node is not None:
            if isinstance(inner_node, list):
                obj[field] = [ast2objtree(n, node_type) for n in inner_node]
            elif isinstance(inner_node, node_type):
                obj[field] = ast2objtree(inner_node, node_type)
            else:
                obj[field] = str(inner_node)
    # json obj of class = dict of fields
    if len(node._fields) > 0:
        return { node.__class__.__name__ : obj }
    else:
        return node.__class__.__name__
