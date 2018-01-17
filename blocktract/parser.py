import ast

from .types import (
        GlobalType, global_types,
        local_types,
    )
from .context import Context
from .statements import (
        parse_statement,
        ReturnStmt,
    )

def parse_global(name: str, typeclass: str, value=None) -> GlobalType:
    assert typeclass in global_types.keys(), \
            "'{}' is not a supported type!".format(typeclass)
    return global_types[typeclass](name, namespace='self', value=value)

def parse_args(args: list) -> dict:
    parsed_args = {}
    for name, typeclass in args:
        assert typeclass in local_types.keys(), \
                "'{}' is not a supported type!".format(typeclass)
        assert name not in parsed_args.keys(), \
                "Arg '{}' already in args!".format(name)
        parsed_args[name] = local_types[typeclass](name)
    return parsed_args

class Function:
    def __init__(self, context: Context, decorators=None, args=None, body=None, return_type=None):
        self.decorators = [d.id for d in decorators]
        self.args = parse_args([(a.arg, a.annotation.id) for a in args.args])
        # Push new context (aka variable scope) when evaluating a set of statements
        context.push(self.args)
        self.body = [parse_statement(s, context) for s in body]
        self.returns = return_type
        # Check return type
        for stmt in self.body:
            if isinstance(stmt, ReturnStmt):
                assert return_type in local_types.keys(), \
                        "'{}' is not a supported type!".format(return_type)
                assert isinstance(stmt.returns, local_types[return_type]), \
                        "Statement returns '{}' instead of '{}':\n{}".\
                                format(local_types[return_type], stmt.returns, stmt)

    def __repr__(self):
        # JSON formatted output
        repr_str = "{"
        repr_str += "'decorators': {}, ".format(self.decorators) if self.decorators else ""
        repr_str += "'args': [{}], ".format(", ".\
                    join(["{"+"'{}': '{}'".format(k, repr(v))+"}" for k, v in self.args.items()])) \
                            if self.args else ""
        repr_str += "'body': {}, ".format(self.body) if self.body else ""
        repr_str += "'returns': {}, ".format(self.returns) if self.returns else ""
        repr_str = repr_str[:-2] + "}"  # Remove extra space and comma
        return repr_str


# Top-Level Node of VyAST
class Contract:
    def __init__(self, module: ast.Module):
        state = {}
        constructor = None
        methods = {}
        for node in module.body:
            if isinstance(node, ast.AnnAssign):
                assert not methods, "Cannot add global after method!"
                assert node.target.id not in state, \
                        "'{}' already defined!".format(node.target.id)
                state[node.target.id] = parse_global(node.target.id,
                                                     node.annotation.id,
                                                     value=node.value)
            elif isinstance(node, ast.FunctionDef):
                if not hasattr(self, 'context'):
                    # Define top-level context
                    self.context = Context(state=state)
                assert node.name not in methods, \
                        "'{}' already defined!".format(node.target.id)
                func = Function(context=self.context,
                                decorators=node.decorator_list,
                                args=node.args,
                                body=node.body,
                                return_type=node.returns.id if node.returns else None)
                if node.name == '__init__':
                    constructor = func
                else:
                    methods[node.name] = func
            else:
                raise IOError("Node {} not allowed!".format(type(node)))

        self.state = state
        self.constructor = constructor
        self.methods = methods

    def __repr__(self):
        # JSON formatted output
        repr_str = "{"
        repr_str += ("'state': {"+", ".join(
                        ["'{}': '{}'".format(k, repr(v)) for k, v in self.state.items()]
                    )+"}, ") if self.state else ""
        repr_str += "'constructor': {}, ".format(self.constructor) if self.constructor else ""
        repr_str += "'methods': {}, ".format(self.methods) if self.methods else ""
        repr_str = repr_str[:-2] + "}"  # Remove extra space and comma
        return repr_str

def parse_vy(raw_code: str) -> Contract:
    py_ast = ast.parse(raw_code)
    vy_ast = Contract(py_ast)
    print(vy_ast)
    return vy_ast
